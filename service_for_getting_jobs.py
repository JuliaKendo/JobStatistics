import requests
import logging

PROG_LANGUAGES = ['Python', 'Java', 'JavaScript', 'Go', 'PHP', 'C++', '1C']
logging.basicConfig(level = logging.DEBUG, filename = u'log.txt')

def get_url(url_template):
    url = 'https://{0}'.format(url_template)
    return url

def query_to_site(url, params, headers=None):
    try:
        responce = requests.get(url, headers=headers or {}, params=params)
    except requests.exceptions.HTTPError as error:
        logging.error(u'Ошибка получения данных по ссылке {0}:\n{1}'.format(url, error))
        return
    responce.raise_for_status()
    return responce.json()

def add_keywords(params, prog_language, num_of_keyword):
    keywords_template = 'keywords[{0}][{1}]'
    keywords_params = {'srws':1,'skwc':'and','keys':prog_language}
    for key, param in keywords_params.items():
        params[keywords_template.format(num_of_keyword, key)] = param

def average_salary(currency, salary_from, salary_to):
    if currency != 'RUR' and currency != 'rub':
        return None
    try:
        if salary_from > 0 and salary_to > 0:
            return (salary_from + salary_to) / 2
        elif salary_from > 0 and not salary_to:
            return salary_from * 1.2
        elif not salary_from and salary_to > 0:
            return salary_to * 0.8
        else:
            return 0
    except:
        return None

def create_table_data(json_data):
    table_data = []
    if len(json_data)==0:
        logging.error(u'Отсутствуют данные для формирования таблицы вакансий')
        return(table_data)
    table_data.append(['Язык программирования','Вакансий найдено','Вакансий обработанно','Средняя зарплата'])
    for Item in json_data:
        table_data.append([Item['language'],Item['total'],Item['total_processed'],Item['average_salary']])
    return table_data
