from selenium import webdriver
import os
import time
import re
from datetime import datetime


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

''' input fields are have to be strings with the comma seperated words.
(ex: pros = 'java, react')
this method will evaluate the post with a pointing system. Each pros will add 1
and each cons will subtract 1. If there are mendatory_pros and mendatory_cons
method won't apply the job if it contains a mendatory_cons or not contain a mendatory_pros. If the overall point >= 4,
the method will execute the job application.
'''
#todo: apply on popular options worksday, dice, indeed etc.
def apply_if_fit(post, pros=None, cons=None, mendatory_pros=None, mendatory_cons=None):
    apply_button = driver.find_element_by_class('jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view')
    apply_button_apply_on_linkedin = False if apply_button.get_attribute('aria-label').endswith('company website') else True
    points = 0
    post = post.lower()


    if(not (pros or cons or mendatory_pros or mendatory_cons)):
        if apply_button_apply_on_linkedin:
            apply_button.click()
            return True
        else:
            pass #todo: apply on popular options worksday, dice, indeed etc.

    if(mendatory_pros):
        mendatory_pros = mendatory_pros.lower()
        mendatory_pros_list = mendatory_pros.split(", ")

        for mendatory_pro in mendatory_pros_list:
            if not re.search(mendatory_pro, post):
                return False

    if(mendatory_cons):
        mendatory_cons = mendatory_cons.lower()
        mendatory_cons_list = mendatory_cons.split(", ")

        for mendatory_con in mendatory_cons_list:
            if re.search(mendatory_con, post):
                return False

    if(pros):
        pros = pros.lower()
        pros_list = pros.split(", ")

        for pro in pros_list:
            if re.search(pro, post):
                points+=1
    if(cons):
        cons = cons.lower()
        cons_list = cons.split(", ")

        for con in cons_list:
            if re.search(con, post):
                points-=1

    if points >= 4:
        if not (pros or cons or mendatory_pros or mendatory_cons):
            if apply_button_apply_on_linkedin:
                apply_button.click()
                return True
            else:
                pass #todo: apply on popular options worksday, dice, indeed etc.


def save_applied():
    job_title = driver.find_element_by_class_name('jobs-details-top-card__job-title t-20 t-black t-normal')
    company = driver.find_element_by_xpath("(//a[@data-control-name='company_link'])[2]")
    location = driver.find_element_by_xpath("(//span[@class='jobs-details-top-card__bullet'])[1]")
    date = datetime.now()
    try:
        f = open('applied_jobs.csv','a')
        f.write('\n{company}, {job_title}, {location}, {date}'.format(company, job_title, location, date))
        f.close()
    except FileNotFoundError:
        print('creating applied_jobs.csv file in the project root directory')
        f = open('applied_jobs.csv','w')
        f.write('{company}, {job_title}, {location}, {date}'.format(company, job_title, location, date))



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


if __name__ == '__main__':
    applier()








