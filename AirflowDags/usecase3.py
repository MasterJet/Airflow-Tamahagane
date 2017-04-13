import airflow
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from datetime import timedelta


wdr = '/mnt/wdir/'
bashOperators = wdr + 'BashOperators/'
supporting_scripts = wdr + 'supporting_scripts/'
tempDir = wdr + 'usecase3/temp/'

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

dag = DAG(dag_id='useCase3',schedule_interval='@once',  default_args=default_args)


def should_run(ds, **kwargs):
    with open(tempDir + 'fileRows') as fp:
        for line in fp:
            li=str.split(line)
            value=li[0]
            x=int(value)
            if x >= 10000:
                return "Large"
            elif x >= 5000:
                return "Medium"
            else:
                return "Small"
            break




cmdDownloadFromS3 ='aws s3 cp s3://af-testing-data/carsData.tar.gz ' + tempDir
DownloadFromS3 = BashOperator(
    task_id='Download.Data.From.S3',
    bash_command=cmdDownloadFromS3,
    dag=dag)

cmdExtract ='bash ' + bashOperators + 'compression.sh ' + tempDir + 'carsData.tar.gz' + ' e gzip ' + tempDir
Extract = BashOperator(
    task_id='Extract',
    bash_command=cmdExtract,
    dag=dag)
Extract.set_upstream(DownloadFromS3)

cmdGetFilrows='wc -l ' + tempDir + 'carsData.csv > ' + tempDir + 'fileRows'
workLoad = BashOperator(
    task_id='Check.WorkLoad',
    bash_command=cmdGetFilrows,
    dag=dag)
workLoad.set_upstream(Extract)

cond = BranchPythonOperator(
   task_id='If',
    provide_context=True,
    python_callable=should_run,
    dag=dag)
cond.set_upstream(workLoad)

oper_1 = DummyOperator(
    task_id='Small',

    dag=dag)
oper_1.set_upstream(cond)

oper_2 = DummyOperator(
    task_id='Medium',
    dag=dag)
oper_2.set_upstream(cond)

oper_3 = DummyOperator(
    task_id='Large',
    dag=dag)
oper_3.set_upstream(cond)

###
cmdSplitLarge ='bash ' + bashOperators + 'split.sh  ' + tempDir + 'carsData.csv 10 XYZ ' + tempDir 
split10 = BashOperator(
    task_id='Split.File.10',
    bash_command=cmdSplitLarge,
    dag=dag)
split10.set_upstream(oper_3)

cmdGetTermsFromSql ='bash ' + bashOperators + 'split.sh  ' + tempDir + 'carsData.csv 5 XYZ ' + tempDir 
split5 = BashOperator(
    task_id='Split.File.5',
    bash_command=cmdGetTermsFromSql,
    dag=dag)
split5.set_upstream(oper_2)

cmdMergePcs ='bash ' + bashOperators + 'mergeAllFromDir.sh  ' + tempDir + 'chunks ' + tempDir + 'filteredData'
Merge10 = BashOperator(
    task_id='M3.Merge.Results',
    bash_command=cmdMergePcs,
    dag=dag)


cmdMergePcs ='bash ' + bashOperators + 'mergeAllFromDir.sh  ' + tempDir + 'chunks ' + tempDir + 'filteredData'
Merge5 = BashOperator(
    task_id='M2.Merge.Results',
    bash_command=cmdMergePcs,
    dag=dag)

for num in range(0,10):
    cmdFilter ='bash ' + bashOperators + 'grep.sh  ' + tempDir + 'XYZ' + str(num) + ' audi 0 1 1 0 -1 ' + tempDir + 'chunks/Filtered_' + str(num)
    t1 = BashOperator(
    task_id='M3.Filter.task.'+str(num),
    bash_command=cmdFilter,
    dag=dag)
    t1.set_upstream(split10)
    t1.set_downstream(Merge10)

for num in range(0,5):
    cmdFilter ='bash ' + bashOperators + 'grep.sh  ' + tempDir + 'XYZ' + str(num) + ' audi 0 1 1 0 -1 ' + tempDir + 'chunks/Filtered_' + str(num)
    t2 = BashOperator(
    task_id='M2.Filter.task.'+str(num),
    bash_command=cmdFilter,
    dag=dag)
    t2.set_upstream(split5)
    t2.set_downstream(Merge5)

cmdSingleFilter ='bash ' + bashOperators + 'grep.sh  ' + tempDir + 'carsData.csv'+ ' audi 0 1 1 0 -1 ' + tempDir + 'Filtered_Data'  
t3 = BashOperator(
    task_id='Single.Filter.task',
    bash_command=cmdSingleFilter,
    dag=dag)

t3.set_upstream(oper_1)

cmdCompress ='bash ' + bashOperators + 'compression.sh  ' + tempDir + 'filteredData' + ' a gzip foo'
compress = BashOperator(
    task_id='Compress',
    bash_command=cmdCompress,
    dag=dag)

compress.set_upstream(Merge10)

cmdUploadS3 ='aws s3 cp ' + tempDir + 'filteredData.gz s3://af-testing-data/'  
uploadS3 = BashOperator(
    task_id='Upload.S3',
    bash_command=cmdUploadS3,
    dag=dag)
uploadS3.set_upstream(compress)

cmdsample ='bash ' + bashOperators + 'sample.sh ' + tempDir + 'filteredData 100 ' + tempDir + 'sampleData' 
sample = BashOperator(
    task_id='sample',
    bash_command=cmdsample,
    dag=dag)
sample.set_upstream(Merge5)

cmdsamplDB ='python ' + supporting_scripts + 'inser_uid_into_mysql.py ' +  tempDir + 'sampleData' 
samplDB = BashOperator(
    task_id='Sample.Into.DB',
    bash_command=cmdsamplDB,
    dag=dag)
samplDB.set_upstream(sample)

cmdIntoDB ='python ' + supporting_scripts + 'inser_uid_into_mysql.py ' +  tempDir + 'Filtered_Data'
intoDB = BashOperator(
    task_id='into.DB',
    bash_command=cmdIntoDB,
    dag=dag)
intoDB.set_upstream(t3)
