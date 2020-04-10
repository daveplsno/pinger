#!/usr/bin/env python
import textfsm
import subprocess
import pprint
import time
import concurrent.futures

targets = {
  "benedict": {
    "target": "Benedict.blender.net",
    "size": 500,
    "count": 5,
    "interval": 1
  },
  "brent": {
    "target": "alucarddelta.duckdns.org",
    "size": 500,
    "count": 5,
    "interval": 1
  },
}

#targets = {
#  "benedict": {
#    "target": "Benedict.blender.net",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "davidpoyner": {
#    "target": "davidpoyner.com",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "sam": {
#    "target": "10.2.1.3",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "gateway": {
#    "target": "10.2.1.1",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "samfqdn": {
#    "target": "sam.blender.net",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "brent": {
#    "target": "alucarddelta.duckdns.org",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "josh": {
#    "target": "joshsname.duckdns.org",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "google": {
#    "target": "8.8.8.8",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "google2": {
#    "target": "8.8.4.4",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "cf": {
#    "target": "1.1.1.1",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#  "cf2": {
#    "target": "1.0.0.1",
#    "size": 500,
#    "count": 5,
#    "interval": 1
#  },
#}

def collector(hostname):
    p = subprocess.Popen(["ping", "-q",
                        "-c", str(targets[hostname]['count']), 
                        "-W", str(targets[hostname]['interval']), 
                        targets[hostname]['target']
                    ],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    ping_reply, ping_errors = p.communicate()
    encoding = 'utf-8'
    ping_reply_s = str(ping_reply, encoding)
    return ping_reply_s

def parse_results(template, result, hostname):
    template = textfsm.TextFSM(template)
    parsed_results = template.ParseText(result)
    data = [dict(zip(template.header, pr)) for pr in parsed_results]
    targets[hostname]['data'] = data[0]

def SlowWorker():
    start = time.perf_counter()
    pingtemplate = open("ping.tsmtemplate")
    hosts = targets.keys()
    for x in hosts:
        print (f"started working on {x}")
        ping_results = collector (x)
        parse_results(pingtemplate, ping_results, x)
        print (f"finished working on {x}")
    pprint.pprint(targets)
    finish = time.perf_counter()

def FastWorker(hostname):
    pingtemplate = open("ping.tsmtemplate")
    print (f"started working on {hostname}")
    ping_results = collector (hostname)
    parse_results(pingtemplate, ping_results, hostname)
    print (f"finished working on {hostname}")

def FastWorkerThreads():
    hosts = list(targets.keys())
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(FastWorker, hosts)

if __name__ == "__main__":
    start = time.perf_counter()
    #SlowWorker()
    FastWorkerThreads()
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')
    pprint.pprint(targets)