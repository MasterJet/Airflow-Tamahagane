from airflow import DAG
from airflow.operators import SimpleHttpOperator, HttpSensor, BashOperator, PythonOperator
from datetime import datetime, timedelta
import os

wdr = '/mnt/wdir/'
bashOperators = wdr + 'BashOperators/'
supporting_scripts = wdr + 'supporting_scripts/'
tempDir = wdr + 'usecase2/temp/'

default_args = {
	'owner': 'User1',
	'depends_on_past': False,
	'start_date': datetime(2017, 2, 1),
	'end_date': datetime(2018, 12, 8),
	'email': ['junaidali.it@gmail.com'],
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 0,
	'retry_delay': timedelta(minutes=1),
	
}


dag = DAG(
	dag_id='useCase2',
	default_args=default_args,
	schedule_interval="@once")

cmdGetTermsFromSql ='python ' + supporting_scripts + 'getTerms.py  ' + tempDir + 'searchTerms'
getTerms = BashOperator(
	task_id='get.Terms',
	bash_command=cmdGetTermsFromSql,
	dag=dag)

cmdDownloadFromS3 ='aws s3 cp s3://af-testing-data/carsData.tar.gz ' + tempDir
DownloadFromS3 = BashOperator(
	task_id='Download.From.S3',
	bash_command=cmdDownloadFromS3,
	dag=dag)

cmdExtract ='bash ' + bashOperators + 'compression.sh ' + tempDir + 'carsData.tar.gz' + ' e gzip ' + tempDir
Extract = BashOperator(
	task_id='Extract',
	bash_command=cmdExtract,
	dag=dag)

cmdFilterTweet ='bash ' + bashOperators + 'filterTweetsWithTerms.sh ' + tempDir + 'carsData.csv '  + tempDir + 'searchTerms ' + tempDir + 'filteredTweets'
FilterTweets = BashOperator(
	task_id='Filter.Tweets',
	bash_command=cmdFilterTweet,
	dag=dag)

cmdSample ='bash ' + bashOperators + 'sample.sh ' + tempDir + 'filteredTweets 10 ' + tempDir + 'sampleTweets'
tackSample = BashOperator(
	task_id='Extract.Sample',
	bash_command=cmdSample,
	dag=dag)

cmdSample2Gsheet ='export WORKON_HOME=~/v-ENVs && source /usr/bin/virtualenvwrapper.sh && workon env3 && python ' + supporting_scripts + 'tap-sample.py ' + tempDir + 'sampleTweets | target-gsheet -c ' + supporting_scripts + 'config.json'
Sample2Gsheet = BashOperator(
	task_id='Send.Sample.To.gSheet',
	bash_command=cmdSample2Gsheet,
	dag=dag)

cmdUniqueUsers ='bash ' + bashOperators + 'sort.sh ' + tempDir + 'filteredTweets , 1 d 1 ' + tempDir + 'uniqueUsers'
UniqueUsers = BashOperator(
	task_id='Unique.Users',
	bash_command=cmdUniqueUsers,
	dag=dag)

cmdSortOnFollowers ='bash ' + bashOperators + 'sort.sh ' + tempDir + 'uniqueUsers , 2 d 0 ' + tempDir + 'tweets_sorted'
SortOnFollowers = BashOperator(
	task_id='Sort.On.Followers',
	bash_command=cmdSortOnFollowers,
	dag=dag)

cmdHead100 ='bash ' + bashOperators + 'head.sh ' + tempDir + 'tweets_sorted 100 ' + tempDir + 'top100'
Head100 = BashOperator(
	task_id='Head.100',
	bash_command=cmdHead100,
	dag=dag)

cmdInsertIntoDB ='python ' + supporting_scripts + 'inser_uid_into_mysql.py ' +  tempDir + 'top100'
insertIntoDB = BashOperator(
	task_id='Insert.Into.DB',
	bash_command=cmdInsertIntoDB,
	dag=dag)


# workflow
getTerms.set_downstream(DownloadFromS3)
DownloadFromS3.set_downstream(Extract)
getTerms.set_downstream(FilterTweets)
Extract.set_downstream(FilterTweets)
FilterTweets.set_downstream(tackSample)
tackSample.set_downstream(Sample2Gsheet)
FilterTweets.set_downstream(UniqueUsers)
UniqueUsers.set_downstream(SortOnFollowers)
SortOnFollowers.set_downstream(Head100)
Head100.set_downstream(insertIntoDB)
