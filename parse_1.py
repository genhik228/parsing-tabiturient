import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from database import get_institutes, insert_directions, get_city, insert_institutes, insert_city, get_id_direction, \
    insert_ball, insert_exam
from reg_parse import parse_info
from xpath_script import get_fresh_institutes, get_special

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)

def scroll_link():
    while True:
        try:
            driver.execute_script("window.scrollBy(0, 1000);")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[text()='Загрузить еще']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            element.click()
            # time.sleep(2)
            driver.execute_script("window.scrollBy(0, 1000);")
        except:
            new_height = driver.execute_script("return document.body.scrollHeight")
            if driver.execute_script("return window.pageYOffset + window.innerHeight") >= new_height:
                print("Достигнут конец страницы")
                driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
                # time.sleep(1)
                break
            else:
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                # time.sleep(1)

def find_city():
    city_data = []
    try:
        all_russia = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Вся Россия')]"))
        )
        all_russia.click()
        proxodnoi_links = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'city')]"))
        )
        for link in proxodnoi_links:
            html_target = link.get_attribute("outerHTML")
            soup = BeautifulSoup(html_target, 'html.parser')
            region = soup.find('span', class_='font2').b.text.strip()
            city_data.append([link.get_attribute('href'), region])
    except Exception as e:
        print(f"Ошибка: {e}")
    print(city_data)
    insert_city(city_data)

def find_institutes_in_gorod(city_id):
    institutes = get_fresh_institutes(wait)
    date_institutes = []
    for index in range(len(institutes)):
        current_institutes = get_fresh_institutes(wait)
        if index >= len(current_institutes):
            break
        institute = current_institutes[index]
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", institute)
            wait.until(EC.visibility_of(institute))
            try:
                full_name = institute.find_element(By.CSS_SELECTOR, 'span.font2').text
                print(f"Название вуза: {full_name}")
            except Exception as name_error:
                print(f"Не удалось получить название: {name_error}")
                full_name = None
            try:
                name_small = institute.find_element(By.CSS_SELECTOR, 'span.font3').text
                print(f"Название вуза: {name_small}")
            except Exception as name_error:
                print(f"Не удалось получить название: {name_error}")
                name_small = None

            driver.execute_script("arguments[0].click();", institute)
            print(f"Успешный клик на институт #{index + 1}")
            try:
                proxodnoi_links = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'proxodnoi')]"))
                )
                for link in proxodnoi_links:
                    li = link.get_attribute('href')
                    date_institutes.append([city_id, full_name, name_small, li])
                    print(f"Найдена ссылка: {link.get_attribute('href')}")
                    break
            except Exception as link_error:
                print(f"Ссылки не найдены: {link_error}")
        except Exception as e:
            print(f"Ошибка при клике на институт #{index + 1}: {str(e)}")
            driver.execute_script("window.scrollBy(0, 1000);")
    print(date_institutes)
    insert_institutes(date_institutes)

