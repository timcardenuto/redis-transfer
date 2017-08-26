#!/usr/bin/env python
# Run this part on the Redis server (actually doesn't have to run *on* the Redis server, this script acts as a Redis client, so you can do 'sender.py' -> Redis Server -> 'receiver.py' to transfer data.
# 2 arguments required are IP/port to attach this client to Redis server
# Attaches and waits for transfer message that indicates data is ready to start copying
# Assumes 1 file per transfer message
# Only 1 file transfer at a time FIFO style, the rest are blocked (no threads)

import time
import sys
import os
import errno
import ast
import redis


def transfer(key,filename,filesize):
	if not os.path.exists(os.path.dirname(filename)):
		if os.path.dirname(filename) != '':
			try:
				os.makedirs(os.path.dirname(filename))
			except OSError as exc: # Guard against race condition
				print exc
	fh = open(filename,"wb")
	tmpsize = 0
	start = time.time()
	while(tmpsize < filesize):
		if(r.llen(key) != 0):
			chunk = r.lpop(key)		# pop data chunk off Redis memory (also deletes)
			fh.write(chunk)			# write data chunk to disk			
			tmpsize = tmpsize + sys.getsizeof(chunk) - 37	# 37 is the size of some pointer or something that Redis uses
	fh.close()
	end = time.time()
	print "Completed transfer of ",filesize," bytes"
	print "Download time: ",(end-start)

if __name__=="__main__":
	if len(sys.argv)<3:
		print "Error: Redis server IP/port not specified"
		sys.exit(1)	
	host = sys.argv[1]
	port = sys.argv[2]
	r = redis.Redis(host,port)
	service = r.pubsub()
	service.subscribe('chan')			# this channel name has to be the same for receiver/sender script
	for message in service.listen():	# loop to receive transfer indication and key name
		if isinstance(message['data'],str):
			datadict = ast.literal_eval(message['data'])
			print datadict
			transfer(datadict['key'],datadict['filename'],datadict['filesize'])
			print "########################################\n"




