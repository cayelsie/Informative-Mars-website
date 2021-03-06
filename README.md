The aim of this project was to create a web application that scrapes several websites for information about Mars and displays all of that information in one HTML page. Referenced files can be found in the Missions_to_Mars folder.

Initial web scraping was performed using a Jupyter Notebook, BeautifulSoup, Pandas and Requests/Splinter. Items scraped include: the latest news title and paragraph from The NASA Mars News Site (https://mars.nasa.gov/news/), the featured Mars image at the Jet Propulsion Laboratory site (https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html), a Mars facts table from Space Facts (https://space-facts.com/mars/), and high resolution images of the hemispheres of Mars from the USGS Astrogeology site (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars). The jupyter notebook is found at mission_to_mars.ipynb. 

MongoDB and Flask were used to create a single HTML page that displays all of the scraped information. scrape_mars.py contains a function that will execute the scraping, as well as the code to store the scraped information in a dictionary. The flask application (app.py) contains the code that will import and call the scrape function and store the returns into MongoDB. Additionally, it contains a route that will query the MongoDB and pass the stored scraped data into an HTML template for display. Thetemplates folder contains the index.html file, the HTML template. The static folder contains the style.css file for styling the display.

The images folder contains screenshots of the final website as well as a screenshot of the scraped data housed within MongoDB.

![](Missions_to_Mars/images/Top_of_page.PNG)

![](Missions_to_Mars/images/Middle_of_page.PNG)

![](Missions_to_Mars/images/Bottom_of_page.PNG)

![](Missions_to_Mars/images/MongoDB_screenshot.PNG)
