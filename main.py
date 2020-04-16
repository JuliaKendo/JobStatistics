#!/usr/bin/python
# -*- coding: utf-8 -*-

import get_data_from_headhunter as hh
import get_data_from_superjob as sj
from terminaltables import AsciiTable

def main():
    statistics_job_headhunter = hh.jobs_from_hh()
    table_job_headhunter = AsciiTable(statistics_job_headhunter,'HeadHunter Moscow')
    print(table_job_headhunter.table)

    statistics_super_job = sj.jobs_from_sj()
    table_super_job = AsciiTable(statistics_super_job,'SuperJob Moscow')
    print(table_super_job.table)

if __name__=='__main__':
    main()
