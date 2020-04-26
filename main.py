import get_data_from_headhunter as hh
import get_data_from_superjob as sj
from terminaltables import AsciiTable

def main():
    headhunter_jobs_statistics = hh.jobs_from_hh()
    headhunter_jobs_table = AsciiTable(headhunter_jobs_statistics,'HeadHunter Moscow')
    print(headhunter_jobs_table.table)

    super_jobs_statistics = sj.jobs_from_sj()
    super_jobs_table = AsciiTable(super_jobs_statistics,'SuperJob Moscow')
    print(super_jobs_table.table)

if __name__=='__main__':
    main()
