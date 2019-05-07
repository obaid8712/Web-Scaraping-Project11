#!/usr/bin/env python
# coding: utf-8
# # START WEB SCRAPING : MISSION TO MARS

# Import Dependency
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

# ## Mac User
# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
#!which chromedriver
#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#browser = Browser('chrome', **executable_path, headless=False)

# ## Windows User
# Run crome browser for Windows
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    browser = init_browser()

    # Vist NASA Mars News Web
    ##########################
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # collect the latest News Title and Paragraph Text
    slide = soup.find_all('li', class_='slide')[0]

    news_title=slide.find_all('div',class_='content_title')[0].text
    news_p=slide.find_all('div',class_='article_teaser_body')[0].text
    #print(news_title)
    #print(news_p)

    # Visit JPL Mars Space Images - Featured Image
    ################################################
    url='https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(url)
    time.sleep(2)
    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    slide=soup.find_all('div', class_="carousel_items")[0]
    #print(slide)
    # Get the style reference for image url
    url_text = [i['style'] for i in soup.find_all('article', style=True)]
    #print(url_text)
    # Clean and Get the Featured Image url only
    str1=(url_text[0].split('/',1)[1]).split('\'',1)[0]
    #print(str1)
    base_url='https://www.jpl.nasa.gov/'
    # Construct the Featured Image url
    featured_image_url=base_url+str1
    #print(featured_image_url)


    # Visit twitter.com for Mars Weather
    ######################################
    url='https://twitter.com/marswxreport'
    browser.visit(url)
    time.sleep(2)
    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    slide=soup.find_all('li', class_="js-stream-item stream-item stream-item ")[0]
    #print(slide)

    #mars_weather
    mars_wx=slide.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text
    #print(mars_wx)

    wx_list=mars_wx.split()
    #print(wx_list)
    #len(wx_list)-1
    sum_str=''
    i=0
    for x in wx_list:    
        if i > 0 and i < (len(wx_list)-1):
            sum_str=sum_str+x+' '
        i=i+1    
    mars_weather=sum_str
    #print(mars_weather)

    # Visit space-facts.com for Mars Facts
    ########################################
    url='https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    slide=soup.find_all('table', id="tablepress-mars")[0]
    #print(slide)

    # Append Data for each row and row length is 9
    #td class="column-
    col1=[]
    col2=[]

    for x in range(9):    
        c1=slide.find_all('td', class_="column-1")[x].text
        c2=slide.find_all('td', class_="column-2")[x].text

        col1.append(c1)
        col2.append(c2)
        #print(c1,c2)

    #col_list=[col1,col2]
    df_mars=pd.DataFrame({"":col1,
                        "value":col2})
    #df=df_mars.reset_index(drop=True,inplace=False)
    #df_mars.head(10)

    #df.to_html('filename.html')
    df_mars.to_html('filename.html',index=False)

    #Visit astrogeology web for Mars Hemispheres
    ##############################################
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    slide=soup.find_all('div', class_="collapsible results")[0]
    #print(slide)

    title=[]
    img_url=[]
    for x in range(4):
        t1=(slide.find_all('h3')[x].text).split('Enhanced')[0]
        title.append(t1)
    #print(title)

    i=0
    for x in range(4):
        base_url='https://astrogeology.usgs.gov'
        ref=base_url+slide.find_all('a',class_="itemLink product-item")[i]['href']
        i+=1
        browser.visit(ref)
        html = browser.html
        time.sleep(2)
        soup = BeautifulSoup(html, 'html.parser')
        temp_slide=soup.find_all('a', target="_blank")[0]['href']
        img_url.append(temp_slide)
        i+=1
    #print(img_url)

    hemisphere_image_urls=[]
    for x in range(4):
        d1=dict({'title':title[x],'img_url':img_url[x]})
        hemisphere_image_urls.append(d1)
    #print(hemisphere_image_urls)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url":featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
