#!/usr/bin/env python

import threading
import time
from pythonping.executor import Communicator

target = 'benedict.blender.net'
timeout = 1

client = Communicator(target, None, timeout)

seq = 1
identifier = client.seed_id
attempts = 0
lost = 0
dump_requested = False

def monitor():
    global attempts
    global lost
    while True:
        time.sleep(10)
        loss = round(100 * lost / attempts)
        print("{} packets sent {} packets lost {}% packet loss".format(attempts, lost, loss))
        attempts = 0
        lost = 0

thread = threading.Thread(target=monitor, args=())
thread.daemon = True
thread.start()

while True:
    attempts += 1
    client.send_ping(client.seed_id, seq, b'a')
    res = client.listen_for(identifier, timeout)
    if not res.message:
        lost += 1
    seq = client.increase_seq(seq)
    time.sleep(3)
    print (res)
