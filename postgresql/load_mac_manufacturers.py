#!/usr/bin/env python

import re
import requests
import psycopg2

url = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"

pgname = "piwifi"
pguser = "dba"
pghost = "pgdatabase"
# set password in ~/.pgpass

def fixMAC(line):
    cols = None
    try:
        if not (line == '' or line[0] == '#' or line.replace(' ','') == ''):
            # removes trailing comments and whitespace
            cols = re.split(r'\t+', line.split("#",1)[0].strip())
            if len(cols[0]) == 8:
                cols[0] += ':00:00:00'
            else:
                cols[0] = cols[0][:17]
            if len(cols) <= 2:
                cols.append( cols[1] )
            return cols
        else:
            return None
    except Exception, e:
        print line
        print e

if __name__ == "__main__":
    conn = psycopg2.connect(dbname=pgname, user=pguser, host=pghost)
    cur = conn.cursor()
    sql = "INSERT INTO mac_manufacturers (mac, short_desc, description) VALUES (%s, %s, %s);"

    r = requests.get(url)

    try:
        for line in r.content.split("\n"):
            data = fixMAC(line)
            if not data == None: 
                cur.execute(sql, data)
        conn.commit()
    except Exception, e:
        print line
        print data
        print e
    finally:
        conn.close()
    
