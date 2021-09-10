##################################################
#                                                #
#             DeepL Translate Script             #
#                                                #
#       Hacked together by BoredManPlays         #
#                                                #
##################################################

import clipboard
from selenium import webdriver
import time

text_to_translate = 'Oh salut, voici un exemple de texte pour tester mon script python de traduction.'
driver_path='./chromedriver'
driver = webdriver.Chrome(driver_path)
deepl_url = 'https://www.deepl.com/translator/en'
driver.get(deepl_url)

input_css = 'div.lmt__inner_textarea_container textarea'
input_area = driver.find_element_by_css_selector(input_css)
input_area.clear()
input_area.send_keys(text_to_translate)
time.sleep(6)
output_button_xpath = '/html/body/div[2]/div[1]/div[4]/div[4]/div[3]/div[1]/div[2]/div[1]/button'
output_button = driver.find_element_by_xpath(output_button_xpath)
output_button.click()
time.sleep(2)
english_button_xpath = '/html/body/div[2]/div[1]/div[4]/div[4]/div[3]/div[1]/div[2]/div[1]/div[2]/button[6]'
english_button = driver.find_element_by_xpath(output_button_xpath)
english_button.click()
button_css = ' div.lmt__target_toolbar__copy button'
button = driver.find_element_by_css_selector(button_css)
button.click()
content = clipboard.paste()
driver.quit()

print('_'*50)
print('Original    :', text_to_translate)
print('Translation :', content)
print('_'*50)