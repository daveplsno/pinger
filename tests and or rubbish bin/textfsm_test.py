#!/usr/bin/env python

import textfsm

results = 'PING joshsname.duckdns.org (180.150.79.145): 500 data bytes\n\n--- joshsname.duckdns.org ping statistics ---\n5 packets transmitted, 5 packets received, 0% packet loss\nround-trip min/avg/max = 13.357/22.654/34.980 ms\n'
pingtemplate = open("ping.tsmtemplate")
template = textfsm.TextFSM(pingtemplate)
parsed = template.ParseText(results)
print (results)
print (parsed)
