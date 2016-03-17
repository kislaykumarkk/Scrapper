from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BS
import sys
import os
import pdfkit


roll = 10400212001
i = 151 # do it 2 times



while i > 0:
    driver = webdriver.Chrome('/Users/Kislay/Desktop/chromedriver')
    driver.get("http://www.wbutech.net/result_odd1516.php")

    def find_by_xpath(locator):
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, locator))
        )

        return element

    class FormPage(object):
        def fill_form(self, roll):
            find_by_xpath('//input[@name = "rollno"]').send_keys(roll)
            

            return self # makes it so you can call .submit() after calling this function

        def submit(self):
            driver.find_element_by_name("sem7").click()

        def save(self):
            '''driver.find_element_by_name("SGPA")
            print'''

    roll = roll+1

    '''data = {
        
        #roll = roll+1
        'rollno': roll
        print roll
        
    }'''


    FormPage().fill_form(roll).submit()    #driver.find_element_by_name("sem7").click()
    soup = BS(driver.page_source)

    path = '/Users/Kislay/Desktop/Result/' + str(roll) +'.html'

    
    with open(path, 'w') as f:
        for line in soup.prettify('utf-8',):
            f.write(str(line))

    out = '/Users/Kislay/Desktop/Result/' + str(roll) + '.pdf'

    pdfkit.from_file(path, out)

    driver.quit() # closes the webbrowser
    
    os.remove(path)

    i = i - 1