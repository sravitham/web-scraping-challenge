# imports
import splinter
import requests
import pandas as pd
from splinter import Browser, browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager    

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Create a dict to store 
    mars_data = {}

    # Mars news and Scrape page into Soup
    mars_url = 'https://redplanetscience.com/'
    browser.visit(mars_url)

    html = browser.html   
    mars_soup = bs(html, "html.parser")
    news_title= mars_soup.find_all('div', class_='content_title')[0].text
    news_date= mars_soup.find_all('div', class_='list_date')[0].text 
    news_p= mars_soup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    html = browser.html
    img_soup = bs(html, "html.parser")
    relative_image_path=img_soup.find_all('img', class_='headerimage fade-in')[0]["src"]
    featured_image_url= (f'{jpl_url}{relative_image_path}')
 
    # tables
    facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(facts_url)
    html = browser.html
    facts_soup = bs(html, "html.parser")
    tables = pd.read_html(facts_url)
    mars_facts=tables[0]
    mars_facts.columns= ["Mars - Earth Comparison","Mars","Earth"]
    mars_facts.drop(index=mars_facts.index[0], axis=0,inplace=True)
    mars_facts.set_index('Mars - Earth Comparison')
    facts_html=mars_facts.to_html()
    facts_html.replace('\n','')

    # hemispheres
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    html = browser.html
    hemi_soup = bs(html, "html.parser")
    mars_hemi=hemi_soup.find_all('div', class_='item')
    hemi_href=[]
    for row in mars_hemi:
        hemi_href.append(hemi_url+ (row.find('a', class_='itemLink product-item')['href']))
    # Create empty list
    hemi_img_urls = []
    # for loop to get title and image link
    for url in hemi_href:
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2', class_ = 'title').text
        par_url=soup.find('img', class_ = 'wide-image')['src']
        img_url = hemi_url + par_url
        hemi_img_urls.append({'title': title, 'img_url': img_url})

    mars_data = {
    "news_title": news_title,
    "news_date": news_date,
    "news_p":news_p,
    "featured_image_url": featured_image_url, 
    "mars_facts":facts_html, 
    "mars_hemi": hemi_img_urls

    }

    browser.quit()
    return mars_data