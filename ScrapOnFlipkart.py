import time
from queue import Queue
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()

file = open("Flipkart_links.csv","w",encoding = 'utf-8')
file.write('Products, Links\n')

def show_more_function():
    try:
        try:
            show_more = driver.find_element_by_class_name('_2D_EGV')
            show_more.click()
        except:
            show_more = driver.find_element_by_class_name('_1dJtDF._2SvCnW')
            show_more.click()

    except:
        return False


def hasLink():
    block = driver.find_element_by_class_name('_3aoPnm')
    block_items = block.find_elements_by_tag_name("a")
    # for items in block_items:
    #     print(items.text)
    # print("hasLink is over")
    return block_items


def isLink():
    list_item = hasLink()
    global completed_texts
    for item in range(0, len(list_item)):
        if (list_item[item].text not in completed_texts):
            # print(list_item[item].get_attribute("href"))
            # if (list_item[item].get_attribute("href") != "javascript:void(0)"):
            linkQueue.put(list_item[item].get_attribute("href"))
            completed_texts.append(list_item[item].text)
        else:
            continue
    getLink()

def error(link):
    try:
        blockitem = hasLink()
        if len(blockitem) > 0:
            return(link)
    except:
        global non_completed_links
        non_completed_links.append(url)
        getLink()

def getLink():
    link = linkQueue.get()
    driver.get(link)
    try:
        blockitem = hasLink()
        if len(blockitem) > 0:
            show_more_function()
            finalLink(link)
            isLink()
    except:
        global non_completed_links
        non_completed_links.append(url)
        getLink()

def finalLink(link):
    try:
        stri = ""
        block_item = hasLink()
        exceptions = len(driver.find_elements_by_class_name('_3OIXYL'))
        while exceptions > 0:
            stri += str(block_item.pop(0).text) + " >> "
            exceptions = exceptions - 1
        if len(block_item)==0:
            final_items = hasLink()
            for items in final_items:
                print(items.text, end = ""),print(" >> ", end = "")
                file.write(items.text),file.write(" >> " +",")
            print(link)
            file.write(link)
    except:
        return False


if __name__ == '__main__':
    completed_texts = []
    list_item = []
    non_completed_links = []
    linkQueue = Queue()
    starttime = time.time()
    url = "https://www.flipkart.com/all-categories/pr?sid=search.flipkart.com"
    # url = "https://www.flipkart.com/home-cleaning-bathroom-accessories/bathroom-accessories/toothbrush-holders/pr?sid=rja,zqm,oga&otracker=categorytree"
    driver.get(url)
    show_more_function()
    # finalLink(url)
    isLink()
    for links in non_completed_links:
        print(links)
    print('That took {} seconds'.format(time.time() - starttime))
