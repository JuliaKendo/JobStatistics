import service_for_getting_jobs as service
from itertools import count

def read_vacancies_from_hh():
    vacancies_from_hh = {}
    url = 'https://api.hh.ru/vacancies'
    
    for prog_language in service.PROG_LANGUAGES:
        salaries = []
        params = {
            'area':1,
            'only_with_salary':True,
            'currency':'RUR',
            'text':'Программист And {0}'.format(prog_language)
        }
        for page in count(0):
            params['page'] = page
            response_from_site = service.query_to_site(url, params)
            if not response_from_site:
                continue
            for item in response_from_site['items']:
                describing_salary = item['salary']
                salaries.append({
                    'from':describing_salary['from'],
                    'to':describing_salary['to'],
                    'currency':describing_salary['currency']
                })
            if page==response_from_site['pages']:
                break
        vacancies_from_hh[prog_language] = salaries

    return vacancies_from_hh    

def get_vacancies_from_hh():
    headhunter_jobs_statistics = []
    vacancies_from_hh = read_vacancies_from_hh()
    for prog_language, salaries in vacancies_from_hh.items():
        predict_salaries = [service.get_predict_salary(describing_salary) for describing_salary in salaries]
        processed_jobs_offers = [predict_salary for predict_salary in predict_salaries if predict_salary and predict_salary > 0]
        amount_jobs_offers = len(processed_jobs_offers)
        amount_predicted_salary = sum(processed_jobs_offers)
        try:
            average_salary = round(amount_predicted_salary/amount_jobs_offers)
        except ZeroDivisionError:
            average_salary = 0
        headhunter_jobs_statistics.append({
            'source':'HeadHunter',
            'language':prog_language,
            'total':len(predict_salaries),
            'total_processed':amount_jobs_offers,
            'average_salary':average_salary
        })

    return service.create_table_data(headhunter_jobs_statistics)