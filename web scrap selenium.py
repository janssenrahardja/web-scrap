#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import bs4 as bs
import pandas as pd
import time


# In[2]:


browser = webdriver.Chrome("chromedriver")


# In[3]:


names=[] #list name of the product
stores=[] #list store name of the product
prices=[] #list price of the product
ratings=[] #list rating of the product
images=[] #list image url of the product
descriptions=[] #list description of the product

productUrls=[] #list product url

url = 'https://www.tokopedia.com/p/handphone-tablet/handphone'
#xpath
div_productList = '//div[@data-testid="lstCL2ProductList"]'
btn_next = '//button[@aria-label="Laman berikutnya"]'


# In[4]:


def getDataProduct(productLinks, soup):
    #filter data products
    dataProducts = soup.find('div', attrs={'data-testid':'lstCL2ProductList'})

    for data in dataProducts.findAll('a',href=True, attrs={'data-testid':'lnkProductContainer'}):
        topads = data.find('img', attrs={'alt':'topads icon'})
        if not (topads) :
            productUrls.append(data['href'])


# In[5]:


#open browser, scroll to end, and sleep to load page
browser.get(url)
browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(5)

#search next pagination element
btnNext = browser.find_element_by_xpath(btn_next)

#get html
html = browser.page_source
soup = bs.BeautifulSoup(html,'html.parser')

#get data from first page
getDataProduct(productUrls, soup)
#navigate to next page
btnNext.click()
getDataProduct(productUrls, soup)

top100Urls = productUrls[0:100]


# In[6]:


#process data from top 100
for data in top100Urls:
    #open each url
    browser.get(data)
    time.sleep(5)
    
    #get html
    html = browser.page_source
    soup = bs.BeautifulSoup(html,'html.parser')
    
    #data product
    name = soup.find('h1', attrs={'data-testid':'lblPDPDetailProductName'})
    store = soup.find('a', attrs={'data-testid':'llbPDPFooterShopName'})
    storeName = store.find('h2')
    description = soup.find('div', attrs={'data-testid':'lblPDPDescriptionProduk'})
    price = soup.find('div', attrs={'data-testid':'lblPDPDetailProductPrice'})
    rating = soup.find('span', attrs={'data-testid':'lblPDPDetailProductRatingNumber'})
    image = soup.find('img', attrs={'data-testid':'PDPMainImage'})
    imageUrl = image['src']
    
    #insert into list
    names.append(name.text)
    stores.append(storeName.text)
    prices.append(price.text)
    ratings.append(rating.text)
    images.append(imageUrl)
    descriptions.append(description.text)


# In[7]:


#generate data frame using pandas
df = pd.DataFrame({'Name of Product':names,'Description':descriptions,'Image Link':images,'Price':prices,'Rating':ratings,'Name of Store':stores})
#export to csv
df.to_csv('products.csv', index=False, encoding='utf-8')

