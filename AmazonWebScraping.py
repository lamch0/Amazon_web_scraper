# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import csv

# assign the driver path
driver_path = './chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--headless')

# create a driver object using driver_path as a parameter
# driver = webdriver.Chrome(options = options, service = Service(executable_path=driver_path)) # run in background
driver = webdriver.Chrome(service = Service(executable_path=driver_path)) # show browser

# open the category list
categories = pd.read_csv('category_list.csv', sep="`")

# assign your website to scrape
web = 'https://www.amazon.com/-/zh_TW/'

# create empty lists for containing the data we'd like to scrape
product_name = []
product_asin = []
product_price = []
product_ratings = []
product_ratings_num = []
product_link = []


driver.get(web)

for cat_count, category in enumerate(categories['synonyms']):
    category = str(category).split(',')[0]
    if (category == 'nan'):
        category = categories['category'][cat_count]
    cat_name = categories['category'][cat_count]

    results = []

    # assign any keyword for searching
    keyword = category
        
    driver.implicitly_wait(3)
    
    # create WebElement for a search box
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')

    # clear the searchbox
    search_box.clear()

    # type the keyword in searchbox
    search_box.send_keys(keyword)

    # create WebElement for a search button 
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')

    # click search_button
    search_button.click()

    print('====================================searching for {}===================================='.format(cat_name))

    # wait for the page to download
    driver.implicitly_wait(3)

    product_img_link = []
    count = 0 
    
    # loop for 3 pages
    for i in range(4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # in case no result found
        try:
            items = WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
        except:
            break
            
        for item in items:
            # find product name
            try:
                name = item.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')
            except:
                name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')

            # find product asin
            data_asin = item.get_attribute("data-asin")

            # find prices
            whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
            fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')

            if whole_price != [] and fraction_price != []:
                price = '.'.join([whole_price[0].text, fraction_price[0].text])
            else:
                price = 0

            # find a ratings box
            ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

            if ratings_box != []:
                ratings = ratings_box[0].get_attribute('aria-label')
                ratings_num = ratings_box[1].get_attribute('aria-label')
            else:
                ratings, ratings_num = 0, 0

            # find the details link
            link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")

            # find the product image link
            img_link = item.find_element(By.XPATH, './/img[@class="s-image"]').get_attribute('src')
            product_img_link.append(img_link)
            
            # create image
            if not os.path.exists("images"):
                os.mkdir("images")
            image = requests.get(img_link)
            if not os.path.exists("images/{}".format(cat_name)):
                os.mkdir("images/{}".format(cat_name))
            image_path = "./images/{}/".format(cat_name) + 'img_'+ str(count+1) + ".jpg"
            count += 1
            with open(image_path, "wb") as file:
                print('writing images to {}'.format(image_path))
                file.write(image.content)

            results.append((name.text, data_asin, price, ratings, str(ratings_num), link, img_link, cat_name, image_path))

            
        try:
            # find the next page button
            next = driver.find_element(By.XPATH, '//a[contains(@class, "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")]').get_attribute('href')
            # go to next page
            driver.get(next)
            print('==================================next page==================================')
        except:
            continue

    df = pd.DataFrame(results)
    
    if not os.path.exists('result.csv'):
        # create csv
        df.to_csv('result.csv', sep='`', index=False, header =["product_name", "product_asin", "product_price", "product_ratings", "product_ratings_num", "product_link", "img_link", "category", "img_dir"])
        print('creating new csv...')
    else:
        # append csv
        df.to_csv('result.csv', sep='`', mode='a', index=False, header=False)
        print('appending csv...')

# quit the driver after finishing scraping 
driver.quit()
print('Finish scraping!')