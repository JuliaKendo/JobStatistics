import service_for_getting_jobs as service
import logging

logger = logging.getLogger('statistics')

def get_total_hh_pages(url_template, params):
    url = service.get_url(url_template)
    response_from_site = service.query_to_site(url, params)
    return response_from_site.get('pages',0) if response_from_site else 0

def get_total_hh_jobs(url_template, params):
    url = service.get_url(url_template)
    response_from_site = service.query_to_site(url, params)
    return response_from_site.get('found',0) if response_from_site else 0

def predict_rub_salary_from_hh(url_template, params):
    predict_rub_salary = {'total_processed_vacancies':0,'total_predicted_salary':0}
    params['only_with_salary'] = True
    params['currency'] = 'RUR'
    url = service.get_url(url_template)
    response_from_site = service.query_to_site(url, params)
    if not response_from_site:
        return predict_rub_salary

    for item in response_from_site['items']:
        predicted_salary = None
        salary = item['salary']
        try:
            predicted_salary = service.get_predicted_salary(salary['currency'],salary['from'],salary['to'])
        except TypeError as error:
            logger.error('Ошибка получения усредненной зарплаты с сайта Head Hunter')

        if predicted_salary:
            predict_rub_salary['total_processed_vacancies'] += 1
            predict_rub_salary['total_predicted_salary'] += predicted_salary

    return predict_rub_salary

def get_vacancies_from_hh():
    headhunter_jobs_statistics = []
    url_template = 'api.hh.ru/vacancies'

    for prog_language in service.PROG_LANGUAGES:
        page = 0
        processed_jobs_offers = 0
        amount_predicted_salary = 0
        params = {'area':1,'text':'Программист And {0}'.format(prog_language)}
        total_pages = get_total_hh_pages(url_template, params)
        total_jobs_offers = get_total_hh_jobs(url_template, params)
        while page < total_pages:
            predict_rub_salary = predict_rub_salary_from_hh(url_template, params)
            processed_jobs_offers += predict_rub_salary['total_processed_vacancies']
            amount_predicted_salary += predict_rub_salary['total_predicted_salary']
            page += 1
        try:
            average_salary = round(amount_predicted_salary/processed_jobs_offers)
        except ZeroDivisionError:
            average_salary = 0    
        headhunter_jobs_statistics.append({'source':'HeadHunter',
                                        'language':prog_language,
                                        'total':total_jobs_offers,
                                        'total_processed':processed_jobs_offers,
                                        'average_salary':average_salary})
            
    return service.create_table_data(headhunter_jobs_statistics)