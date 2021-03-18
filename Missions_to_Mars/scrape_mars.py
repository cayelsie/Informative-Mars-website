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

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    astro_soup = bs(html, 'html.parser')

    #Setting variables for the page main url and also an empty list to house the dictionaries at the end
    main_url = 'https://astrogeology.usgs.gov/'
    hemisphere_image_urls = []

    #Use a tag that will create an iterable list of ALL items desired
    astro_item = astro_soup.find_all('div', class_ = 'item')

    #Look through the soup object
    for item in astro_item:
    
        #Get a parent div above each item desired and then store the href line that will help take us to the desired image page
        div = item.find('div', class_='description')
        href=div.a['href']
    
        #concatenate the main page url with the desired href
        hemi_url = (main_url + href)
    
        #Get the hemisphere name
        name = div.find('h3').text
    
        #Remove the word 'enhanced'
        hem_name = name.rsplit(' ', 1)[0]

        #Browser accesses the correct page for each hemisphere
        browser.visit(hemi_url)
        
        #Get the html code for each page
        html = browser.html
        
        #Crate a soup object for each page
        img_soup = bs(html, 'html.parser')
        
        #Search for the images with the img tag
        img_tag = img_soup.find('img', class_='wide-image')
            
        #Extract the image src for each
        img = img_tag['src']
        
        #Concatenate the main page url with the desired href
        img_url = (main_url + img)

        #Create a list of dictionaries
        hemisphere_dict = {}
        hemisphere_dict['title'] = hem_name
        hemisphere_dict['img_url'] = img_url
        hemisphere_image_urls.append(hemisphere_dict)
   



    # Store data in a dictionary
    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_mars_image": featured_image_url,
        "mars_facts": mars_facts
        "hemispheres": hemisphere_image_urls     
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict
