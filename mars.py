# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

# Create scrape function with mission_to_mars code
def scrape():
    # Set up executable path to browser with webdriver_manager
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Navigate to Mars News page
    browser.visit('https://redplanetscience.com/')
    # Create HTML object
    html = browser.html
    # Create BS object, parse with html.parser
    page = bs(html, 'html.parser')
    # Find News Title (class = content_title), assign to variable
    news_title = page.find('div', class_='content_title').text
    # Find Paragraph Text (class = article_teaser_body), assign to variable
    news_p = page.find('div', class_='article_teaser_body').text

    # Navigate to Featured Space Image page
    browser.visit('https://spaceimages-mars.com/')
    # Create HTML object
    html = browser.html
    # Create BS object, parse with html.parser
    page = bs(html, 'html.parser')
    # Find current Featured Mars Image (class = headerimage), assign to variable
    images = page.find('img', class_='headerimage fade-in')['src']
    featured_image_url = f'https://spaceimages-mars.com/{images}'

    # Use pd.read_html to scrape the tables from the Mars Facts webpage into a "tables" variable
    tables = pd.read_html("https://galaxyfacts-mars.com/", header=0)
    # Set the first table into a DF 
    mars_facts_df = tables[0]
    mars_facts_df.set_index("Mars - Earth Comparison", inplace=True) 
    # Use .to_html() to convert DF to html table string
    mars_facts_html = mars_facts_df.to_html()
    mars_facts_html

    # Navigate to Astrogeology page
    browser.visit('https://marshemispheres.com/')
    # Create HTML object
    html = browser.html
    # Create BS object, parse with html.parser
    page = bs(html, 'html.parser')
    # Locate each of the four hemisphere sections in the html 
    locations = page.find_all("div", class_="description")
    # Create empty list to hold the img_url/title dictionaries
    hemisphere_urls_titles_list = []
    # Run through the html section locations for each hemisphere...
    for location in locations:
        # Find the link to the full res image
        img_link = location.find('a')['href']
        # Navigate to the page for full res image, create BS object to parse through
        browser.visit('https://marshemispheres.com/' + img_link)
        html = browser.html
        page = bs(html, 'html.parser')
        # Find the image source link (img section, class 'wide-image', save full img_url
        img_src = page.find("img", class_='wide-image')["src"]
        img_url = 'https://marshemispheres.com/' + img_src
        # Find the title for the image (h2 within the div section, class 'cover')
        # --strip the h2 text, split off the last word with rsplit(), save the hemisphere title
        hemisphere_title = page.find("div", class_="cover").find('h2').text.strip().rsplit(' ', 1)[0] 
        # Create the hemisphere dictionary (title: ... , img_url: ...), append to dictionary list
        hemisphere_dict = {'title': hemisphere_title, 'img_url': img_url}
        hemisphere_urls_titles_list.append(hemisphere_dict)
        
    # Store all scraped data into a dictionary
    scraped_mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts_html": mars_facts_html,
        "hemisphere_urls_titles_list": hemisphere_urls_titles_list
    }

    # Exit browser
    browser.quit()

    # Return scraped data
    return scraped_mars_data