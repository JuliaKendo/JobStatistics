import service_for_getting_jobs as service
from itertools import count

def read_vacancies_from_hh():
    vacancies_from_hh = {}
    url_template = 'api.hh.ru/vacancies'
    
    for language_num, prog_language in enumerate(service.PROG_LANGUAGES):
        salaries = []
        params = {'area':1,'only_with_salary':True,'currency':'RUR','text':'Программист And {0}'.format(prog_language)}
        for page in count(0):
            params['page'] = page
            url = service.get_url(url_template)
            response_from_site = service.query_to_site(url, params)
            if response_from_site:
                for item in response_from_site['items']:
                    info_salary = item['salary']
                    salaries.append({'from':info_salary['from'],'to':info_salary['to'],'currency':info_salary['currency']})
                if page==response_from_site['pages']:
                    break
        vacancies_from_hh[prog_language] = salaries

    return vacancies_from_hh    

def get_vacancies_from_hh():
    headhunter_jobs_statistics = []
    vacancies_from_hh = read_vacancies_from_hh()
    for prog_language in vacancies_from_hh.keys():
        predicted_salaries = [service.get_predicted_salary(item) for item in vacancies_from_hh[prog_language]]
        processed_jobs_offers = [int(predicted_salary or 0) for predicted_salary in predicted_salaries if int(predicted_salary or 0) > 0]
        amount_jobs_offers = len(processed_jobs_offers)
        amount_predicted_salary = sum(processed_jobs_offers)
        try:
            average_salary = round(amount_predicted_salary/amount_jobs_offers)
        except ZeroDivisionError:
            average_salary = 0
        headhunter_jobs_statistics.append({'source':'HeadHunter',
                                   'language':prog_language,
                                   'total':len(predicted_salaries),
                                   'total_processed':amount_jobs_offers,
                                   'average_salary':average_salary})

    return service.create_table_data(headhunter_jobs_statistics)