playlogfiletoserver
===================

Takes a log file in  Apache combined format, load test a server. You can speed up or slow down the simulation. It prints out a report on how long each request took.

Summary: These python scripts take a log file in the standard Apache combined format and load test a server of your choice (like a development server). You can speed up or slow down the simulation. It prints out a report on how long each request took, which you can use to do comparisons between different server configurations with regards to performance. It is tested on Ubuntu 12.04 with pycurl installed.

## Requirements
It needs pycurls to be installed and has been tested on Ubuntu 12.04 Linux.


## How it works
First a pre processor that takes a log file in the Apache combined log file format and outputs a python module containing a tuple of tuples with info on when to fire each request and what request that would be:
    
preparelogfile.py

Secondly, some kind of user agent is needed to do the actual requesting, and it needs to be able to run requests in parallel, lest we would not be load testing the server much if we just kindly wait for it to duly process each request in sequence. I found Pete Warden's pyparallelcurl that uses pycurl/libcurl to do its magic. pyparallelcurl is included in this git repository for convenience:

pyparallelcurl.py

Thirdly and lastly the script to do the actual load testing:

playlogfiletoserver.py


So, first get an appropriate number of lines from an Apache log file inthe combined log format, name it access_log and place it in the same directory as preparelogfile.py, then run from the command line:
    
'''
python preparelogfile.py
'''

...and you should get a new python module called generatedrequests.py. It is a good idea to just use a slice of an Apache log file. I used 9000 lines.

Then, configure these lines in the playlogfiletoserver.py to your taste:
    
'''
server = 'http://www.example.com'
speedup = 4
maxparallelrequests = 100
'''

Changing the speedup value allows you to replay the log file at a higher or lower speed than normal. The value in the file is currently 4, which means a one hour slice of a log file plays back in fifteen minutes. Change the value of speedup to 1 if you want normal playback time.

If you then issue

'''
python playlogfiletoserver.py
'''

...you should start seeing requests hitting the server.

## Catching and analyzing outputs

Assuming bash shell.

Just typing:

'''
python playlogfiletoserver.py
'''

will print to STDOUT. You can print to file instead with:
    
'''
python playlogfiletoserver.py > areport.txt
'''

...or write both to terminal and a file with:
    
'''
python playlogfiletoserver.py | tee areport.txt
'''

If you want to sort requests with longest duration first you can do:
    
cat areport.txt | sort -rn |less

