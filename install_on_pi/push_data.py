#!/usr/bin/env python
import subprocess, StringIO, csv
from simplejson import dumps
import datetime
import psycopg2

freq = 302 # cron runs every 5 minutes
last_seen = datetime.datetime.now() - datetime.timedelta(seconds=freq)

pgname = "piwifi"
pguser = "pi"
pghost = "pgdatabase"
# set password in ~/.pgpass

def fetch_data():
        # get the newest capture.csv file, then use awk to get only Station data
        cmd = r"cat /tmp/`ls -Art /tmp | grep capture | tail -n 1` | awk '/Station/{y=1;next}y'"
        data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        f = StringIO.StringIO(data)
        # convert the data to a list of dict() objects
        conv = lambda row: {'mac':row[0].strip(), 'last_time_seen':row[2].strip(), 'power':row[3].strip()}
        data = [row for row in csv.reader(f, delimiter=',') if len(row) != 0]
        return [conv(row) for row in data] 

if __name__ == "__main__": 
    data = fetch_data()

    conn = psycopg2.connect(dbname=pgname, user=pguser, host=pghost)
    cur = conn.cursor()

    sql = "INSERT INTO wifi_log (mac, last_time_seen, power) VALUES (%s, %s, %s) ;"

    try:
        for row in data:
            if datetime.datetime.strptime(row['last_time_seen'], '%Y-%m-%d %H:%M:%S') > last_seen:
                cur.execute(sql, (row['mac'], row['last_time_seen'], row['power']))
        conn.commit()
    except Exception, e:
        print data
        print e
    finally:
        conn.close()

