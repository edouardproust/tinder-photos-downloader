# BeutifullSoup scrapping: https://www.makeuseof.com/beautiful-soup-tutorial/
 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
import requests
import codecs
import config as c


def get_photos_urls(userId, photos_dimensions):

    photos_urls = []

    # Prevent Selenium to open browser window
    options = Options()
    options.headless = True
    # Use Selenium to enable JS support while scrapping
    driver = webdriver.Firefox(options=options)
    # Open url with Selenium
    try:
        driver.get(c.TINDER_PROFILE_BASE_URL + userId)
        # Click on carousel buttons to load photos
        carousel_btns = driver.find_elements(By.TAG_NAME, "button")
        for btn in carousel_btns:
            classes = btn.get_attribute('class')
            if ('bullet' in classes):
                btn.click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as e:
        return error_msg(exception=e)
    
    # Writing page source code to a HTML file (for debug)
    with open("data/bf4/profile.htm", "w") as file:
        file.write(soup.prettify())

    # Extract photos urls
    data_scripts = []
    for script in soup.find_all('script'):
        script_str = script.get_text()
        if 'window.__data' in script_str:
            data_scripts.append(script_str)

    if len(data_scripts) < 1:
            return error_msg()
    else:
        for script_str in data_scripts:
            matches = re.findall('"url":"(.+?)"', script_str)
            if(len(matches) < 1):
                return error_msg(ref='user_id')
            else:
                for url in matches:
                    if (photos_dimensions + '_') in url:
                        url = codecs.decode(url, 'unicode-escape')
                        photos_urls.append(url)
    return {
        "result": "success",
        "photos": photos_urls
    }


def error_msg(ref = None, exception = None):
    msg = None
    msg_default = f"An error occured. Please contact <a href='mailto:{c.AUTHOR_EMAIL}'>webmaster</a>"
    if exception:
        dir(exception)
        if exception.msg:
            msg = f"{msg_default} with the following message: <i>{requests.utils.unquote(exception.msg)}</i>"
        else:
            msg = msg = msg_default + '.'
    elif ref == "user_id":
        msg = "The person you're looking for was not found. Please verify that you entered a correct user ID."
    else:
        msg = msg_default + '.'
    
    return {
        "result": "error",
        "msg": msg
    }