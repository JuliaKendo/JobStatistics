import os
import service_for_getting_jobs as service
import logging
import math

logger = logging.getLogger('statistics')

def get_total_sj_pages(total_jobs_offers):
    max_num_pages_to_analyze = int(os.environ.get('MAX_NUM_PAGES_TO_ANALYZE') or 0)
    pages = math.ceil(total_jobs_offers / 100)
    return max(pages, max_num_pages_to_analyze)    

def get_total_sj_jobs(url_template, params, header):
    url = service.get_url(url_template)
    response_from_site = service.query_to_site(url, params, header)
    return response_from_site.get('total',0) if response_from_site else 0    

def predict_rub_salary_sj(url_template, params, header):
    predict_rub_salary = {'total_processed':0,'average_salary':0}
    url = service.get_url(url_template)
    response_from_site = service.query_to_site(url, params, header)
    if response_from_site:
        for item in response_from_site['objects']:
            average_salary = None
            try:
                average_salary = service.get_average_salary(item['currency'],item['payment_from'],item['payment_to'])
            except TypeError as error:
                logger.error('Ошибка получения усредненной зарплаты с сайта SuperJob')
            
            if average_salary:
                predict_rub_salary['total_processed'] += 1
                predict_rub_salary['average_salary'] += average_salary

    return predict_rub_salary

def jobs_from_sj():
    super_jobs_statistics = []  
    url_template = 'api.superjob.ru/2.0/vacancies'
    url_header = {'X-Api-App-Id':os.environ.get('SUPERJOB_SECRETKEY')}

    for num_language, prog_language in enumerate(service.PROG_LANGUAGES):
        total_pages = 0
        page = 0
        processed_jobs_offers = 0
        processed_salary = 0
        params = {'town':'Москва','count':100}
        service.add_keywords(params, 'программист', '0')
        service.add_keywords(params, prog_language, num_language+1)
        total_jobs_offers = get_total_sj_jobs(url_template, params, url_header)
        total_pages = get_total_sj_pages(total_jobs_offers)
        while page <= total_pages:
            params['page'] = page
            predict_rub_salary = predict_rub_salary_sj(url_template, params, url_header)
            processed_jobs_offers += predict_rub_salary['total_processed']
            processed_salary += predict_rub_salary['average_salary']
            page += 1
        try:
            average_salary = round(processed_salary/processed_jobs_offers)
        except ZeroDivisionError:
            average_salary = 0
        super_jobs_statistics.append({'source':'SuperJob',
                                   'language':prog_language,
                                   'total':total_jobs_offers,
                                   'total_processed':processed_jobs_offers,
                                   'average_salary':average_salary})

    return service.create_table_data(super_jobs_statistics)