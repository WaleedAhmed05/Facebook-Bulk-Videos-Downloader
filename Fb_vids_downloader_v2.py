# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 18:45:53 2019
version 2.0
@author: Waleed
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import urllib.request 
import re
import os
import pandas as pd


def Download_ChromeDriver():
    import zipfile
    downlink="https://chromedriver.storage.googleapis.com/76.0.3809.126/chromedriver_win32.zip" #Latest chromedriver download link for windows
    print("Downloading...")
    urllib.request.urlretrieve(downlink, "webdriver.zip")
    with zipfile.ZipFile("webdriver.zip", 'r') as zip_pos:
        print("Unzipping...")
        zip_pos.extractall()
    os.remove("webdriver.zip") 

if not os.path.exists("chromedriver.exe"):
    print("Chromedriver doesn't exist, Downloading Webdriver...")
    Download_ChromeDriver() 

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('log-level=3')

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

data=pd.read_csv("Video_links.csv")
data_length=len(data)

if data_length==0:
    print("Video List is empty, please add some video links in csv file")
else:
    print("Total Videos to be download..... "+str([data_length]))

def check_isHD(page_source):
    regex = "hd_src:[^\\s(),]+"
    if re.findall(regex, page_source)[0] == 'hd_src:null':
        return False
    else:
        return True

def download(video_url):
    driver.get(video_url)
    page_source = driver.page_source
    
    if check_isHD(page_source):
        regex = "hd_src:\"[^\"\s()]+"
        video_source = re.findall(regex, page_source)[0].replace('&amp;', '&').replace('hd_src:"', '')
        print("HD result available..")
    else:
        regex = "sd_src:\"[^\"\s()]+"
        video_source = re.findall(regex, page_source)[0].replace('&amp;', '&').replace('sd_src:"', '')
        print("No HD result, downloading in standard resolution...")
    
    regex_name=r'<title[^>]*>([^<]+)</title>'
    Video_name=re.findall(regex_name, page_source)[0]
    
    Video_name=Video_name.translate({ord(i): None for i in '|*\/:?<>'})
    print("Downloading............."+str(i+1)+"/"+str(data_length))
    
    if not os.path.exists("Downloaded Vidoes"):
        os.makedirs("Downloaded Vidoes")
    
    urlretrieve(video_source, "Downloaded Vidoes/"+Video_name+'.mp4')
    print(Video_name+" Downloaded")
    
    
fb_url="facebook.com"    
for i in range(data_length):
    print("========================")
    video_url=str(data.iloc[i,0])
    
    if fb_url in video_url:
        driver.get(video_url)
        download(video_url)
    else:
        print("Video "+str([i+1])+" has Invalid URL")
    
driver.quit()