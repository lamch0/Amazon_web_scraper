# Amazon_web_scraper
An amazon web scraper in python with Selenium and BeautifulSoup that can get the fields down below in a csv file.

## Setup
Please download your web driver.

If you are using chrome, download it from https://chromedriver.chromium.org/downloads.

You can check your chrome version with chrome://version/.

## How it works
Change the keyword to your desire search keyword.

It normally takes around 5-7 minutes for 3 pages of each category.

If you get errors, it probably relates to the class names of the items. 

You may uncomment the line ```# driver = webdriver.Chrome(service = Service(executable_path=driver_path)) # show browser``` in order to show your brower and inspect for the respective class name. (However, after testing, showing the browser is less likely to be blocked by amazon. Therefore, showing the browser is default)

### Fields for the product
* Name
* Asin (the unique code for each product)
* Price
* Ratings
* Ratings numbers
* Links to product details
* Images Links

## Remarks
As Amazon does not allow auto scraping with just BeautifulSoup, using Selenium can let us simulate a human and scrape what we want.

In this application, I am trying to have the keyword and product name in CHINESE. If you want to set it in English, you might need to pay attention to the web url and class names as they might vary.

Also, Amazon's website might change from time to time so it is normal to have the class names or even the DOM element changed.

# Reference 
The code is amended but based on https://medium.com/@jb.ranchana/web-scraping-with-selenium-in-python-amazon-search-result-part-1-f09c88090932.
