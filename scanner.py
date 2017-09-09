#!/usr/bin/env python3

from multiprocessing import Pool
import socket
import re
import time

def scan_port(port):
	global address
	try:
		socket.create_connection((address, port), 0.2)
		print(port)
	except socket.timeout as e:
		pass
	except Exception as e:
		print(e)

begin = time.time()

MAX_THREAD = 128

#get the address
default = 'www.tureng.com'
address = input("Enter the address to scan: ")
if(not len(address)):
	address = default

if(re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',address)):
	ip = address
	print(socket.gethostbyaddr(address))
else:
	try:
		print(socket.gethostbyname(address))
	except:
		pass

print("Scanning")
with Pool(MAX_THREAD//4) as pool:
	pool.map(scan_port, range(1, 2**16 + 1))

print("Time passed: " + str(time.time() - begin) + "seconds.")