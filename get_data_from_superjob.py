import os
from dotenv import load_dotenv
import service_for_getting_jobs as service

load_dotenv()
url_header = {'X-Api-App-Id':os.getenv('SUPERJOB_SECRETKEY')}

def get_total_sj_pages(total_jobs_offers):
    pages = total_jobs_offers / 100
    if pages > round(pages):
        pages = round(pages)+1
    else:
        pages = round(pages)
    return max(pages, 5)    

def get_total_sj_jobs(url_template, params):
    url = service.get_url(url_template)
    response_from_site = service.query_to_site(url, params, url_header)
    return response_from_site.get('total',0) if response_from_site else 0    

def predict_rub_salary_sj(url_template, params):
    predict_rub_salary = {'total_processed':0,'average_salary':0}
    url = service.get_url(url_template)
    response_from_site = service.query_to_site(url, params, url_header)
    if not response_from_site:
        return predict_rub_salary
        
    for item in response_from_site['objects']:
        average_salary = service.average_salary(item['currency'],item['payment_from'],item['payment_to'])
        if average_salary:
             predict_rub_salary['total_processed'] += 1
             predict_rub_salary['average_salary'] += average_salary

    return predict_rub_salary

def jobs_from_sj():
    super_jobs_statistics = []  
    url_template = 'api.superjob.ru/2.0/vacancies'

    for num_language, prog_language in enumerate(service.PROG_LANGUAGES):
        page = 0
        processed_jobs_offers = 0
        processed_salary = 0
        params = {'town':'Москва','count':100}
        service.add_keywords(params, 'программист', '0')
        service.add_keywords(params, prog_language, num_language+1)
        total_jobs_offers = get_total_sj_jobs(url_template, params)
        total_pages = get_total_sj_pages(total_jobs_offers)
        while page <= total_pages:
            params['page'] = page
            predict_rub_salary = predict_rub_salary_sj(url_template, params)
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