import os
import service_for_getting_jobs as service
from itertools import count

def read_vacancies_from_sj():
    vacancies_from_sj = {}
    url_template = 'api.superjob.ru/2.0/vacancies'
    url_header = {'X-Api-App-Id':os.environ.get('SUPERJOB_SECRETKEY')}
    
    for language_num, prog_language in enumerate(service.PROG_LANGUAGES):
        salaries = []
        params = {'town':'Москва'}
        service.add_keywords(params, 'программист', '0')
        service.add_keywords(params, prog_language, language_num+1)
        for page in count(0):
            params['page'] = page
            url = service.get_url(url_template)
            response_from_site = service.query_to_site(url, params, url_header)
            if response_from_site:
                for item in response_from_site['objects']:
                    salaries.append({'from':item['payment_from'],'to':item['payment_to'],'currency':item['currency']})
                if not response_from_site['more']:
                    break
        vacancies_from_sj[prog_language] = salaries

    return vacancies_from_sj

def get_vacancies_from_sj():
    super_jobs_statistics = []
    vacancies_from_sj = read_vacancies_from_sj()
    for prog_language in vacancies_from_sj.keys():
        predicted_salaries = [service.get_predicted_salary(item) for item in vacancies_from_sj[prog_language]]
        processed_jobs_offers = [int(predicted_salary or 0) for predicted_salary in predicted_salaries if int(predicted_salary or 0) > 0]
        amount_jobs_offers = len(processed_jobs_offers)
        amount_predicted_salary = sum(predicted_salaries)
        try:
            average_salary = round(amount_predicted_salary/amount_jobs_offers)
        except ZeroDivisionError:
            average_salary = 0
        super_jobs_statistics.append({'source':'SuperJob',
                                   'language':prog_language,
                                   'total':len(predicted_salaries),
                                   'total_processed':amount_jobs_offers,
                                   'average_salary':average_salary})

    return service.create_table_data(super_jobs_statistics)