from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

# initializes chromedriver
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# returns the content of the latest tweet
def scrape_latest_news():
    # initialize browser
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser = init_browser()
    browser.visit(url)
    # 2 second time delay is so that the page can load and all information can be scraped
    time.sleep(2)
    # Scrape the html on the site after the timer is done
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # find the first div class that contains news information 
    # (this will be the latest news for the website)
    latest_news_class = soup.find("div", class_ = "list_text")
    # close the browser
    browser.quit() 
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
    # return the list of news information (date, title, description)
    return result_list

# returns the url of the image of the day
def scrape_image_of_the_day():
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # Create browser object from Splinter library
    browser = init_browser()
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
    # Collect url from link
    for result in link:
        try:
            # collect the partial URL
            partial_url = result.get('src')
            # if the partial URL exists, create the full URL
            if(partial_url):
                featured_image_url = "https://www.jpl.nasa.gov" + partial_url
        except AttributeError as e:
            print(e)
    return featured_image_url

# returns body of the latest nasa mars tweet
def scrape_latest_tweet():
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser = init_browser()
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
    return mars_weather

# returns an html table of mars facts 
def scrape_mars_data():
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url , encoding= "utf-8")
    mars_data_df = tables[0]
    # Clean up dataframe columns and index
    mars_data_df.columns = ['Description','Value']
    mars_data_df.set_index('Description', inplace=True)
    
    # convert the dataframe to html and remove extra newlines
    html_table = mars_data_df.to_html()
    
    return html_table


# returns a dictionary of decriptions and image urls
def scrape_hemisphere_images():
    # Initialize hemispehre list and chromedriver
    hemisphere_images_list = []
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser = init_browser()
    browser.visit(url)
    # Click on the hemisphere link to open the html of the high quality image
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    # Load the html, parse for the image, and store the image in the "link" variable
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    picture_url = soup.find('div', class_="downloads")
    link = picture_url.a['href']
    # create containers for site info
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

    # return the list of dictionaries
    return hemisphere_images_list

# Main scrape function.  Calls all the previous scrape functions
# returns the data in a dictionary format that will be uploaded to mongodb
def scrape():
    # Scrape the latest news tweet
    latest_news = scrape_latest_news()

    # Scrape the url for the image of the day
    image_of_day_url = scrape_image_of_the_day()

    # Scrape the latest tweet
    latest_tweet = scrape_latest_tweet()

    # scrape table data
    html_table = scrape_mars_data()

    # Scrape the links to the hemispheres of mars
    image_of_hemispehres_list_dict = scrape_hemisphere_images()

    # create a dictionary that will be used for the mongodb database
    mars_data_dict = { 
        "news_title" : latest_news[1],
        "news_p" : latest_news[2],
        "featured_image_url" : image_of_day_url,
        "mars_weather" : latest_tweet,
        "mars_facts_html" : html_table,
        "hemispheres" : image_of_hemispehres_list_dict
    }

    return mars_data_dict

    






