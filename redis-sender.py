#!/usr/bin/env python
# Copies files into Redis memory in 1024 bytes chunks and tells receiver process to copy/delete them
# First and second arguments are the IP address and port of the Redis server
# Third argument is the byte size of each transfer (not filesize)
# Any remaining arguments are treated as filenames and will copy them all. Directories are copied recursively.

import time
import sys
import os
import redis


def transfer(filename,chunksize):
	print "Copying: ",filename
	fh = open(filename,"rb")
	fh.seek(0,2)
	filesize = fh.tell()
	print "Filesize: ",filesize," bytes"
	fh.seek(0,0)
	# need way to indicate to receiver that I'm starting transfer and what the key name is
	r.publish('chan', {'key':'chunks','filename':filename,'filesize':filesize})
	num_chunks = filesize/chunksize		
	remainder = filesize%chunksize
	count = 0
	start = time.time()
	while count < num_chunks:
		r.rpush('chunks',fh.read(chunksize))
		count += 1
	r.rpush('chunks',fh.read(remainder))
	end = time.time()
	print "Upload time: ",(end-start)
	print "Completed ##################\n"


if __name__=="__main__":
	# check for Redis server IP/port arguments
	if len(sys.argv)<5:
		print "Error: use command like this:"
		print "./sender.py <redis_server_IP> <redis_server_port> <per_transfer_byte_size> <directory_or_files>"
		sys.exit(1)	
	host = sys.argv[1]
	port = sys.argv[2]
	r = redis.Redis(host,port)
	chunksize = int(sys.argv[3])

	# if copying directory
	if os.path.isdir(sys.argv[4]):
		print "Parsing directory"		
		for subdir, dirs, files in os.walk(sys.argv[4]):
			for file in files:
				filename = subdir + os.sep + file
				transfer(filename,chunksize)

	# if copying 1 or more files
	else:
		for filename in sys.argv[4:]:
			transfer(filename,chunksize)

