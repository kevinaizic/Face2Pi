#!/usr/bin/env python

#change these values to suit your needs, MAC can be found by holding down dash button and connecting to its AP, 
#then browsing to 192.168.0.1, and you can set up the button on your LAN with the amazon app 
#**just close the app when it asks to select a product or you're going to end up ordering stuff with every actuation**
#
#clustercam calls this script which will wait indefinitely until a press it detected, then start taking pictures, and repeat

from scapy.all import *

def arp_detect(pkt):
    if pkt[ARP].op == 1: #network request
	if pkt[ARP].hwsrc == '00:00:00:00:00:00': #clorox
		print("cloroxpress") 
		exit()
        elif pkt[ARP].hwsrc == '00:00:00:00:00:00': #doritos
		print("doritospress")
		exit()

#keepalive without print 
sniff(prn=arp_detect, filter="arp", store=0)
