#!/usr/bin/env python

import textfsm
import subprocess
import pprint
import time, datetime
import concurrent.futures
import requests
import sqlite3
from pathlib import Path

path = Path(__file__).resolve().parent

def LoadTargetDict(url):
    try:
        targets = requests.get(url)
        if targets != None:
            json = targets.json()
            targetdict = {x['name']: x for x in json['results']}
        return targetdict
    except:
        targetdict = {}
        return targetdict

def WorkerThreads():
    listofhosts = list(targetdict.keys())
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(PingWorker, listofhosts)

def PingWorker(hostname):
    print (f"started pinging {hostname}")
    targetdict[hostname]['data'] = {}
    results = collector (
        targetdict[hostname]['name'],
        targetdict[hostname]['address'], 
        targetdict[hostname]['icmp_count'], 
        targetdict[hostname]['icmp_interval'], 
        targetdict[hostname]['icmp_size']
        )
    print (f"finished pinging {hostname}")
    print (f"parsing for {hostname}")
    targetdict[hostname]['results'] = results
    pingtemplate = open(str(path) + "/ping.tsmtemplate")
    #pingtemplate = open("ping.tsmtemplate")
    parse_results(pingtemplate, targetdict[hostname]['results'], hostname)
    print (f"finished parsing for {hostname}")
    return results

def collector(hostname, address, count, interval, size):
    p = subprocess.Popen(["ping", "-q",
                        "-c", str(count), 
                        "-W", str(interval),
                        "-s", str(size),
                        address
                        ],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE
                     )
    ping_reply, ping_errors = p.communicate()
    encoding = 'utf-8'
    ping_reply_s = str(ping_reply, encoding)
    ping_errors_s = str(ping_errors, encoding)
    if ping_reply_s != "":
        targetdict[hostname]['success'] = True
        return ping_reply_s
    else:
        targetdict[hostname]['success'] = False
        return ping_errors_s

def parse_results(template, result, hostname):
    x = datetime.datetime.utcnow()
    if targetdict[hostname]['success'] == True:
        print (f"parsing data for {hostname}")
        x = datetime.datetime.utcnow()
        template = textfsm.TextFSM(template)
        parsed_results = template.ParseText(result)
        data = [dict(zip(template.header, pr)) for pr in parsed_results]
        targetdict[hostname]['data'] = data[0]
        targetdict[hostname]['data']['created'] = x.strftime('%Y-%m-%d %H:%M:%S')
    elif targetdict[hostname]['success'] == False:
        targetdict[hostname]['data']['packetloss'] = 100
        targetdict[hostname]['data']['received'] = 0
        targetdict[hostname]['data']['rtt_avg'] = 0
        targetdict[hostname]['data']['rtt_max'] = 0
        targetdict[hostname]['data']['rtt_mdev'] = 0
        targetdict[hostname]['data']['rtt_min'] = 0
        targetdict[hostname]['data']['transmitted'] = 0
        targetdict[hostname]['data']['created'] = x.strftime('%Y-%m-%d %H:%M:%S')

def update_db():
    db = (str(path) + "/../db.sqlite3")
    #db = ("../db.sqlite3")
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for k, v in targetdict.items():
        c.execute(
            '''
            INSERT OR REPLACE into collector_icmp_results (
              name, address, created,
              icmp_count, icmp_interval, icmp_size, 
              packetloss, received, rtt_avg, 
              rtt_max, rtt_mdev, rtt_min, 
              transmitted, success, results
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
            k, v['address'], v['data']['created'],
            v['icmp_count'], v['icmp_interval'], v['icmp_size'], 
            v['data']['packetloss'], v['data']['received'],  v['data']['rtt_avg'],
            v['data']['rtt_max'], v['data']['rtt_mdev'], v['data']['rtt_min'],
            v['data']['transmitted'], v['success'], v['results']
            )
        )
        conn.commit()
    conn.close()

if __name__ == "__main__":
    while True:
        start = time.perf_counter()
        targetdict = LoadTargetDict("http://localhost:10000/targets.json")
        if targetdict != {}:
            WorkerThreads()
            update_db()
        else:
            print ("something exploded, retrying in 5 secs")
        finish = time.perf_counter()
        print (f'Finished in {round(finish-start, 2)} second(s)')
        print ("sleeping for 5 sec")
        time.sleep(5)