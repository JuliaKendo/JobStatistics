import requests
import logging

PROG_LANGUAGES = ['Python', 'Java', 'JavaScript', 'Go', 'PHP', 'C++', '1C']
logging.basicConfig(level = logging.DEBUG, filename = u'log.txt')

def get_url(url_template, params):
    url = 'https://{0}/'.format(url_template)
    if len(params)>0:
        url = url + '?'
    for key, param in params.items():
        if not param:
            continue
        if type(param)==str:
            value = param.replace(' ','%20')
        else:
            value = param
        if key.find('keyword')==-1:
            url = url + '&{0}={1}'.format(key, value)
        else:
            url = url + '&{0}'.format(value)
    url = url.replace('?&','?')
    return url

def query_to_site(Url, Headers=None):
    try:
        if Headers:
            responce = requests.get(Url, headers=Headers)
        else:
            responce = requests.get(Url)
    except requests.exceptions.HTTPError as error:
        logging.error(u'Ошибка получения данных по ссылке {0}:\n{1}'.format(Url, error))
        return {}
    responce.raise_for_status()
    return responce.json()

def get_keywords(ProgLanguage, NumOfKeyword):
    StrKeyword = ''
    KeywordsTemplate = 'keywords[{0}][{1}]={2}&'

    for Key, Param in {'srws':1,'skwc':'and','keys':ProgLanguage}.items():
        StrKeyword += KeywordsTemplate.format(NumOfKeyword, Key, Param)

    return StrKeyword[:-1]

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

def create_table_data(JsonData):
    TableData = []
    if len(JsonData)==0:
        logging.error(u'Отсутствуют данные для формирования таблицы вакансий')
        return(TableData)
    TableData.append(['Язык программирования','Вакансий найдено','Вакансий обработанно','Средняя зарплата'])
    for Item in JsonData:
        TableData.append([Item['language'],Item['total'],Item['total_processed'],Item['average_salary']])
    return TableData
