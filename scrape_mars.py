# Dependencies
import time
import re
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
from selenium import webdriver
import pymongo
from sys import platform


def init_Browser():
    executable_path = {"executable_path": "chromedriver"}

    browser = Browser("chrome", **executable_path, headless=True)
    return browser
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_Browser()

        #Scrape the NASA Mars News Site and collect News Title and the Paragraph Text.

        # Visit Nasa news url through splinter module
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html, "html.parser")


        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find("div", class_="content_title").find("a").text
        news_p = soup.find("div", class_="article_teaser_body").text

        # Dictionary entry from MARS NEWS
        mars_info["news_title"] = news_title
        mars_info["news_paragraph"] = news_p

        return mars_info

    finally:

        browser.quit()

#Feature Image
def scrape_mars_image():

    try:
        # Initialize browser 
        browser = init_Browser()

        # Visit Mars Space Images through splinter module
        image_url_featured = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url_featured)

        base_url = 'https://www.jpl.nasa.gov'

        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup2 = bs(html_image, "html.parser")

        pic = soup2.find('article', class_='carousel_item')
        first_part = pic['style'].split('\'')
        featured_image = (base_url + first_part[1])
        mars_info["featured"] = featured_image

        return mars_info

    finally:

        browser.quit()

#Mars Weather
def scrape_mars_weather():
    browser = init_Browser()

    #Visit Mars Weather Twitter and scrape latest weather tweet
    weather_url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    #Use Beautiful Soup to scrape the tweet
    html_weather = browser.html
    soup2 = bs(html_weather, "html.parser")
    mars_weather = soup2.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    # Find all elements that contain tweets
    for tweet in mars_weather: 
        #weather_tweet = tweet.find("p").text
        # weather_tweet = tweet.find("p").text

        if "Sol" and "pressure" in tweet.text:
            print(tweet.text)
            mars_info["weather_tweet"] = tweet.text
            break
        else: 
            pass

        # mars_info["weather_tweet"] = weather_tweet
    browser.quit()

    return mars_info

        # finally:

    

    #Mars Facts
def scrape_mars_facts():

    browser = init_Browser()
    #Visit Mars Facts webpage and use PANDAS to scrape the table containing Mars Facts
    hemispheres_url = "https://space-facts.com/mars/"

    #Use Pandas to read in the table
    mars_facts = pd.read_html(hemispheres_url)

    #Create a dataframe for the table
    mars_df = mars_facts[0]

    mars_df.columns = ["Mars Planet Attribute", "Attribute Value"]
    #Set the index for the table to the attribute
    mars_df.set_index("Mars Planet Attribute", inplace=True)
    
     # Save html code to folder Assets
    data = mars_df.to_html()
    # Dictionary entry from MARS FACTS
    mars_info["mars_facts"] = data

    return mars_info

# MARS HEMISPHERES

def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_Browser()

        # Visit hemispheres website
        hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_hemispheres, "html.parser")

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all("div", class_="item")

        # Create empty list for hemisphere urls 
        hiu = []

        # Store the main_ul 
        hemispheres_main_url = "https://astrogeology.usgs.gov" 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find("h3").text
            
            # Store link that leads to full image website
            partial_img_url = i.find("a", class_="itemLink product-item")["href"]
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = bs( partial_img_html, "html.parser")
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find("img", class_="wide-image")["src"]
            
            # Append the retreived information into a list of dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info["hiu"] = hiu

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()