import requests
import os
import logging
import get_data_from_headhunter as hh
import get_data_from_superjob as sj
from dotenv import load_dotenv
from terminaltables import AsciiTable

logger = logging.getLogger('statistics')

class SaveLogHandler(logging.Handler):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    def emit(self, record):
        log_entry = self.format(record)+'\n'
        with open(self.filename, 'a') as logfile:
            logfile.write(log_entry)

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
    logger.setLevel(logging.DEBUG)
    logger.addHandler(SaveLogHandler('log.txt'))
    show_jobs_statistics(hh.jobs_from_hh, 'HeadHunter Moscow')
    show_jobs_statistics(sj.jobs_from_sj, 'SuperJob Moscow')

if __name__=='__main__':
    main()