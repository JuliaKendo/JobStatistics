import requests
import logging

PROG_LANGUAGES = ['Python', 'Java', 'JavaScript', 'Go', 'PHP', 'C++', '1C']
logger = logging.getLogger('statistics')

def get_url(url_template):
    url = 'https://{0}'.format(url_template)
    return url

def query_to_site(url, params, headers=None):
    logger.info('Запрос к сайту')
    response = requests.get(url, headers=headers or {}, params=params)
    response.raise_for_status()
    return response.json()

def add_keywords(params, prog_language, num_of_keyword):
    keywords_template = 'keywords[{0}][{1}]'
    keywords_params = {'srws':1,'skwc':'and','keys':prog_language}
    for key, param in keywords_params.items():
        params[keywords_template.format(num_of_keyword, key)] = param

def get_average_salary(currency, salary_from, salary_to):
    if currency != 'RUR' and currency != 'rub':
        return None
    if int(salary_from or 0) > 0 and not salary_to:
        return int(salary_from or 0) * 1.2
    elif not salary_from and int(salary_to or 0) > 0:
        return int(salary_to or 0) * 0.8
    elif salary_from > 0 and salary_to > 0:
        return (salary_from + salary_to) / 2
    else:
        return 0

def create_table_data(list_of_job_statistics):
    table_data = []
    if list_of_job_statistics:
        table_data.append(['Язык программирования','Вакансий найдено','Вакансий обработанно','Средняя зарплата'])
        for item in list_of_job_statistics:
            table_data.append([item['language'],item['total'],item['total_processed'],item['average_salary']])
    else:
        logger.error('Отсутствуют данные для формирования таблицы вакансий')
    return table_data