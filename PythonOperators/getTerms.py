#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# According to:
# https://www.python.org/dev/peps/pep-0263/
#

import MySQLdb
import sys

if len(sys.argv) < 1:
    print("Required argument missing")
    sys.exit(1)

outputFile = sys.argv[1]
db = MySQLdb.connect("localhost", "etl_jobs", "etl_jobs", "etl_jobs")
cursor = db.cursor()
cursor.execute("SELECT term from search_terms")

fh = open(outputFile, "w")

for x in cursor:
    fh.write(x[0] + "\n")

fh.close()
db.close()
