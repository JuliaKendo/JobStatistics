import os
from dotenv import load_dotenv
import service_for_getting_jobs as service

load_dotenv()
url_header = {'X-Api-App-Id':os.getenv('SECRETKEY')}

def get_total_sj_pages(total_job_offers):
    pages = total_job_offers / 100
    if pages > round(pages):
        pages = round(pages)+1
    else:
        pages = round(pages)
    return max(pages, 5)    

def get_total_sj_jobs(url_template, params):
    Url = service.get_url(url_template, params)
    json_info = service.query_to_site(Url, params, url_header)
    return json_info['total']    

def predict_rub_salary_sj(url_template, params):
    average_salary_info = {'total_processed':0,'average_salary':0}
    Url = service.get_url(url_template, params)
    json_info = service.query_to_site(Url, params, url_header)
    for item in json_info['objects']:
        average_salary = service.average_salary(item['currency'],item['payment_from'],item['payment_to'])
        if average_salary:
             average_salary_info['total_processed'] += 1
             average_salary_info['average_salary'] += average_salary

    return average_salary_info

def jobs_from_sj():
    statistics_super_job = []  
    url_template = 'api.superjob.ru/2.0/vacancies'

    for num_language, prog_language in enumerate(service.PROG_LANGUAGES):
        page = 0
        processed_job_offers = 0
        processed_salary = 0
        params = {'town':'Москва','count':100}
        service.add_keywords(params, 'программист', '0')
        service.add_keywords(params, prog_language, num_language+1)
        total_job_offers = get_total_sj_jobs(url_template, params)
        total_pages = get_total_sj_pages(total_job_offers)
        while page <= total_pages:
            params['page'] = page
            average_salary = predict_rub_salary_sj(url_template, params)
            processed_job_offers += average_salary['total_processed']
            processed_salary += average_salary['average_salary']
            page += 1
        try:
            processed_average_salary = round(processed_salary/processed_job_offers)
        except ZeroDivisionError:
            processed_average_salary = 0
        statistics_super_job.append({'source':'SuperJob',
                                   'language':prog_language,
                                   'total':total_job_offers,
                                   'total_processed':processed_job_offers,
                                    'average_salary':processed_average_salary})

    return service.create_table_data(statistics_super_job)