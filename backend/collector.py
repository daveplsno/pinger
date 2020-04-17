#!/usr/bin/env python

import os, sys
import textfsm
import subprocess
import pprint
import time, datetime
import concurrent.futures
import requests
import sqlite3
from pathlib import Path

path = Path(__file__).resolve().parent

try:
    token = os.getenv('PINGERTOKEN')
except:
    print ("""
    ow, already with the issues, pls set a token as os var ty

    export PINGERTOKEN=GETTHETOKENFROMDAVELMAO

    or for docker:
    -e PINGERTOKEN=GETTHETOKENFROMDAVELMAO

    tyty
    """)
    sys.exit(1)

def LoadTargetDict(url, token):
    try:
        targets = requests.get(url, headers={'Authorization': 'Token {}'.format(token)})
        if targets != None:
            json = targets.json()
            targetdict = {x['name']: x for x in json['results']}
        return targetdict
    except:
        targetdict = {}
        print ("Issue loading targets")
        return targetdict

def LoadUsername(url, token):
    try:
        username = requests.get(url, headers={'Authorization': 'Token {}'.format(token)})
        if username != None:
            json = username.json()
            username = (json['results'][0]['username'])
            print (f"username: {username}")
        return username
    except:
        username = None
        print ("Issue loading username")
        return username

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
    targetdict[hostname]['results'] = results
    try:
        if targetdict[hostname]['success'] == True:
            #pingtemplate = open(str(path) + "/ping.tsmtemplate")
            pingtemplate = open("ping.tsmtemplate")
            parse_results(pingtemplate, targetdict[hostname]['results'], hostname)
            targetdict[hostname]['data']['username'] = username
        elif targetdict[hostname]['success'] == False:
            print (f"entering default fail results for {hostname}")
            targetdict[hostname]['data']['packetloss'] = 100
            targetdict[hostname]['data']['received'] = 0
            targetdict[hostname]['data']['rtt_avg'] = 0
            targetdict[hostname]['data']['rtt_max'] = 0
            targetdict[hostname]['data']['rtt_min'] = 0
            targetdict[hostname]['data']['transmitted'] = 0
            targetdict[hostname]['data']['created'] = timestamp
            targetdict[hostname]['data']['username'] = username
    except:
        print (f"failed to parse for {hostname}")
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
    ping_reply = str(ping_reply, encoding)
    ping_errors = str(ping_errors, encoding)
    if ping_reply != "":
        targetdict[hostname]['success'] = True
        return ping_reply
    else:
        targetdict[hostname]['success'] = False
        #print (ping_errors)
        return ping_errors

def parse_results(template, result, hostname):
    print (f"started parsing results for {hostname}")
    template = textfsm.TextFSM(template)
    parsed_results = template.ParseText(result)
    data = [dict(zip(template.header, pr)) for pr in parsed_results]
    targetdict[hostname]['data'] = data[0]
    targetdict[hostname]['data']['created'] = timestamp
    print (f"finished parsing results for {hostname}")

"""
update_db() is no longer being used but keeping it here for later cos 
it might be useful to store data locally when api posts fail
letting us post all the stuff that failed whenever api is online again
"""

def update_db():
    pprint.pprint (targetdict)
    conn = None
    try:
        #db = (str(path) + "/db.sqlite3")
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
                  rtt_max, rtt_min, 
                  transmitted, success, results, username
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                k, v['address'], v['data']['created'],
                v['icmp_count'], v['icmp_interval'], v['icmp_size'], 
                v['data']['packetloss'], v['data']['received'],  v['data']['rtt_avg'],
                v['data']['rtt_max'], v['data']['rtt_min'],
                v['data']['transmitted'], v['success'], v['results'], v['data']['username']
                )
            )
            conn.commit()
        print (f"db update successful")
    except:
        print (f"db operation failed")    
    finally:
        if conn:
            conn.close()

def UpdateAPI():
    #pprint.pprint (targetdict)
    stufftopost = {}
    for k, v in targetdict.items():
        stufftopost = {
        "created": v['data']['created'],
        "name": v['name'],
        "address": v['address'],
        "success": v['success'],
        "rtt_min": v['data']['rtt_min'],
        "rtt_avg": v['data']['rtt_avg'],
        "rtt_max": v['data']['rtt_max'],
        "packetloss": v['data']['packetloss'],
        "transmitted": v['data']['transmitted'],
        "received": v['data']['received'],
        "username": username
        }
        requests.post('https://pinger.davidpoyner.com/api/icmp_results/', headers={
                'Authorization': 'Token {}'.format(token),
                'Content-type': 'application/json',
                },
            json = stufftopost
        )
    print ("Updated API")

if __name__ == "__main__":
    while True:
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        targetdict = LoadTargetDict("https://pinger.davidpoyner.com/api/targets.json", token)
        username = LoadUsername("https://pinger.davidpoyner.com/api/user-id/", token)
        print (f"{timestamp}")
        if targetdict != {}:
            WorkerThreads()
            #update_db()
            UpdateAPI()
        else:
            print ("something exploded, retrying in 5 secs")
        time.sleep(5)

"""
if i wanna check timing of script, use these things:
start = time.perf_counter()
finish = time.perf_counter()
print (f'Finished in {round(finish-start, 2)} second(s)')
print (f"sleeping for 5 sec")
"""