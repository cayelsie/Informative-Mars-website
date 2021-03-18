from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit NASA Mars url
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)

    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    nasa_soup = bs(html, 'html.parser')

    #Search original soup object to find a parent tag to extract info
    nasa = nasa_soup.find('ul', class_='item_list')

    #Extract & store the headline title
    news_title = nasa.find('div', class_='content_title').text

    #Extract & store the paragraph
    news_p= nasa.find('div', class_='article_teaser_body').text

    ##################################################################
    #Visit JPL url
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)

    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html.parser'
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    #Get a tag containing featured Mars image
    items = jpl_soup.find('a', class_='showimg fancybox-thumbs')

    #Select the full image href
    href = items['href']

    #Save the full url for the image in a variable    
    featured_image_url = ('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href)
    ###################################################################################
    #Visit Space Facts url using pandas and store the table data
    mars_url = 'https://space-facts.com/mars/'
    mars_tables = pd.read_html(mars_url)

    #Get the first table of Mars facts and set as a variable
    mars_df = mars_tables[0]

    #Set column names
    mars_df.columns = ['Description', 'Mars']

    #Convert to html
    mars_facts = mars_df.to_html(index = False)
    ##################################################################################

    #Visit Astrogeology url
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)



    # Store data in a dictionary
    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_mars_image": featured_image_url,
        "mars_facts": mars_facts
        
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict
