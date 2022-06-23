#!/usr/bin/env python
# coding: utf-8

# In[110]:


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


# In[111]:


# assign the driver path
driver_path = './chromedriver'


# In[112]:


options = webdriver.ChromeOptions()
options.add_argument('--headless')


# In[113]:


# create a driver object using driver_path as a parameter
# driver = webdriver.Chrome(options = options, service = Service(executable_path=driver_path)) # run in background
driver = webdriver.Chrome(service = Service(executable_path=driver_path)) # show browser


# In[114]:


# assign your website to scrape
web = 'https://www.amazon.com'

driver.get(web)


# In[117]:


# assign any keyword for searching
keyword = '眼鏡'


# In[118]:


# create WebElement for a search box
search_box = driver.find_element(By.ID, 'twotabsearchtextbox')


# In[119]:


# type the keyword in searchbox
search_box.send_keys(keyword)


# In[120]:


# create WebElement for a search button 
search_button = driver.find_element(By.ID, 'nav-search-submit-button')


# In[121]:


# click search_button
search_button.click()


# In[122]:


# wait for the page to download
driver.implicitly_wait(5)


# In[123]:


# create empty lists for containing the data we'd like to scrape
product_name = []
product_asin = []
product_price = []
product_ratings = []
product_ratings_num = []
product_link = []
product_img_link = []
results = []


# In[124]:


items = driver.find_elements(By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')


# In[125]:


items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))


# In[126]:


for item in items:
    # find product name
    name = item.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')
#     product_name.append(name.text)
    
    # find product asin
    data_asin = item.get_attribute("data-asin")
#     product_asin.append(data_asin)
    
    
    # find prices
    whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
    fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')

    if whole_price != [] and fraction_price != []:
        price = '.'.join([whole_price[0].text, fraction_price[0].text])
    else:
        price = 0
        
#     product_price.append(price)
    
    # find a ratings box
    ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

    if ratings_box != []:
        ratings = ratings_box[0].get_attribute('aria-label')
        ratings_num = ratings_box[1].get_attribute('aria-label')
    else:
        ratings, ratings_num = 0, 0

#     product_ratings.append(ratings)
#     product_ratings_num.append(str(ratings_num))

    # find the details link
    link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
#     product_link.append(link)
    
    # find the product image link
    img_link = item.find_element(By.XPATH, './/img[@class="s-image"]').get_attribute('src')
    product_img_link.append(img_link)
    
    results.append((name.text, data_asin, price, ratings, str(ratings_num), link, img_link))


# In[106]:


# quit the driver after finishing scraping 
driver.quit()


# In[127]:


df = pd.DataFrame(results, columns=["product_name", "product_asin", "product_price", "product_ratings", "product_ratings_num", "product_link", "img_link"])
print(df)


# In[108]:


df.to_excel("test.xlsx", sheet_name="test", index=False)


# In[129]:


for index, link in enumerate(product_img_link):
    if not os.path.exists("images"):
        os.mkdir("images")
    image = requests.get(link)
    with open("./images" + str(index+1) + ".jpg", "wb") as file:
        file.write(image.content)
    


# In[ ]:




