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

def LoadTargets():
    try:
        targets = requests.get("http://localhost:10000/targets.json")
        if targets != None:
            targetdict = {x['name']: x for x in targets.json()}
        return targetdict
    except:
        targetdict = {}
        return targetdict

def PingPrefill(hostname):
    x = datetime.datetime.utcnow()
    targetdict[hostname]['data'] = {}
    targetdict[hostname]['data']['success'] = False
    targetdict[hostname]['data']['created'] = x.strftime('%d/%m/%Y %H:%M:%S')
    targetdict[hostname]['data']['packetloss'] = 100
    targetdict[hostname]['data']['received'] = 0
    targetdict[hostname]['data']['rtt_avg'] = 0
    targetdict[hostname]['data']['rtt_max'] = 0
    targetdict[hostname]['data']['rtt_mdev'] = 0
    targetdict[hostname]['data']['rtt_min'] = 0
    targetdict[hostname]['data']['transmitted'] = 0

def collector(hostname):
    p = subprocess.Popen(["ping", "-q",
                        "-c", str(targetdict[hostname]['icmp_count']), 
                        "-W", str(targetdict[hostname]['icmp_interval']),
                        "-s", str(targetdict[hostname]['icmp_size']),
                        targetdict[hostname]['address']
                    ],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    ping_reply, ping_errors = p.communicate()
    encoding = 'utf-8'
    ping_reply_s = str(ping_reply, encoding)
    if ping_reply_s != "":
        targetdict[hostname]['data']['success'] = True
    return ping_reply_s

def parse_results(template, result, hostname):
    if targetdict[hostname]['data']['success'] == True:
        print (f"parsing data for {hostname}")
        x = datetime.datetime.utcnow()
        template = textfsm.TextFSM(template)
        parsed_results = template.ParseText(result)
        data = [dict(zip(template.header, pr)) for pr in parsed_results]
        targetdict[hostname]['data'] = data[0]
        targetdict[hostname]['data']['created'] = x.strftime('%d/%m/%Y %H:%M:%S')
        targetdict[hostname]['data']['success'] = True

def PingWorker(hostname):
    print (f"started working on {hostname}")
    PingPrefill(hostname)
    ping_results = collector(hostname)
    pingtemplate = open(str(path) + "/ping.tsmtemplate")
    parse_results(pingtemplate, ping_results, hostname)
    print (f"finished working on {hostname}")

def WorkerThreads():
    hosts = list(targetdict.keys())
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(PingWorker, hosts)

def update_db():
    db = (str(path) + "/../db.sqlite3")
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
              transmitted, success
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
            k, v['address'], v['data']['created'], 
            v['icmp_count'], v['icmp_interval'], v['icmp_size'], 
            v['data']['packetloss'], v['data']['received'],  v['data']['rtt_avg'],
            v['data']['rtt_max'], v['data']['rtt_mdev'], v['data']['rtt_min'],
            v['data']['transmitted'], v['data']['success']
            )
        )
        conn.commit()
    conn.close()

if __name__ == "__main__":
    #start = time.perf_counter()
    while True:
        time.sleep(2)
        targetdict = LoadTargets()
        if targetdict != {}:
            WorkerThreads()
            update_db()
        else:
            time.sleep(2)
            print ("something exploded, retrying, or die")
    #finish = time.perf_counter()
    #print(f'Finished in {round(finish-start, 2)} second(s)')
    