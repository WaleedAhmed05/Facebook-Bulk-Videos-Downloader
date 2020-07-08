"""
@author: Waleed Ahmed
#Version 0.7
"""

import urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os

def Download_ChromeDriver():
    import zipfile
    downlink="https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_win32.zip" #Latest chromedriver download link for windows 7-July-20
    print("Downloading...")
    urllib.request.urlretrieve(downlink, "webdriver.zip")
    with zipfile.ZipFile("webdriver.zip", 'r') as zip_pos:
        print("Unzipping...")
        zip_pos.extractall()
    os.remove("webdriver.zip") 

if not os.path.exists("chromedriver.exe"):
    print("Chromedriver doesn't exist, Downloading Webdriver...")
    Download_ChromeDriver()  
    
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver', options=chrome_options,) #remove this and above line if you want to see UI of browser.
   
data=pd.read_csv("Video_links.csv")
data_length=len(data)

if data_length==0:
    print("Video List is empty, please add some video links in csv file")
else:
    print("Total Videos to be download..... "+str([data_length]))

def Download():
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
        elemt3=driver.find_element_by_id("hdlink") #it will download HD resolution video by default
        print("HD Result Available, Downloading in HD Result:")
        Download()
    except NoSuchElementException:
        try:
            elemt3=driver.find_element_by_id("sdlink")
            print("No HD Available, Downloading in Standard Resolution:")
            Download()
        except NoSuchElementException:
            print("Video "+str([i+1])+" is unable to download, due to privacy or it might be invalid URL.")
            pass

driver.quit()        
