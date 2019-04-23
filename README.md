
# Mars NASA Data Mining
---
This script includes prototype code for mining data from NASA regarding their mars mission.


```python
# Dependencies

# Web scraping dependencies
from bs4 import BeautifulSoup

# Asynchronous scraping dependencies
import time
from selenium import webdriver
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
```

# Scrape Latest News


```python
# Create soup object
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
# Chromedriver set-up
executable_path = {'executable_path': 'chromedriver.exe'}
browser = webdriver.Chrome(**executable_path)
browser.get(url)

# 2 second time delay is so that the page can load and all information can be scraped
time.sleep(2)

# Scrape the html on the site after the timer is done
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# find the first div class that contains news information 
# (this will be the latest news for the website)
latest_news_class = soup.find("div", class_ = "list_text")

# close the browser
browser.close()
```


```python
# Loop through returned results
result_list = []
for result in latest_news_class:
    # Error handling
    try:
        # Identify and return title of listing
        text_result = result.text
        
        # append to the result list if the attribute exists
        if (text_result):
            result_list.append(text_result)
    except AttributeError as e:
        print(e)

result_list
```




    ['April 23, 2019',
     "NASA's InSight Detects First Likely 'Quake' on Mars",
     'While their causes are still unknown, one of three shaking events looks a lot like the quakes detected on the Moon by the Apollo missions.']



# Scrape Image of the Day


```python
url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

# Create browser object from Splinter library
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url2)

# Click on the button that says FULL IMAGE to scrape the image
browser.click_link_by_partial_text('FULL IMAGE')

# Pause to let the browser load
time.sleep(2)

# Load html
html = browser.html

# Close the browser
browser.quit()

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')
link = soup.find("div", class_ = "fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open")
```


```python
for result in link:
    try:
        # collect the partial URL
        partial_url = result.get('src')
        # if the partial URL exists, create the full URL
        if(partial_url):
            featured_image_url = "https://www.jpl.nasa.gov" + partial_url
    except AttributeError as e:
        print(e)

featured_image_url
```




    'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA14317_ip.jpg'



# Scrape latest mars weather tweet


```python
url3 = "https://twitter.com/marswxreport?lang=en"

# Create browser object from Splinter library
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url3)

# Pause to let the browser load
time.sleep(2)

# Load html
html = browser.html

# Close the browser
browser.quit()

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')
tweet_box = soup.find("div", class_ = "js-tweet-text-container")
```


```python
# Loop through the tweet_box's HTML elements
for element in tweet_box:
    try:
        # store the tweet in a variable
        tweet = element.text
        # if the tweet exists, then assign it to eh variable "mars_weather"
        if(tweet):
            mars_weather = tweet
    # Print to terminal if the attribute does not exist
    except AttributeError as e:
        print(e)

# clean newlines and show in JN
mars_weather = mars_weather.replace("\n", " ")
mars_weather
```

    'NavigableString' object has no attribute 'text'
    'NavigableString' object has no attribute 'text'
    




    'Mars, I hear you. I’ve detected some quiet but distinct shaking on #Mars. The faint rumbles appear to have come from the inside of the planet, and are still being studied by my team. Take a listen.http://go.nasa.gov/2GCEBtm\xa0pic.twitter.com/Z8Hn03jigO'



# Scrape mars data


```python
# Scrape data in a tabular form using pandas
import pandas as pd
url = "https://space-facts.com/mars/"
tables = pd.read_html(url , encoding= "utf-8")
mars_data_df = tables[0]
```


```python
# Clean up dataframe columns and index
mars_data_df.columns = ['Description','Value']
mars_data_df.set_index('Description', inplace=True)

# output to JN
mars_data_df

# save the dataframe to an html table
html_table = mars_data_df.to_html()
```

# Scrape Hemisphere Images


```python
# Initialize hemispehre list and chromedriver
hemisphere_images_list = []
url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url4)

# Click on the hemisphere link to open the html of the high quality image
browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
# Load the html, parse for the image, and store the image in the "link" variable
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
picture_url = soup.find('div', class_="downloads")
link = picture_url.a['href']
# create 
link_dict = {"title": "Cerberus Hemisphere", "img_url": link}
hemisphere_images_list.append(link_dict)
# go back to previous page
browser.back()

# Click on the hemisphere link to open the html of the high quality image
browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
# Load the html, parse for the image, and store the image in the "link" variable
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
picture_url = soup.find('div', class_="downloads")
# create containers from the scraped information
link = picture_url.a['href']
link_dict = {"title": "Schiaparelli Hemisphere", "img_url": link}
hemisphere_images_list.append(link_dict)
# go back to previous page
browser.back()


# Click on the hemisphere link to open the html of the high quality image
browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
# Load the html, parse for the image, and store the image in the "link" variable
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
picture_url = soup.find('div', class_="downloads")
link = picture_url.a['href']
# create containers from the scraped information
link_dict = {"title": "Syrtis Major Hemisphere", "img_url": link}
hemisphere_images_list.append(link_dict)
# go back to previous page
browser.back()

# Click on the hemisphere link to open the html of the high quality image
browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
# Load the html, parse for the image, and store the image in the "link" variable
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
picture_url = soup.find('div', class_="downloads")
link = picture_url.a['href']
# create containers from the scraped information
link_dict = {"title": "Valles Marineris Hemisphere", "img_url": link}
hemisphere_images_list.append(link_dict)
# close the browser
browser.quit()

# Output final list to JN window
print(hemisphere_images_list)
```

    [{'title': 'Cerberus Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': 'Schiaparelli Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': 'Syrtis Major Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, {'title': 'Valles Marineris Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]
    
