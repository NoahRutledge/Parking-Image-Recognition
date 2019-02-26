from selenium import webdriver
from PIL import Image
from io import BytesIO

chrome = webdriver.Chrome()
chrome.get('https://www.youtube.com/watch?v=PmrWwYTlAVQ&feature=player_embedded')

element = chrome.find_element_by_id('player')
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