def main():
    driver.get("https://tabiturient.ru/")
    find_city()
    links_gorod = get_city()
    for link_gorod in links_gorod:
        print(link_gorod)
        print("Вызов скролинга")
        driver.get(link_gorod[1])
        scroll_link()
        find_institutes_in_gorod(link_gorod[0])

    links = get_institutes()
    total_links = len(links)
    # links = [(111, 4, 'Филиал Северного (Арктического) федерального университета имени М.В. Ломоносова в г. Коряжме', 'Филиал САФУ в г. Коряжме', 'https://tabiturient.ru/vuzu/narfukf/proxodnoi/')]
    for index, li in enumerate(links, start=1):
        progress = f"[{index}/{total_links}]"
        progress_percent = f"({index / total_links:.0%})"
        print(f"{progress} {progress_percent} Обрабатывается: {li[2]} | Ссылка: {li[4]}")

        driver.get(li[4])
        scroll_link()
        special = get_special(wait)  # Получаем список институтов
        print('ВСЕГО СПЕЦИАЛЬНОСТЕЙ', len(special))
        for index in range(len(special)):
            print(f"[{index}/{len(special)}]")
            print()
            current_special = get_special(wait)
            if index >= len(current_special):
                break
            institute = current_special[index]
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", institute)
                wait.until(EC.visibility_of(institute))
                driver.execute_script("arguments[0].click();", institute)
                target_div = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bg1.bg1-2.p40.pm40")))
                html_target = target_div.get_attribute("outerHTML")
                id_instit = li[0]
                info_dir = parse_info(id_instit, html_target)
                print("ИНФО о направлении 1", info_dir)

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                obs = [
                    item.text.strip()
                    for item in soup.select('.cirfloat3:not(.cirfloatalt) b.font11')
                ]
                dop = [
                    item.text.strip()
                    for item in soup.select('.cirfloat3.cirfloatalt b.font11')
                ]
                bonus_element = driver.find_element(
                    By.XPATH,
                    '//span[@class="font2" and contains(., "Дополнительные баллы:")]'
                )
                bonus_text = bonus_element.text.strip()

                print("Обязательные предметы:", obs)
                print("Дополнительные предметы:", dop)
                print("Дополнительные баллы:", bonus_text)

                td_elements = driver.find_elements(By.CSS_SELECTOR, 'td.psevdoline')
                ball_form1 = []
                ball_form2 = []
                ball_form3 = []
                for td in td_elements:
                    js_code = td.get_attribute('onmouseover')
                    # очно
                    proxans1_match = re.search(r"proxans1-id[^\d]*-.*?innerHTML='(\d+|Нет данных)';", js_code)
                    yearans1_match = re.search(r"yearans1-id[^\d]*-.*?innerHTML='(\d{4})';", js_code)
                    proxans1 = proxans1_match.group(1) if proxans1_match else None
                    yearans1 = yearans1_match.group(1) if yearans1_match else None

                    # Заочная форма обучения
                    proxans2_match = re.search(r"proxans2-id[^\d]*-.*?innerHTML='(\d+|Нет данных)';", js_code)
                    yearans2_match = re.search(r"yearans2-id[^\d]*-.*?innerHTML='(\d{4})';", js_code)
                    proxans2 = proxans2_match.group(1) if proxans2_match else None
                    yearans2 = yearans2_match.group(1) if yearans2_match else None

                    # Очно-заочная форма обучения (вечер)
                    proxans3_match = re.search(r"proxans3-id[^\d]*-.*?innerHTML='(\d+|Нет данных)';", js_code)
                    yearans3_match = re.search(r"yearans3-id[^\d]*-.*?innerHTML='(\d{4})';", js_code)
                    proxans3 = proxans3_match.group(1) if proxans3_match else None
                    yearans3 = yearans3_match.group(1) if yearans3_match else None

                    if proxans1 is not None and yearans1 is not None:
                        if proxans1 != yearans1:
                            ball_form1.append([proxans1, yearans1])
                    if proxans2 is not None and yearans2 is not None:
                        if proxans2 != yearans2:
                            ball_form2.append([proxans2, yearans2])
                    if proxans3 is not None and yearans3 is not None:
                        if proxans3 != yearans3:
                            ball_form3.append([proxans3, yearans3])

                if ball_form1:
                    insert1 = []
                    for i in range(len(info_dir)):
                        l = []
                        for j in range(len(info_dir[i])):
                            l.append(info_dir[i][j])
                        insert1.append(l)
                    for index in range(len(insert1)):
                        insert1[index].append('Очная')
                    print('Очная', insert1)
                    insert_directions(insert1)
                    print("БАЛЛЫ 1", ball_form1)

                    for val in insert1:
                        id_directions_list = get_id_direction(id_instit, val)
                        insert_ball_list = []
                        insert_exams = []
                        print('ID', id_directions_list)

                        for id_d in id_directions_list:
                            for ball in ball_form1:
                                insert_ball_list.append([ball[0], ball[1], id_d[0]])
                            for predmet in obs:
                                insert_exams.append([id_d[0], predmet, 'Обязательный'])

                            for predmet in dop:
                                insert_exams.append([id_d[0], predmet, 'На выбор'])
                        insert_exam(insert_exams)
                        insert_ball(insert_ball_list)
                if ball_form2:
                    insert1 = []
                    for i in range(len(info_dir)):
                        l = []
                        for j in range(len(info_dir[i])):
                            l.append(info_dir[i][j])
                        insert1.append(l)
                    for index in range(len(insert1)):
                        insert1[index].append('Заочная')
                    print('Заочная', insert1)
                    insert_directions(insert1)
                    print("БАЛЛЫ 2", ball_form2)

                    for val in insert1:
                        id_directions_list = get_id_direction(id_instit, val)
                        insert_ball_list = []
                        insert_exams = []
                        print('ID', id_directions_list)
                        for id_d in id_directions_list:
                            for ball in ball_form2:
                                insert_ball_list.append([ball[0], ball[1], id_d[0]])
                            for predmet in obs:
                                insert_exams.append([id_d[0], predmet, 'Обязательный'])

                            for predmet in dop:
                                insert_exams.append([id_d[0], predmet, 'На выбор'])
                        insert_exam(insert_exams)
                        insert_ball(insert_ball_list)
                if ball_form3:
                    insert1 = []
                    for i in range(len(info_dir)):
                        l = []
                        for j in range(len(info_dir[i])):
                            l.append(info_dir[i][j])
                        insert1.append(l)
                    for index in range(len(insert1)):
                        insert1[index].append('Очно - заочная')
                    print('ОЧНО-ЗАОЧ', insert1)
                    print("БАЛЛЫ 3", ball_form3)

                    insert_directions(insert1)
                    for val in insert1:
                        id_directions_list = get_id_direction(id_instit, val)
                        insert_ball_list = []
                        insert_exams = []
                        print('ID', id_directions_list)
                        for id_d in id_directions_list:
                            for ball in ball_form3:
                                insert_ball_list.append([ball[0], ball[1], id_d[0]])
                            for predmet in obs:
                                insert_exams.append([id_d[0], predmet, 'Обязательный'])
                            for predmet in dop:
                                insert_exams.append([id_d[0], predmet, 'На выбор'])
                        insert_exam(insert_exams)
                        insert_ball(insert_ball_list)
            except Exception as e:
                print(f"Ошибка при клике на СПЕЦИАЛИЗАЦИИ #{index + 1}: {str(e)}")
                driver.execute_script("window.scrollBy(0, 500);")
        print()
        print()
main()

