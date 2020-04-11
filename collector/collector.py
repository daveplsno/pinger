#!/usr/bin/env python
import textfsm
import subprocess
import pprint
import time, datetime
import concurrent.futures
import requests
import sqlite3

def loadtargets():
    targets = requests.get("http://localhost:10000/targets.json")
    targetdict = {x['name']: x for x in targets.json()}
    return targetdict

def collector(hostname):
    x = datetime.datetime.utcnow()
    targetdict[hostname]['data'] = {}
    targetdict[hostname]['data']['created'] = x.strftime('%d/%m/%Y %H:%M:%S')
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
    if ping_reply != None:
        targetdict[hostname]['data']['success'] = False
        targetdict[hostname]['data']['packetloss'] = 100
        targetdict[hostname]['data']['received'] = 0
        targetdict[hostname]['data']['rtt_avg'] = 0
        targetdict[hostname]['data']['rtt_max'] = 0
        targetdict[hostname]['data']['rtt_mdev'] = 0
        targetdict[hostname]['data']['rtt_min'] = 0
        targetdict[hostname]['data']['transmitted'] = 0
    else:
        targetdict[hostname]['data']['success'] = True
    return ping_reply_s

def parse_results(template, result, hostname):
    x = datetime.datetime.utcnow()
    template = textfsm.TextFSM(template)
    parsed_results = template.ParseText(result)
    data = [dict(zip(template.header, pr)) for pr in parsed_results]
    targetdict[hostname]['data'] = data[0]
    targetdict[hostname]['data']['created'] = x.strftime('%d/%m/%Y %H:%M:%S')
    targetdict[hostname]['data']['success'] = True

def Worker(hostname):
    pingtemplate = open("ping.tsmtemplate")
    print (f"started working on {hostname}")
    ping_results = collector (hostname)
    parse_results(pingtemplate, ping_results, hostname)
    print (f"finished working on {hostname}")

def WorkerThreads():
    hosts = list(targetdict.keys())
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(Worker, hosts)

def update_db():
    conn = sqlite3.connect('../db.sqlite3')
    c = conn.cursor()
    for k, v in targetdict.items():
        c.execute(
            '''
            INSERT OR REPLACE into collector_icmp_results (
              name, 
              address,
              created,
              icmp_count,
              icmp_interval,
              icmp_size,
              packetloss,
              received,
              rtt_avg, 
              rtt_max, 
              rtt_mdev,
              rtt_min, 
              transmitted,
              success
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
            k,
            v['address'],
            v['data']['created'],
            v['icmp_count'],
            v['icmp_interval'],
            v['icmp_size'],
            v['data']['packetloss'],
            v['data']['received'],
            v['data']['rtt_avg'],
            v['data']['rtt_max'],
            v['data']['rtt_mdev'],
            v['data']['rtt_min'],
            v['data']['transmitted'],
            v['data']['success']
            )
        )
        conn.commit()
    conn.close()


if __name__ == "__main__":
    start = time.perf_counter()
    targetdict = loadtargets()
    WorkerThreads()
    update_db()
    pprint.pprint(targetdict)
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')
    