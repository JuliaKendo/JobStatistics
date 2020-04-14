import os
from dotenv import load_dotenv
import service_for_getting_jobs as service

load_dotenv()
url_params = {'X-Api-App-Id':os.environ.get('SECRETKEY')}

def get_total_sj_pages(TotalJobOffers):
    Pages = TotalJobOffers / 100
    if Pages > round(Pages):
        Pages = round(Pages)+1
    else:
        Pages = round(Pages)
    return max(Pages, 5)    

def get_total_sj_jobs(url_template, params):
    Url = service.get_url(url_template, params)
    JsonInfo = service.query_to_site(Url, url_params)
    return JsonInfo['total']    

def predict_rub_salary_sj(url_template, params):
    AverageSalaryInfo = {'total_processed':0,'average_salary':0}
    Url = service.get_url(url_template, params)
    JsonInfo = service.query_to_site(Url, url_params)
    for item in JsonInfo['objects']:
        AverageSalary = service.average_salary(item['currency'],item['payment_from'],item['payment_to'])
        if AverageSalary:
             AverageSalaryInfo['total_processed'] += 1
             AverageSalaryInfo['average_salary'] += AverageSalary

    return AverageSalaryInfo

def jobs_from_sj():
    StatisticsSuperJob = []
    params = {'town':'Москва','count':100}

    params['keyword0'] = service.get_keywords('программист', '0')
    url_template = 'api.superjob.ru/2.0/vacancies'

    for num_language, prog_language in enumerate(service.PROG_LANGUAGES):
        Page = 0
        ProcessedJobOffers = 0
        ProcessedSalary = 0
        params['keyword1'] = service.get_keywords(prog_language, num_language+1)
        TotalJobOffers = get_total_sj_jobs(url_template, params)
        TotalPages = get_total_sj_pages(TotalJobOffers)
        while Page <= TotalPages:
            params['page'] = Page
            AverageSalary = predict_rub_salary_sj(url_template, params)
            ProcessedJobOffers += AverageSalary['total_processed']
            ProcessedSalary += AverageSalary['average_salary']
            Page += 1
        try:
            ProcessedAverageSalary = round(ProcessedSalary/ProcessedJobOffers)
        except ZeroDivisionError:
            ProcessedAverageSalary = 0
        StatisticsSuperJob.append({'source':'SuperJob',
                                   'language':prog_language,
                                   'total':TotalJobOffers,
                                   'total_processed':ProcessedJobOffers,
                                    'average_salary':ProcessedAverageSalary})

    return service.create_table_data(StatisticsSuperJob)