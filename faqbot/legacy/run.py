'''
This is shitty coz I didn't wanna spend any time
debugging why I keep getting IMAP disconnects.
'''

import subprocess
import time

DEBUG = True
DELAY = 1200 # seconds, or 20 minutes

while True:
	p = subprocess.Popen(["python", "bot.py"])
	time.sleep(DELAY)

	if DEBUG:
		print "Killing {}".format(p.pid)

	p.kill()