from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import time


def get_screenshot(identifier, link):
    chrome_options = Options()
    chrome_options.add_argument("headless")
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    chrome.get(link)
    time.sleep(1)
    element = chrome.find_element_by_id(identifier)
    location = element.location
    size = element.size
    png = chrome.get_screenshot_as_png()
    chrome.quit()

    im = Image.open(BytesIO(png))

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    
    im = im.crop((left, top, right, bottom))
    im.save('Videos/screenshot.png')
