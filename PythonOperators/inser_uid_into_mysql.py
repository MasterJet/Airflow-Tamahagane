import MySQLdb
import sys
import csv

if len(sys.argv) < 1:
	print "Required argument missing";
	exit(1) 
db = MySQLdb.connect("localhost","etl_jobs","etl_jobs","etl_jobs" );
cursor = db.cursor();

fh = open(sys.argv[1], 'rb');
reader = csv.reader(fh);

for row in reader:
	uid = row[0].strip();
	cursor.execute("insert into topUsers (screen_name) values ('%s') " % (uid));

db.commit();
fh.close();
