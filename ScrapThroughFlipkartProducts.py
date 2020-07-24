import time
from queue import Queue
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
driver = webdriver.Chrome()

file = open("FlipkartProducts.csv", "w", encoding='utf-8')
file.write("Product Name,Product Price,Product Seller,Product Link\n")

def findLinks():
    block = driver.find_elements_by_class_name("_2cLu-l")
    for names in block:
        if names.get_attribute("href") != "Previous" and names.get_attribute("href") != "Next" and names.get_attribute("href") != "NEXT" and names.get_attribute("href") != "PREVIOUS":
            linkQueue.put(names.get_attribute("href"))
    nextButton = driver.find_elements_by_class_name("_3fVaIS")
    for next in nextButton:
        if next.text == "NEXT":
            next.click()
            time.sleep(1)
            findLinks()
    getLink()


def getLink():
    link = linkQueue.get()
    driver.get(link)
    try:
        itemName = driver.find_element_by_tag_name("h1")
        itemPrice = driver.find_element_by_class_name("_1vC4OE._3qQ9m1")
        try:
            itemSeller = driver.find_element_by_class_name("_9-sL7L")
        except:
            itemSeller = driver.find_element_by_id("sellerName")
        print("Product Name : " + str(itemName.text))
        print("Product Price: " + str(itemPrice.text))
        print("Product Seller: " + str(itemSeller.text))
        print("Product Link: " + link)
        print("------------------------------------------")
        file.write(str(itemName.text) + "," + str(itemPrice.text) + "," + str(itemSeller.text) + "," + link + "\n")
        if(queue.empty()):
            return False
        else:
            getLink()
    except:
        nonCompleted.append(link)
        getLink()

if __name__ == "__main__":
    nonCompleted = []
    starttime = time.time()
    linkQueue = Queue()
    driver.get("https://www.flipkart.com/computers/routers/pr?sid=6bo,2a2&otracker=categorytree")
    findLinks()
    for links in nonCompleted:
        print(links)
    print('That took {} seconds'.format(time.time() - starttime))
file.close()
