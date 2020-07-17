import time
import pika
from queue import Queue
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Chrome(executable_path = r'G:\_Eunimart\Tasks\StoringURL - Task IV - 15-06-20\chromedriver.exe')

# file = open("amazon_link.csv","w",encoding = 'utf-8')
# file.write("Products,Links\n")

def show_more_function():
    try:
        show_more = driver.find_element(By.CLASS_NAME, 'a-icon.a-icon-extender-expand')
        show_more.click()
    except:
        return False
    return True

def hasLink():
    # try:
        block = driver.find_element_by_id("departments")
        block_item = block.find_elements_by_tag_name("a")
        return block_item
    # except:
        # return False

def isLink():
    # if(hasLink()):
        list_item = hasLink()
        exceptions = -1   
        try:  
            exceptions = len(driver.find_elements_by_class_name('s-back-arrow.aok-inline-block'))
        except NoSuchElementException:
            exceptions = -1
        finally:
            global completed_texts
            for item in range(exceptions + 1 , len(list_item)):
            # for item in list_item:
                if(list_item[item].text != "Any Department" and list_item[item].text not in completed_texts):
                    # print(list_item[item].get_attribute("href"))
                    if(list_item[item].get_attribute("href")!="javascript:void(0)"):
                        linkQueue.put(list_item[item].get_attribute("href"))
                        completed_texts.append(list_item[item].text)
                else:
                    # break
                    continue
            getLink()

def getLink():
    link = linkQueue.get()
    driver.get(link)
    show_more_function()
    finalLink(link)
    # linkQueue.pop()
    isLink()

def finalLink(link):
    try:
        stri = ''
        block_item = hasLink()
        exceptions = len(driver.find_elements_by_class_name('s-back-arrow.aok-inline-block'))
        while exceptions > 0:
            stri += str(block_item.pop(0).text) + " >> "
            exceptions = exceptions - 1
        if(len(block_item)==0):
            category = driver.find_element_by_id("departments")
            categories = category.find_elements_by_class_name("a-size-base.a-color-base")
            categories.pop(0)
            for name in range(1,len(categories)):
                if(categories[name] != "Any Department"):
                    print(categories[name].text, end =""),print(" >> ",end = "")
            print(link)
    except:
        return False
    return True

if __name__ == '__main__':
    completed_texts = []
    list_item = []
    linkQueue = Queue()
    starttime = time.time()
    # url = "https://www.amazon.in/s?k=all&rh=n%3A1953602031&dc&qid=1594917293&rnid=3576079031&ref=sr_nr_n_1"
    url = "https://www.amazon.in/s?k=all&ref=nb_sb_noss"
    driver.get(url)
    # finalLink(url)
    # show_more_function()
    isLink()
    print('That took {} seconds'.format(time.time() - starttime))
# file.close()
connection.close()