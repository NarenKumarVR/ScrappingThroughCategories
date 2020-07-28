from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

file = open("CategoryLinks.csv", "w", encoding='utf-8')
file.write("Products,Links\n")

path = ''
completed = []


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


def is_link(url):
    try:
        # driver.get(url)
        product_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, '_3aoPnm'))
        )

        sub_link = product_container.find_elements_by_tag_name("a")
        stri = ""
        if len(sub_link) > 0:
            return sub_link
        else:
            return False
    except:
        return False


def get_links(text, url):
    global completed
    if url not in completed:
        driver.get(url)
        completed.append(url)
        show_more_function()
        # global path                 
        # path += text + '>'
        if is_link(url):
            sub_link = is_link(url)
            links = []
            for link in sub_link:
                if link not in completed:
                    links += [(link.text, link.get_attribute("href"))]
                    # print(link.text,link.get_attribute("href"))
                else:
                    continue
            return links
    else:
        return False


links = []


def final_links(text, url):
    sub_link = get_links(text, url)
    if sub_link:
        for text, url in sub_link:
            print(text + " | " + url)
            final_links(text, url)
    else:
        global links
        links += [(text, url)]


def main():
    url = "https://www.flipkart.com/all-categories/pr?sid=search.flipkart.com"
    final_links("All Departments", url)
    for product_name, product_link in links:
        file.write(product_name.replace(",", "&") + "," + product_link + "\n")
        print(f"{product_name} {'-' * 15} {product_link}")


if __name__ == '__main__':
    # is_link("https://www.flipkart.com/food-products/food-combo/pr?sid=eat,ymr&otracker=categorytree")
    main()

file.close()
