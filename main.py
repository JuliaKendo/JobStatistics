import requests
import os
import logging
import get_data_from_headhunter as hh
import get_data_from_superjob as sj
from dotenv import load_dotenv
from terminaltables import AsciiTable

logger = logging.getLogger('statistics')

def initialize_logger():
    output_dir = os.path.dirname(os.path.realpath(__file__))
    logger.setLevel(logging.DEBUG)
     
    handler = logging.FileHandler(os.path.join(output_dir, 'log.txt'),"a")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def show_jobs_statistics(function_jobs_statistics, title):
    try:
        jobs_statistics = function_jobs_statistics()
    except requests.exceptions.HTTPError as error:
        logger.error('Не удалось получить данные с сайта {0}: {1}'.format(title, error))
    except (KeyError, TypeError) as error:
        logger.error('Ошибка анализа информации с сайта {0}: {1}'.format(title, error))
    else:
        jobs_table = AsciiTable(jobs_statistics, title)
        print(jobs_table.table)

def main():

    load_dotenv()
    initialize_logger()
    show_jobs_statistics(hh.get_vacancies_from_hh, 'HeadHunter Moscow')
    show_jobs_statistics(sj.get_vacancies_from_sj, 'SuperJob Moscow')

if __name__=='__main__':
    main()