from splinter import Browser
from bs4 import BeautifulSoup as bs
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

   



    # Store data in a dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict
