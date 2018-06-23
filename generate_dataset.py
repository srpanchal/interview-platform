
import selenium
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from urllib.request import urlopen

query = input("Search Criteria: ")# you can change the query for the image  here
image_type="ActiOn"
query= query.split()
query='+'.join(query)
#add the directory for your image here
DIR="Pictures"

#driver=webdriver.Chrome()
driver = webdriver.Chrome('data/chromedriver')
driver.get('https://images.google.com/')
elem=driver.find_element_by_name('q')
elem.send_keys(query)
elem.send_keys(Keys.RETURN)

#scroll down

SCROLL_PAUSE_TIME = 10
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            more=driver.find_element_by_id('smb')
            more.click()
        except:
            break
    last_height = new_height

#Get Pictures
pics=driver.find_elements_by_class_name("rg_meta")

ActualImages=[]

for i in driver.find_elements_by_class_name("rg_meta"):
    link , Type = json.loads(i.get_attribute('innerHTML'))['ou'] , json.loads(i.get_attribute('innerHTML'))['ity']
    ActualImages.append((link,Type))

print('Total', len(ActualImages), 'Images')

header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}

if not os.path.exists(DIR):
            os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)
###print images
for i , (img , Type) in enumerate( ActualImages):
    try:
        #req = request(img, headers={'User-Agent' : header})
        raw_img = urlopen(img).read()

        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        print(cntr)
        if len(Type)==0:
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


        f.write(raw_img)
        f.close()
    except Exception as e:
        print("could not load : "+img)
        print(e)