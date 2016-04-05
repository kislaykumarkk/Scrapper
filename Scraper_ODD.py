from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BS
import csv
import sys
import os
import pdfkit

# The data Entry and Populate Section
roll_list = []   #Blank Roll List
initial_roll = 10400212001   #Enter the starting Roll Number of General Students
count = 135		     #Enter the approx count of students
while count > 0:
	roll_list.append(initial_roll)    #Populate List
	initial_roll = initial_roll + 1
	count = count -1

lateral_roll = 10400213122   #Enter the starting Roll Number of Lateral Students
count = 25		     #Enter the approx count of students
while count > 0:
	roll_list.append(lateral_roll)    #Populate List
	lateral_roll = lateral_roll + 1
	count = count -1

# End of Data Entry And Populate Section

csvout = csv.writer(open("results.csv", "w"))
csvout.writerow(("Roll","Name","SGPA"))


for roll in roll_list:
	#Chrome driver to open Browser
	#Donload from https://sites.google.com/a/chromium.org/chromedriver/downloads
	#Add correct path for ChromeDriver here
	driver = webdriver.Chrome('/home/kaustav/chromedriver')
    
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
			with myWait(driver):
				driver.find_element_by_name("sem7").click()



	class myWait(object):
		def __init__(self, driver):
			self.driver = driver

		def __enter__(self):
			pass

		def __exit__(self, *_):
			element = WebDriverWait(driver, 10).until(
			    EC.presence_of_element_located((By.TAG_NAME, "html"))
			)




	FormPage().fill_form(roll).submit()
    
	#Parse HTML source using BeautifulSoup
	soup = BS(driver.page_source)


	#Path to store the HTML files
	path = '/home/kaustav/Result/' + str(roll) +'.html'
	
	#Fetching the tables
	name = ""
	roll_no = ""
	sgpa = 0.0
	soup4tables=soup.find_all('table')
	for tab in soup4tables:
		soup4rows=tab.find_all('tr')
		if(len(soup4rows) ==3):
			str1 = str(soup4rows[1])
			name = str1[((str1.index("Name :"))+7):str1.index("</th>\n<th style=")].strip()
			roll_no1 = str1[((str1.index("Roll No. :"))+11):str1.index("</th>\n</tr>")].strip()
			roll_no = long(roll_no1)
		soup4rows=tab.find_all('tr')
		if(len(soup4rows) ==2):
			str1 = str(soup4rows[0])
			str2 = str1[((str1.index("SEMESTER :"))+10):str1.index("</td>")].strip()
			sgpa = float(str2)
	csvout.writerow((roll_no,name,sgpa))
		
	
	with open(path, 'w') as f:
		for line in soup.prettify('utf-8',):
			f.write(str(line))
	'''
	#Path to store the output PDF file
	out = '/home/kaustav/Result/' + str(roll) + '.pdf'

	#Output as PDF
	pdfkit.from_file(path, out)

	'''
	driver.quit() # closes the webbrowser
    
	os.remove(path)
	


#Status 
