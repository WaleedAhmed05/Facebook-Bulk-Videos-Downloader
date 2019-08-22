"""
Created on Thu Aug  1 14:57:53 2019

@author: Waleed Ahmed
#Version 0.5

~Standard resolutions videos are now downloading, if HD not available.
~Invalid Characters videos are now saving as their iteration number's name.
~Program continuing its iteration, if video has privacy ON or if Video URL is invalid.
~Headless browser added, No UI of browser.
~If Video_links list is empty, it will print an error to put some links in file.



"""

import urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os

data=pd.read_csv("Video_links.csv")
data_length=len(data)

if data_length==0:
    print("Video List is empty, please add some video links in csv file")
else:
    print("Total Videos to be download..... "+str([data_length]))
   
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver', options=chrome_options,)



def download():
    download_id=elemt3.get_attribute('href')
    video_title=elemt3.get_attribute('download').replace('-fbdown.net.mp4','')
    print("Video Name: "+video_title)
    print("Downloading....... "+str(i+1)+"/"+str(data_length))
    print("-------------------------")
    
    if not os.path.exists("Downloaded Vidoes"):
        os.makedirs("Downloaded Vidoes")
    
    try:
        file_name = video_title + '.mp4' 
        urllib.request.urlretrieve(download_id, "Downloaded Vidoes/"+str(file_name))
    except:
        print("Invalid Characters in Video name. ")
        print("Saving video as: "+"Video_"+str(data_length))
        urllib.request.urlretrieve(download_id, "Downloaded Vidoes/Video_"+str(data_length)+".mp4")
    elemt5=driver.find_element_by_class_name("col-md-3")
    elemt5.click()

for i in range(data_length):
    driver.get("https://fbdown.net/")
    
    elemt=driver.find_element_by_name('URLz') 
    elemt.send_keys(str(data.iloc[i,0]))
    
    elemt2=driver.find_element_by_class_name("input-group-btn")
    elemt2.click()
    
    try:
        elemt3=driver.find_element_by_id("hdlink")
        print("HD Result Available, Downloading in HD Result:")
        download()
    except NoSuchElementException:
        try:
            elemt3=driver.find_element_by_id("sdlink")
            print("No HD Available, Downloading in Standard Resolution:")
            download()
        except NoSuchElementException:
            print("Video "+str([i+1])+" is unable to download, due to privacy or it might be invalid URL.")
            pass