#!/usr/bin/python2.7
import sys
import socket
from scapy.all import *

def getLocalIP():
	try:
		skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		skt.connect(("8.8.8.8",80))
		socketIpPort = skt.getsockname()
		ip = socketIpPort[0]
		skt.close()
		return ip
	except:
		return "127.0.0.1"

def dnsCollect(domain, dnsServer):
	ip_layer = IP(dst=dnsServer, src = getLocalIP())
	sport = random.randint(20000, 60000)
	udp_layer = UDP(sport = sport, dport = 53)
	dns_layer = DNS(id = 1, qr = 0, opcode = 0, tc = 0, rd = 1, qdcount = 1, ancount = 0, nscount = 0, arcount = 0)
	dns_layer.qd = DNSQR(qname = domain, qtype = 1, qclass = 1)
	packet = ip_layer/udp_layer/dns_layer
	mr = sr1(packet,timeout=20)
	return mr


def handle(IP):
	result = dnsCollect("www.baidu.com",IP)
	if(result!=None):
		print "True;True;000"
	else:
		print "False;False;000"

if __name__=="__main__":
	handle(sys.argv[1])
