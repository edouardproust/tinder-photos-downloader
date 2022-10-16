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
    driver.set_page_load_timeout(99);
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
        return {"alert": alert(exception=e)}

    # Extract photos urls
    data_scripts = []
    for script in soup.find_all('script'):
        script_str = script.get_text()
        if 'window.__data' in script_str:
            data_scripts.append(script_str)
    if len(data_scripts) < 1:
            return {"alert": alert()}
    else:
        for script_str in data_scripts:
            urls = re.findall('"url":"(.+?)"', script_str)
            if(len(urls) < 1):
                return {"alert": alert(ref='user_id')}
            else:
                for url in urls:
                    if (photos_dimensions + '_') in url:
                        photos_urls.append(codecs.decode(url, 'unicode-escape'))

    if len(photos_urls) < 1:
        return {
            "alert": alert(ref="format"),
            "photos": get_largest_photos(urls)
        }
    return {
        "photos": photos_urls
    }


def get_largest_photos(urls):
    # Get highest width
    widths = []
    for url in urls:
        width = re.search('(.+?)x', url.split("\\u002F")[-1])
        if width:
            width = int(width.group(1))
        if width and not width in widths:
            widths.append(width)
    highest = max(widths)
    # Get url for the highes
    widths = []
    selection = []
    for url in urls:
        if str(highest) in url:
            selection.append(codecs.decode(url, 'unicode-escape'))
    return selection


def alert(ref = None, exception = None):
    alert_default = f"An error occured. Please contact <a href='mailto:{c.AUTHOR_EMAIL}'>webmaster</a>"
    if exception:
        dir(exception)
        if exception.msg:
            return f"{alert_default} with the following message: <i>{requests.utils.unquote(exception.msg)}</i>"
        else:
            return alert_default + '.'
    elif ref == "user_id":
        return "The person you're looking for was not found. Please verify that you entered a correct user ID."
    elif ref == "format":
        return "No photos with the requested dimensions. We retreived the largest ones."
    else:
        return alert_default + '.'