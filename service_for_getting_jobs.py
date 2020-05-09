import requests
import logging

PROG_LANGUAGES = ['Python', 'Java', 'JavaScript', 'Go', 'PHP', 'C++', '1C']
logger = logging.getLogger('statistics')


def query_to_site(url, params, headers=None):
    response = requests.get(url, headers=headers or {}, params=params)
    response.raise_for_status()
    return response.json()


def add_keywords(params, prog_language, num_of_keyword):
    keywords_template = 'keywords[{0}][{1}]'
    keywords_params = {
        'srws': 1,
        'skwc': 'and',
        'keys': prog_language
    }
    for key, param in keywords_params.items():
        params[keywords_template.format(num_of_keyword, key)] = param


def calculate_predict_salary(currency, salary_from, salary_to):
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


def get_predict_salary(item):
    predicted_salary = None
    try:
        predicted_salary = calculate_predict_salary(item['currency'], item['from'], item['to'])
    except TypeError:
        logger.error('Ошибка получения усредненной зарплаты с сайта')

    return predicted_salary


def calculate_average_salary(projected_salaries):
    processed_jobs_offers = [projected_salary for projected_salary in projected_salaries if projected_salary and projected_salary > 0]
    amount_jobs_offers = len(processed_jobs_offers)
    amount_predicted_salary = sum(processed_jobs_offers)
    try:
        average_salary = round(amount_predicted_salary / amount_jobs_offers)
    except ZeroDivisionError:
        average_salary = 0

    return average_salary, amount_jobs_offers


def create_table_data(list_of_job_statistics):
    table_data = []
    if list_of_job_statistics:
        table_data.append(['Язык программирования', 'Вакансий найдено', 'Вакансий обработанно', 'Средняя зарплата'])
        for item in list_of_job_statistics:
            table_data.append([item['language'], item['total'], item['total_processed'], item['average_salary']])
    else:
        logger.error('Отсутствуют данные для формирования таблицы вакансий')
    return table_data
