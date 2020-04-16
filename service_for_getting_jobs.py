import requests
import logging

PROG_LANGUAGES = ['Python', 'Java', 'JavaScript', 'Go', 'PHP', 'C++', '1C']
logging.basicConfig(level = logging.DEBUG, filename = u'log.txt')

def get_url(url_template, params):
    url = 'https://{0}'.format(url_template)
    return url

def query_to_site(Url, Params, Headers=None):
    try:
        if Headers:
            responce = requests.get(Url, headers=Headers, params=Params)
        else:
            responce = requests.get(Url, params=Params)
    except requests.exceptions.HTTPError as error:
        logging.error(u'Ошибка получения данных по ссылке {0}:\n{1}'.format(Url, error))
        return {}
    responce.raise_for_status()
    return responce.json()

def add_keywords(params, prog_language, num_of_keyword):
    keywords_template = 'keywords[{0}][{1}]'

    for key, param in {'srws':1,'skwc':'and','keys':prog_language}.items():
        params[keywords_template.format(num_of_keyword, key)] = param

def average_salary(Currency, From, To):
    if Currency != 'RUR' and Currency != 'rub':
        return None
    try:
        if From > 0 and To > 0:
            return (From + To) / 2
        elif From > 0 and not To:
            return From * 1.2
        elif not From and To > 0:
            return To * 0.8
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
