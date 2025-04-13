from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_fresh_institutes(wait):
    try:
        return wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '.vuzlistcontent')))
    except TimeoutException as e:
        print('На сайте ничего нет', e)
        return []

def get_special(wait): # +++++
    try:
        return wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".p20.r20.nonmobile")))
    except TimeoutException as e:
        print('На сайте ничего нет', e)
        return []