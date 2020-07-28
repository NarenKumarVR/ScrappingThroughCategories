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
        show_more = driver.find_element_by_class_name('a-icon.a-icon-extender-expand')
        show_more.click()
    except:
        return False


def is_link(url):
    # try:
        # driver.get(url)
        stri = ""
        product_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'departments'))
        )

        sub_link = product_container.find_elements_by_tag_name("a")
        exceptions = len(driver.find_elements(By.CLASS_NAME, 's-back-arrow.aok-inline-block'))

        while exceptions > 0:
            stri += str(sub_link.pop(0).text) + " >> "
            exceptions = exceptions - 1
        main_links = []
        for link in sub_link:
            if link.get_attribute("href") != "javascript:void(0)":
                # print(link.text)
                main_links.append(link)

        # for link in main_links:
        #     print(link.get_attribute("href"))

        if main_links:
            return main_links
        else:
            return False
    # except:
    #     return False


def get_links(text, url):
    driver.get(url)
    show_more_function()
    if is_link(url):
        sub_link = is_link(url)
        # global links
        links = []
        for link in sub_link:
            links += [(link.text, link.get_attribute("href"))]
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
    url = "https://www.amazon.in/s?k=all&ref=nb_sb_noss"
    final_links("All Departments", url)
    for product_name, product_link in links:
        file.write(product_name.replace(",", "&") + "," + product_link + "\n")
        print(f"{product_name} {'-' * 15} {product_link}")


if __name__ == '__main__':
    # is_link("https://www.flipkart.com/food-products/food-combo/pr?sid=eat,ymr&otracker=categorytree")
    main()

file.close()
