import service_for_getting_jobs as service

def get_total_hh_pages(url_template, params):
    Url = service.get_url(url_template, params)
    json_info = service.query_to_site(Url, params)
    return json_info['pages']

def get_total_hh_jobs(url_template, params):
    Url = service.get_url(url_template, params)
    json_info = service.query_to_site(Url, params)
    return json_info['found']

def predict_rub_salary_hh(url_template, params):
    average_salary_info = {'total_processed':0,'average_salary':0}
    params['only_with_salary'] = True
    params['currency'] = 'RUR'
    Url = service.get_url(url_template, params)
    json_info = service.query_to_site(Url, params)
    for item in json_info['items']:
        salary = item['salary']
        average_salary = service.average_salary(salary['currency'],salary['from'],salary['to'])
        if average_salary:
            average_salary_info['total_processed'] += 1
            average_salary_info['average_salary'] += average_salary

    return average_salary_info

def jobs_from_hh():
    statistics_job_headhunter = []
    url_template = 'api.hh.ru/vacancies'

    for prog_language in service.PROG_LANGUAGES:
        page = 0
        processed_job_offers = 0
        processed_salary = 0
        params = {'area':1,'text':'Программист And {0}'.format(prog_language)}
        total_pages = get_total_hh_pages(url_template, params)
        total_job_offers = get_total_hh_jobs(url_template, params)
        while page < total_pages:
            average_salary = predict_rub_salary_hh(url_template, params)
            processed_job_offers += average_salary['total_processed']
            processed_salary += average_salary['average_salary']
            page += 1
        try:
            processed_average_salary = round(processed_salary/processed_job_offers)
        except ZeroDivisionError:
            processed_average_salary = 0    
        statistics_job_headhunter.append({'source':'HeadHunter',
                                        'language':prog_language,
                                        'total':total_job_offers,
                                        'total_processed':processed_job_offers,
                                        'average_salary':processed_average_salary})
            
    return service.create_table_data(statistics_job_headhunter)