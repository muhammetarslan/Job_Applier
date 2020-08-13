from selenium import webdriver
import os
import time

driver = webdriver.Chrome('chromedriver')
driver.maximize_window()
page_number = 1

def login():
    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    username_input = driver.find_element_by_id('username')
    password_input = driver.find_element_by_id('password')
    submit_button = driver.find_element_by_xpath('//button[@type="submit"]')

    username_input.send_keys(os.environ.get('LNK_EM'))
    password_input.send_keys(os.environ.get('LNK_PS'))
    submit_button.click()
    time.sleep(2)

def search_sdet():
    driver.get('https://www.linkedin.com/jobs/search/?keywords=sdet&sortBy=DD')
    time.sleep(2)
    res_lst = driver.find_elements_by_css_selector('.jobs-search-results__list.artdeco-list >li')
    return res_lst

def change_page_get_new_list():
    global page_number
    page_number += 1
    driver.find_element_by_xpath('//button[@aria-label="Page {}"]'.format(page_number)).click()
    time.sleep(2)
    res_lst = driver.find_elements_by_css_selector('.jobs-search-results__list.artdeco-list >li')
    return res_lst

'''description stored in html elements under #job-details//span
    this method will scrap them and return the job details
'''
def job_description():
    description_elements = driver.find_elements_by_xpath('//div[@id="job-details"]//*//*')
    description = ''

    for element in description_elements:
        description+=('\n'+element.text)

    return description

def applier():
    login()
    res = search_sdet()
    for posting in res:
        time.sleep(1)
        print(job_description())
        posting.click()
    while page_number<2:
        time.sleep(2)
        res = change_page_get_new_list()
        for posting in res:
            time.sleep(1)
            print(job_description())
            posting.click()

applier()








