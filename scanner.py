#!/usr/bin/env python3

import concurrent.futures
import socket
import re
import time
import sys

def parsePorts(raw_ports):
	if(raw_ports == 'all'):
		return [i for i in range(1,65537)]

	splitted = raw_ports.split('-')

	if(not len(splitted) == 2):
		return None

	try:
		begin = int(splitted[0])
		end = int(splitted[1])
	except ValueError:
		return None 

	if(end > 65536):
		return None

	return [i for i in range(begin,end+1)]


def parse_IP(raw_IP):
	if(not re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',raw_IP)):
		return None
	return raw_IP

def print_usage_and_terminate(filename):
	usage = """[USAGE] python3 %s ip_address ports
e.g. %s 10.10.10.10 all
e.g. %s 10.10.10.10 1-1024
port ranges are inclusive, and have to be between 1-65536
	""" % (filename,filename,filename)
	print(usage)
	sys.exit()

def scan_port(address, port):
	try:
		socket.create_connection((address, port), TIMEOUT)
		return port		
	except socket.timeout as e:
		return None
	except Exception as e:
		print(e)
		return None


if __name__ == '__main__':
	begin = time.time()

	MAX_THREAD = 80
	TIMEOUT = 0.2

	#get the address and the ports
	filename = sys.argv[0]
	try:
		raw_address = sys.argv[1]
		raw_ports = sys.argv[2]
	except IndexError:
		print_usage_and_terminate(filename)

	address = parse_IP(raw_address)
	if(address == None):
		print_usage_and_terminate(sys.argv[0])
		
	ports = parsePorts(raw_ports)
	if(ports == None):
		print_usage_and_terminate(sys.argv[0])

	print("Scanning %s ..." % address)

	with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
		futures = []
		open_port_counter = 0

		for port in ports:
			futures.append(executor.submit(scan_port,address,port))

		for future in futures:
			if(future.result()):
				open_port_counter += 1
				print(future.result())


	# print(ports)
	print("Open port(s) found: %d" % open_port_counter)
	print("Time passed: " + "{0:0.2f}".format(time.time() - begin) + " seconds.")