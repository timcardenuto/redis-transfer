#!/usr/bin/env python

import redis
import time
import sys

if __name__=="__main__":
	if len(sys.argv)<3:
		print "Error: Redis server IP/port not specified"
		sys.exit(1)	
	host = sys.argv[1]
	port = sys.argv[2]
	r = redis.Redis(host,port)
	while True:
		print "Memory usage:  ",r.info().get('used_memory_human'),"    \r",
		sys.stdout.flush()
		time.sleep(1)
