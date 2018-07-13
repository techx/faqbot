"""This is a bad hack, or an alternative as
I'd like to put it, to a cron job shutting
down faqbot and restarting it every so often.

The reason for this is because IDLE is finicky
and our current system doesn't know how to catch
disconnects, so we just restart before stuff
stop working.
"""

import subprocess
import time

VERBOSE = True
DELAY = 1200 # seconds, or 20 minutes

# Loop infinitely.
while True:
    # Start the app.
	p = subprocess.Popen(["python", "app.py"])
	time.sleep(DELAY) # Wait a minute.

	if VERBOSE:
		print "Killing {}".format(p.pid)

	p.kill() # KILL.