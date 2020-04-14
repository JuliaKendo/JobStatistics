import get_data_from_headhunter as HH
import get_data_from_superjob as SJ
from terminaltables import AsciiTable

if __name__=='__main__':

    StatisticsJobHeadHunter = HH.jobs_from_hh()
    TableJobHeadHunter = AsciiTable(StatisticsJobHeadHunter,'HeadHunter Moscow')
    print(TableJobHeadHunter.table)

    StatisticsSuperJob = SJ.jobs_from_sj()
    TableSuperJob = AsciiTable(StatisticsSuperJob,'SuperJob Moscow')
    print(TableSuperJob.table)