import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = r"C:\Users\James\Desktop\chromedriver.exe"
driver = webdriver.Chrome(executable_path=PATH)

FOODS = {}

def head_line_macro_finder(list_item):
    list_item = list_item.text.split('\n')
    #macro name, macro value
    return list_item[-1].split(':')[0], list_item[0]

def lower_table_macro_finder(list_item):
    list_item = list_item.text.split('\n')
    #macro name, macro value
    return list_item[0], list_item[2]

#Go to site
driver.get("https://www.mcdonalds.com/gb/en-gb/good-to-know/nutrition-calculator.html")
time.sleep(5)
try:
    driver.find_element_by_class_name('cookie-message-close').click()
except:
    pass

categories = driver.find_element_by_id("level-all")
buttons = categories.find_elements_by_tag_name('button')
number_of_buttons = len(buttons)

for i in range(number_of_buttons):
    categories = driver.find_element_by_id("level-all")
    buttons = categories.find_elements_by_tag_name('button')
    buttons[i].click()
    time.sleep(5)
    food_items = driver.find_element_by_id("level-category")\
                    .find_elements_by_tag_name('img')
    number_of_food_items = len(food_items)
    
    for j in range(number_of_food_items-1):
        food_items[j].click()
        time.sleep(5)
        try:
            driver.find_element_by_class_name("_hj-f5b2a1eb-9b07_widget_open_close").click()
        except Exception as e:
            pass
        food_name = driver.find_element_by_class_name("meal-item")\
                    .text.split('\n')[1]
        FOODS[food_name]= {}
        table = driver.find_element_by_class_name("my-meal")
        lines = table.find_elements_by_tag_name('li')
        lower_lines = table.find_elements_by_tag_name('tr')
        
        for line in lines[:6]:
            macro, value = head_line_macro_finder(line)
            FOODS[food_name][macro] = value
            
        for line in lower_lines: 
            if line.text != '' and \
                line.text != 'Nutritional Information Per Portion % RI (Adult)':
                try:
                    macro, value = lower_table_macro_finder(line)
                    FOODS[food_name][macro] = value
                except Exception as e:
                    print(e)
                    pass
            
        driver.get("https://www.mcdonalds.com/gb/en-gb/good-to-know/nutrition-calculator.html")
        time.sleep(5)
        try:
            driver.find_element_by_class_name("_hj-f5b2a1eb-9b07_widget_open_close").click()
        except Exception as e:
            pass
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        try:
            driver.find_element_by_class_name('cookie-message-close').click()
        except:
            pass
        categories = driver.find_element_by_id("level-all")
        buttons = categories.find_elements_by_tag_name('button')
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(3)
        buttons[i].click()
        time.sleep(5)
        try:
            driver.find_element_by_class_name("_hj-f5b2a1eb-9b07_widget_open_close").click()
        except Exception as e:
            pass
        food_items = driver.find_element_by_id("level-category")\
                    .find_elements_by_tag_name('img')
    driver.get("https://www.mcdonalds.com/gb/en-gb/good-to-know/nutrition-calculator.html")
    time.sleep(5)

foods_df = pd.DataFrame(FOODS).T

foods_df.to_csv(r".\McDonalds_Scraped.csv")