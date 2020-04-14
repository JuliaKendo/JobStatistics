import service_for_getting_jobs as service

def get_total_hh_pages(url_template, params):
    params['only_with_salary'] = False
    params['currency'] = ''
    Url = service.get_url(url_template, params)
    JsonInfo = service.query_to_site(Url)
    return JsonInfo['pages']

def get_total_hh_jobs(url_template, params):
    params['only_with_salary'] = False
    params['currency'] = ''
    Url = service.get_url(url_template, params)
    JsonInfo = service.query_to_site(Url)
    return JsonInfo['found']

def predict_rub_salary_hh(url_template, params):
    AverageSalaryInfo = {'total_processed':0,'average_salary':0}
    params['only_with_salary'] = True
    params['currency'] = 'RUR'
    Url = service.get_url(url_template, params)
    JsonInfo = service.query_to_site(Url)
    for item in JsonInfo['items']:
        Salary = item['salary']
        AverageSalary = service.average_salary(Salary['currency'],Salary['from'],Salary['to'])
        if AverageSalary:
            AverageSalaryInfo['total_processed'] += 1
            AverageSalaryInfo['average_salary'] += AverageSalary

    return AverageSalaryInfo

def jobs_from_hh():
    StatisticsJobHeadHunter = []
    params = {'area':1}
    url_template = 'api.hh.ru/vacancies'

    for prog_language in service.PROG_LANGUAGES:
        Page = 0
        ProcessedJobOffers = 0
        ProcessedSalary = 0
        params['text'] = 'Программист And {0}'.format(prog_language)
        TotalPages = get_total_hh_pages(url_template, params)
        TotalJobOffers = get_total_hh_jobs(url_template, params)
        while Page < TotalPages:
            AverageSalary = predict_rub_salary_hh(url_template, params)
            ProcessedJobOffers += AverageSalary['total_processed']
            ProcessedSalary += AverageSalary['average_salary']
            Page += 1
        try:
            ProcessedAverageSalary = round(ProcessedSalary/ProcessedJobOffers)
        except ZeroDivisionError:
            ProcessedAverageSalary = 0    
        StatisticsJobHeadHunter.append({'source':'HeadHunter',
                                        'language':prog_language,
                                        'total':TotalJobOffers,
                                        'total_processed':ProcessedJobOffers,
                                        'average_salary':ProcessedAverageSalary})
            
    return service.create_table_data(StatisticsJobHeadHunter)