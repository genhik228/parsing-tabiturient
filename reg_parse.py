import re


"""
Уровень программы: Бакалавриат
Код программы: 01.03.02
Профиль программы: Прикладное машинное обучение"""
def parse_info(id_institutes, html_target):

    pattern = r'Подразделение:.*?<b>(.*?)</b>'
    match = re.search(pattern, html_target, re.DOTALL)
    if match:
        extracted = match.group(1).strip()
        fac_list = extracted if extracted else 'Отсутствует'
    else:
        fac_list = 'Отсутствует'

    # direction
    pattern = r'Направление подготовки программы:.*?<b>(.*?)</b>'
    match = re.search(pattern, html_target, re.DOTALL)
    direction_list = match.group(1).strip() if match else 'Отсутствует'

    # level_program
    pattern = r'Уровень программы:.*?<b>(.*?)</b>'
    match = re.search(pattern, html_target, re.DOTALL)
    level_list = match.group(1).strip() if match else 'Отсутствует'

    # code_program
    pattern = r'Код программы:.*?<b>(.*?)</b>'
    match = re.search(pattern, html_target, re.DOTALL)
    code_program_list = match.group(1).strip() if match else 'Отсутствует'

    # profile_program
    pattern = r'Профиль программы:.*?<b>(.*?)</b>'
    match = re.search(pattern, html_target, re.DOTALL)
    profile_program_list = match.group(1).strip() if match else 'Отсутствует'

    if profile_program_list != 'Отсутствует':
        profile_program_list = profile_program_list.replace('\n', '')
        result = []
        for value in profile_program_list.split(';'):
            result.append([id_institutes, fac_list, direction_list, level_list, code_program_list, value])
    else:
        result = [[id_institutes, fac_list, direction_list, level_list, code_program_list, 'Отсутствует']]

    return result
