from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BS
import sys
import os
import pdfkit

#Starting Roll No.
roll = 10400212001

#No of iterations
i = 151



while i > 0:
    #Chrome driver to open Browser
    #Donload from https://sites.google.com/a/chromium.org/chromedriver/downloads
    #Add correct path for ChromeDriver here
    driver = webdriver.Chrome('/Users/Kislay/Desktop/chromedriver')
    
    #URL of the website to Scrap
    driver.get("http://www.wbutech.net/result_odd1516.php")

    def find_by_xpath(locator):
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, locator))
        )

        return element

    class FormPage(object):
        def fill_form(self, roll):
            #Find Form field to enter the roll no
            find_by_xpath('//input[@name = "rollno"]').send_keys(roll)
            
            return self # makes it so you can call .submit() after calling this function

        def submit(self):
            #Click Javascript button
            #Change value for diff semester
            driver.find_element_by_name("sem7").click()


    roll = roll+1


    FormPage().fill_form(roll).submit()
    
    #Parse HTML source using BeautifulSoup
    soup = BS(driver.page_source)


    #Path to store the HTML files
    path = '/Users/Kislay/Desktop/Result/' + str(roll) +'.html'

    
    with open(path, 'w') as f:
        for line in soup.prettify('utf-8',):
            f.write(str(line))

    #Path to store the output PDF file
    out = '/Users/Kislay/Desktop/Result/' + str(roll) + '.pdf'

    #Output as PDF
    pdfkit.from_file(path, out)

    driver.quit() # closes the webbrowser
    
    os.remove(path)

    i = i - 1
