import service_for_getting_jobs as service
from itertools import count


def read_vacancies_from_sj(url_header):
    vacancies_from_sj = {}
    url = 'https://api.superjob.ru/2.0/vacancies'

    for language_num, prog_language in enumerate(service.PROG_LANGUAGES):
        salaries = []
        params = {'town': 'Москва'}
        service.add_keywords(params, 'программист', '0')
        service.add_keywords(params, prog_language, language_num + 1)
        for page in count(0):
            params['page'] = page
            response_from_site = service.query_to_site(url, params, url_header)
            if not response_from_site:
                continue
            for describing_job in response_from_site['objects']:
                salaries.append({
                    'from': describing_job['payment_from'],
                    'to': describing_job['payment_to'],
                    'currency': describing_job['currency']
                })
            if not response_from_site['more']:
                break
        vacancies_from_sj[prog_language] = salaries

    return vacancies_from_sj


def get_vacancies_from_sj(url_header):
    super_jobs_statistics = []
    vacancies_from_sj = read_vacancies_from_sj(url_header)
    for prog_language, salaries in vacancies_from_sj.items():
        projected_salaries = [service.get_predict_salary(describing_salary) for describing_salary in salaries]
        average_salary, amount_jobs_offers = service.calculate_average_salary(projected_salaries)
        super_jobs_statistics.append({
            'source': 'SuperJob',
            'language': prog_language,
            'total': len(projected_salaries),
            'total_processed': amount_jobs_offers,
            'average_salary': average_salary
        })

    return service.create_table_data(super_jobs_statistics)
