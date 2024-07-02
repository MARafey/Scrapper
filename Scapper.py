import requests as req
from bs4 import BeautifulSoup as bsp
import pandas as pd
import csv
import json
import time
from selenium import webdriver


def getPage(url):  # function to get the html of the scrapped page for readability
    response = req.get(url)
    if not response.ok:
        print("Server responded with exit code:", response.status_code)  # if scrapping is not allowed
        return None
    else:
        soup = bsp(response.text, "lxml")  # converting to html
        pretty = soup.prettify()  # increasing readability
        with open('scrapped.html', mode='w',
                  encoding='utf-8') as htmlFile:  # specify encoding method for writing in a file
            htmlFile.write(pretty)
        return soup


def findContent(soup, info,last_height):  # function to extract the required elements from the website soup
    if soup is None:  # if previous function returned none
        return

    # going from basic to specific
    ol = soup.find('ul', id='product-grid')

    articles = []
    for i in range(1, last_height):
        articles += ol.find_all('li', class_=f'coll-main-wrapper grid-layout grid__item page-{i}')

    for i in range(len(articles)):
        # extracting the title
        Sup = articles[i].find('div', class_='card-wrapper underline-links-hover')

            # extracting the Name
        try:
            Name = articles[i].find('h3', class_='card__heading')
            price = Name.text.strip()  # if price_text.startswith('£') else 0.0
            print(price)
            info['Name'].append(price)
        except:
            info['Name'].append(' ')

            # extracting the price
        try:
            Name = articles[i].find('span', class_='money')
            price = Name.text.strip()  # if price_text.startswith('£') else 0.0
            print(price)
            info['Price'].append(price)
        except:
            info['Price'].append(' ')

            # extracting the Image
        try:
            head = articles[i].find('img')
            info['Image'].append(head['src'])
        except:
            info['Image'].append(' ')


def main():  # the function in which all the functionality takes place
    info = {  # uninitialized dictionary to use for later
        'Name': [],
        'Price': [],
        'Image': [],
    }


    url = 'https://outfitters.com.pk/collections/men-mid-summer-sale'

    # Using Selenium to scroll down the page
    driver = webdriver.Chrome()
    driver.get(url)

    # code to scroll down the page to the end
    SCROLL_PAUSE_TIME = 2.5
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        SCROLL_PAUSE_TIME += 0.5
        new_height = driver.execute_script("return document.body.scrollHeight")

        # If reached the end of the page
        if new_height == last_height:
            # Scroll back to top
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(SCROLL_PAUSE_TIME)
            # Scroll down to bottom again
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    soup = bsp(driver.page_source, 'html.parser')
    driver.quit()

    findContent(soup, info,last_height)  # finding and extracting required stuff


    # Write dictionary to CSV file
    csvFile = 'output.csv'  # writing the headings of the columns
    with open(csvFile, mode='w', newline='', encoding='utf-8') as file:  # using an encoder for special characters
        fieldnames = list(info.keys())  # typecasting the keys into a list
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(info['Name'])):  # according to number of items, we are copying every value of every key into it's respective heading
            row = {}
            for key in info.keys():
                row[key] = info[key][i]

            writer.writerow(row)


if __name__ == '__main__':
    main()
