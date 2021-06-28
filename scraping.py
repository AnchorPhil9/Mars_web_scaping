#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
## Here, I used Splinter with Firefox (for personal reasons) following instructions from Splinter's documentation.
## Splinter Documentation: https://splinter.readthedocs.io/en/latest/drivers/firefox.html
## Aside from the different webdriver manager, executable path, and browser name, I nonetheless was able
## to run Module 10 code fine.
from webdriver_manager.firefox import GeckoDriverManager

## From here on out, we'll refactor alot of code work and formatting done in 10.3.6 (2021).
import pandas as pd
import datetime as dt

# In[2]:

def scrape_all():
    # Set the executable path and initialize Splinter
    executable_path = {'executable_path': GeckoDriverManager().install()}
    browser = Browser('firefox', **executable_path, headless=False)
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      ## We'll setup a dictionary entry for Mars' hemispheres.
      ## It'll contain the results of our later mars_hemis function.
      "hemispheres": hemisphere_image_urls
    }
    hemispheres = {}
    browser.quit()
    return data

def mars_news(browser):
    # ### Visit the NASA Mars News Site
    # In[3]:
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # In[4]:
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # In[5]:
        # In[6]:
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # In[7]:
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return new_title, news_p


# ### JPL Space Images Featured Image
# In[8]:
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # In[9]:
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # In[10]:
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # In[11]:
    # find the relative image url
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    # In[12]:
    except AttributeError:
        return None
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url


# ### Mars Facts
def mars_facts():
    # In[13]:
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.head()
    # In[14]:
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # In[15]:
    return df.to_html(classes="table table-striped")


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres
def mars_hemis():
    # In[16]:
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # In[17]:
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    search_soup = soup(html, 'html.parser')
        ## For brevity's sake, we will omit some code and comments detailing each step of our search to
        ## grab hemisphere images, including code that returns html results. We will keep references, however.
    # In[20]:
    browser.visit(url)
    # In[21]:
    mars_urls = []
    ## Backed by Soup documentation (2021), we plug in our "itemLink" class <a> tag parameters
    ## and we use append() to add each link we find to "mars_urls".
    ## Source: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    ## Key Phrase: "One common task"
    for link in search_soup.find_all('a', class_='itemLink product-item'):
        ## We'll add a try-except block to account for errors encountered.
        try:
            mars_urls.append(link.get('href'))
        except:
            print("URLs not found. Recheck the code")
        return mars_urls
    # In[22]:
    ## We do have surplus entries, but we can mitigate those with list slicing as mentioned by Geeks for Geeks (2021).
    ## Source: https://www.geeksforgeeks.org/python-list-slicing/
    clean_urls = mars_urls[0:8:2]
    for x in range (0, 4):
        browser.visit(f'https://marshemispheres.com/{clean_urls[x]}')
        html = browser.html
        search_soupX = soup(html, 'html.parser')
        hemispheres = {}
        ## On each page, we'll have Beautiful Soup look for 'img' instances and get a nearby 'src' link,
        ## similar to what we did for Mars news links in 10.3.4 (2021).
        try:
            hemis_url_find = search_soupX.find('img', class_='wide-image').get('src')
        except:
            print("Cannot find image. Check your html parsing setup and/or find() parameters.")
        return hemis_url_find
        ## We'll also get the "Hemisphere Enhanced" title of each page in 10.3.2 (2021) fashion.
        try:
            hemis_title_find = search_soupX.find('h2', class_='title').get_text()
        except:
            print("Cannot find title. Check your html parsing setup and/or find() parameters")
        return hemis_title_find
        hemispheres = {'img_url': f'https://marshemispheres.com/{hemis_url_find}', 'title': hemis_title_find}
        hemisphere_image_urls.append(hemispheres)
    return hemisphere_image_urls
    browser.quit()

if __name__ == "__main__":
    print(scrape_all)


