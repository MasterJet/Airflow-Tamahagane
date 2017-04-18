#!/usr/bin/python
# -*- coding: utf-8 -*-
# According to:
# https://www.python.org/dev/peps/pep-0263/
#

from airflow import DAG
from airflow.operators import SimpleHttpOperator, HttpSensor, BashOperator, PythonOperator
from datetime import datetime, timedelta
import os

wdr = '/mnt/wdir/'

bashOperators = os.path.join(wdr, 'bashOperators/')
inputfile = os.path.join(wdr, 'usecase1', 'Final.csv')
tempDir = os.path.join(wdr, 'usecase1', 'temp/')

default_args = {
    'owner': 'User1',
    'depends_on_past': False,
    'start_date': datetime(2017, 2, 1),
    'end_date': datetime(2018, 12, 8),
    'email': ['user1@tesmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),

}

dag = DAG(
    dag_id='ford-f150',
    default_args=default_args,
    schedule_interval="@once"
)

cmdFilterTweets = "bash {}  {} 'ford f-150' 1 1 0 -1 {}" . format(os.path.join(bashOperators, 'grep.sh'), inputfile, os.path.join(tempDir, 'tweetsWithFord'))

filterTweets = BashOperator(
    task_id='grep',
    bash_command=cmdFilterTweets,
    dag=dag
)

cmdFilterUser = "bash {} {} , 4 0 {}".\
					format(os.path.join(bashOperators, 'cut.sh'), os.path.join(tempDir, 'tweetsWithFord' ), os.path.join(tempDir, 'usersWithFord'))

filterUser = BashOperator(
    task_id='Cut',
    bash_command=cmdFilterUser,
    dag=dag
)

cmdSort_Unique_UIDs = "bash {} {} , 1 n 1 {}".\
						format(os.path.join(bashOperators, 'sort.sh'), os.path.join(tempDir, 'usersWithFord' ), os.path.join(tempDir, 'SortedusersWithFord'))

Sort_Unique_UIDs = BashOperator(
    task_id='Sort_Unique_UIDs',
    bash_command=cmdSort_Unique_UIDs,
    dag=dag
)

cmdSort_Original_Data = "bash {} {} , 4 n 0 {}".\
						format(os.path.join(bashOperators, 'sort.sh'), inputfile, os.path.join(tempDir, 'SortedData'))

Sort_Original_Data = BashOperator(
    task_id='Sort_Original_Data',
    bash_command=cmdSort_Original_Data,
    dag=dag
)

cmdFilterTweetsOfUsers = "bash {} {} {} 4 1 , 0 n {}".\
						format(os.path.join(bashOperators, 'join.sh'), os.path.join(tempDir, 'SortedData'), os.path.join(tempDir, 'SortedusersWithFord'), os.path.join(tempDir, 'tweetsOfUserWhoUsedFord'))

FilterTweetsWhoUsedFord = BashOperator(
    task_id='Join',
    bash_command=cmdFilterTweetsOfUsers,
    dag=dag
)

filterTweets.set_downstream(filterUser)
filterUser.set_downstream(Sort_Unique_UIDs)
filterUser.set_downstream(Sort_Original_Data)
Sort_Unique_UIDs.set_downstream(FilterTweetsWhoUsedFord)
Sort_Original_Data.set_downstream(FilterTweetsWhoUsedFord)