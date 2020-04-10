#!/usr/bin/env python

import requests
import sqlite3
import json
from pythonping import ping
import datetime
import concurrent.futures
import time
import socket

targets = {
  #"benedict": {
  #  "target": "Benedict.blender.net",
  #  "size": 500,
  #  "count": 5
  #},
  #"davidpoyner": {
  #  "target": "davidpoyner.com",
  #  "size": 500,
  #  "count": 5
  #},
  #"sam": {
  #  "target": "10.2.1.3",
  #  "size": 500,
  #  "count": 5
  #},
  #"gateway": {
  #  "target": "10.2.1.1",
  #  "size": 500,
  #  "count": 5
  #},
  #"samfqdn": {
  #  "target": "sam.blender.net",
  #  "size": 500,
  #  "count": 5
  #},
  #"brent": {
  #  "target": "alucarddelta.duckdns.org",
  #  "size": 500,
  #  "count": 5
  #},
  #"josh": {
  #  "target": "joshsname.duckdns.org",
  #  "size": 500,
  #  "count": 5
  #},
  "google": {
    "target": "8.8.8.8",
    "size": 500,
    "count": 5
  },
  "google2": {
    "target": "8.8.4.4",
    "size": 500,
    "count": 5
  },
  "cf": {
    "target": "1.1.1.1",
    "size": 500,
    "count": 5
  },
  "cf2": {
    "target": "1.0.0.1",
    "size": 500,
    "count": 5
  },
}

def collector(host):
    print (f"collecting for {targets[host]['target']}")
    x = datetime.datetime.utcnow()
    targets[host]['rtt_min_ms'] = 0
    targets[host]['rtt_avg_ms'] = 0
    targets[host]['rtt_max_ms'] = 0
    targets[host]['packet_success'] = 0
    targets[host]['packet_fail'] = 0
    targets[host]['loss_percentage'] = 0
    try:
        response = ping(targets[host]['target'], size=targets[host]['size'], count=targets[host]['count'], verbose = True)
        targets[host]['rtt_min_ms'] = response.rtt_min_ms
        targets[host]['rtt_avg_ms'] = response.rtt_avg_ms
        targets[host]['rtt_max_ms'] = response.rtt_max_ms
        targets[host]['success'] = True
        targets[host]['created'] = x.strftime('%d/%m/%Y %H:%M:%S')
    except:
        targets[host]['success'] = False
        targets[host]['created'] = x.strftime('%d/%m/%Y %H:%M:%S')
    print (f"collected for {targets[host]['target']}")


def threads():
    hosts = list(targets.keys())
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(collector, hosts)

def ping_response():
    for k, v in targets.items():
        print (f"collecting for {v['target']}")
        v['rtt_min_ms'] = 0
        v['rtt_avg_ms'] = 0
        v['rtt_max_ms'] = 0
        v['packet_success'] = 0
        v['packet_fail'] = 0
        v['loss_percentage'] = 0
        x = datetime.datetime.utcnow()
        try:
            response = ping(v['target'], size=v['size'], count=v['count'], verbose = False)
            v['rtt_min_ms'] = response.rtt_min_ms
            v['rtt_avg_ms'] = response.rtt_avg_ms
            v['rtt_max_ms'] = response.rtt_max_ms
            v['success'] = True
            v['created'] = x.strftime('%d/%m/%Y %H:%M:%S')
        except Exception as e:
            v['success'] = False
            v['created'] = x.strftime('%d/%m/%Y %H:%M:%S')
            response = None
        print (f"collected for {v['target']}")

def update_db():
    conn = sqlite3.connect('../../db.sqlite3')
    c = conn.cursor()
    for k, v in targets.items():
        c.execute(
            '''
            INSERT OR REPLACE into collector_icmp_results (
              name, 
              target, 
              size,
              count,
              min_rtt, 
              avg_rtt, 
              max_rtt, 
              success, 
              created, 
              packet_success, 
              packet_fail, 
              loss_percentage
              ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
            k,
            v['target'],
            v['size'],
            v['count'],
            v['rtt_min_ms'],
            v['rtt_avg_ms'],
            v['rtt_max_ms'],
            v['success'],
            v['created'],
            v['packet_success'],
            v['packet_fail'],
            v['loss_percentage'],
            )
        )
        conn.commit()
    conn.close()

#target = "davidpoyner.com"
#target = "sam.blender.net"
#ping_response = ping(target, size=500, count=10, verbose=False)
#get_response = requests.get('https://' + target).elapsed.total_seconds()

def ShowPingResponses():
    print ("ping response for {}: \n"
        "min: {} ms, max: {} ms, avg: {} ms"
        .format(
            target,
            ping_response.rtt_min_ms,
            ping_response.rtt_max_ms,
            ping_response.rtt_avg_ms,
            )
        )

def ShowGetResponse():
    print ("web response for {}: \n"
    "{} ms"
    .format(
        target,
        get_response*1000
     )
    )

if __name__ == '__main__':
    start = time.perf_counter()
    #ping_response()
    threads()
    update_db()
    #print (targets)
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')
