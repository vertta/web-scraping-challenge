# imports
# Import splinter, Pandas and beautiful soup
#import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup

import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# -------scrape all function---------
def scrape_all():
    print("Testing that the function is active")
    #setup splinter 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser=Browser('chrome', **executable_path, headless = False)
# scrape the mars news page and return in json so to load into Mongodb

# get information from the news page 
    news_title, news_paragraph = scrape_news(browser)
    # build the dictionary using the information from the scrapes
    marsData = { 
        "newsTitle" : news_title,
        "newsParagraph": news_paragraph,
        "featuredImage" : scrape_feature_img(browser),
        "facts": scrape_fact_page(browser),
        "hemispheres": scrape_hemisphere_pages(browser),
        "lastModifiedDate": dt.datetime.now()
    }




    # stop web browser
    browser.quit()
    #display output
    return marsData

#-------- scrape the mars news page--------
def scrape_news(browser):
    # go to the mars NASA news site
    url='https://redplanetscience.com/'
    browser.visit(url)
    # delay to wait for page to load
    browser.is_element_present_by_css('div.list_text', wait_time=2)
# convert the HTML information in the broswer to a soup object and print parsed information to verify information 
    html=browser.html
    news_soup = soup(html, 'html.parser')
    #display the title content by find the div tag and assign the value to variable 'news_title'
    slide_elem = news_soup.select_one ('div.list_text')
    # get the title from the text
    news_title=slide_elem.find('div', class_ = 'content_title').get_text()
    
    #get the paragraph for the headline
    news_paragraph=slide_elem.find('div', class_ = 'article_teaser_body').get_text()

    #return news title and paragraph
    return news_title, news_paragraph

#--------scrape through the feature image page ------
#visit the URL for the spae image 
def scrape_feature_img(browser):
    url='https://spaceimages-mars.com'
    browser.visit(url)
    # code to find and click the full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    #Parse the resulting html with soup 
    html= browser.html
    img_soup = soup(html, 'html.parser')

    # find the relative image url 
    img_url_rel = img_soup.find('img', class_= 'fancybox-image').get('src')

    #use base url to render absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    #return image url
    return img_url

#------scrape through the fast page---------
def scrape_fact_page(browser):
     url='https://galaxyfacts-mars.com'
     browser.visit(url)

     #Parse the results for html with soup 
     html = browser.html
     fact_soup = soup(html, 'html.parser')

     # find the fact location 
     factsLocation = fact_soup.find('div', class_="diagram mt-4")
     factTable = factsLocation.find('table')
#initialize string and add text then return the values 
     facts = ""
     facts += str(factTable)  # add text to string
     return facts          # return information in string



# --------scrape through the hemispheres pages------_
def scrape_hemisphere_pages(browser):
    #visit the url for hemisphere information
    url='https://marshemispheres.com/'
    browser.visit(url)

    # build list of image URLs
    #create a list to hold the images and titles 
    hemisphere_image_urls = []

#loop through these links, click the link, find the same anchor, return the href 
    #for i in range(len(links)):
    for i in range(4) :
        hemisphereInfo = {}  #initialize the array to hold hemisphere information 
        browser.find_by_css('a.product-item img')[i].click() # find the elements on each loop to avad a stale element exception error
        sample = browser.links.find_by_text('Sample').first # Find the same image anchor tag and extract the href information
        hemisphereInfo["img_url"] = sample ['href'] 
        hemisphereInfo['title']  = browser.find_by_css('h2.title').text #Get Hemisphere title
        hemisphere_image_urls.append(hemisphereInfo) #Append hemisphere object to list 
        browser.back() # Navigate backward

    return hemisphere_image_urls   # return hemisphere URLs with titles 
# set up as a flash app to run standalone

if __name__ == "__main__":
    print(scrape_all())