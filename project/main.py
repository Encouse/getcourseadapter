from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import os
import json
from selenium.webdriver.firefox.options import Options

base_url = os.environ.get('BASE_URL', 'https://korotylkakurs.ru/')
loginstring = os.environ.get('LOGIN')
passwordstr = os.environ.get('PASSWORD')

def get_driver():
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    return driver

def login(driver):
    driver.get(f'{base_url}cms/system/login')

    login = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH,
             "/html/body/div[1]/div/div/div/div[3]/div/div/div/form/div[1]/div[1]/div/div[1]/input")))

    password = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH,
             "/html/body/div[1]/div/div/div/div[3]/div/div/div/form/div[1]/div[2]/div/div[1]/input")))

    login.send_keys(loginstring)
    password.send_keys(passwordstr)

    login_btn = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'btn-success')))

    login_btn.click()


def go_to_sales(driver):
    driver.get(f'{base_url}pl/sales/deal')


def add_order(driver, email, productid, pay_type='BILL', amount=None, comment=""):
    driver.get(f'{base_url}sales/control/deal/new')
    btn = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH,
             "//*[contains(text(), 'Добавить предложение')]")))
    btn.click()
    add_product_elem = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[contains(text(), {productid})]")))
    add_product_button = add_product_elem.find_element_by_class_name("btn")
    add_product_button.click()
    continue_button = driver.find_element_by_xpath(
        "//button[contains(text(), 'Выбрать')]")
    continue_button.click()
    email_inp = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@id=\"username\"]")))
    email_inp.send_keys(email)
    create_btn = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@value='Создать']")))
    create_btn.click()
    pay_btn = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "//*[contains(text(), 'Добавить платеж')]")
    ))
    pay_btn.click()
    pay_type_datalist = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.ID, "Payment_type")
        )
    )
    pay_type_select = Select(pay_type_datalist)
    pay_type_select.select_by_value(pay_type)
    if amount:
        amount_field = driver.find_element_by_id('Payment_amount')
        amount_field.send_keys(amount)
    payment_status_datalist = driver.find_element_by_id('Payment_status')
    payment_status_select = Select(payment_status_datalist)
    payment_status_select.select_by_value('accepted')
    comment_field = driver.find_element_by_id('Payment_comment')
    comment_field.send_keys(comment)
    save_btn = driver.find_element_by_name('save')
    save_btn.click()
