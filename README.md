playlogfiletoserver
===================

These python scripts take a log file in the standard Apache combined format and load test a server of your choice (like for eaxmple a testing or staging server). Requests will be made in parallel if necessary, to follow the timing of the log file. You can speed up or slow down the simulation. It prints out a report on how long each request took, which you can use to do comparisons between different server configurations with regards to performance.

## Requirements
It needs pycurl to be installed and has been tested on Ubuntu 12.04 Linux.

It parses log files in the Apache combined log format, which in practice can look something like this in the log file:
    
```
255.127.63.31 - - [01/Sep/2012:04:04:52 +0200] "GET /images/my_picture.png HTTP/1.1" 200 117 "http://www.example.com/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
```

The format specification looks like this in the Apache configuration file:

```
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
```



## How to use it

First get an appropriate time slice from an Apache log file in the combined log format. I used a one hour time slice which in that particular log file meant around 9000 lines. Name the log file access_log and place it in the same directory as preparelogfile.py, then run from the command line:
    
```
python preparelogfile.py
```

...and you should get a new python module called generatedrequests.py.

Then, configure these lines in the playlogfiletoserver.py to your taste:
    
```
server = 'http://www.example.com'
speedup = 4
maxparallelrequests = 100
```

Changing the speedup value allows you to replay the log file at a higher or lower speed than normal. The value in the file is currently 4, which means a one hour slice of a log file plays back in fifteen minutes. Change the value of speedup to 1 if you want normal playback time.

If you then issue

```
python playlogfiletoserver.py
```

...you should start seeing requests hitting the server.

## Catching and analyzing the output

Assuming bash shell.

Just typing:

```
python playlogfiletoserver.py
```

will print to STDOUT. You can print to file instead with:
    
```
python playlogfiletoserver.py > areport.txt
```

...or write both to terminal and a file with:
    
```
python playlogfiletoserver.py | tee areport.txt
```

If you want to sort requests with longest duration first you can do:
    
cat areport.txt | sort -rn |less


## pyparallelcurl

playlogfiletoserver uses Pete Warden's pyparallelcurl 

https://github.com/petewarden/pyparallelcurl

that in its turn uses pycurl/libcurl to do its magic. pyparallelcurl.py is included in this git repository for convenience.

## The format of generatedrequests.py

There is no reason to only have the Apache combined log format as input. Any log format with time stamps should work if a script is made to make a generatedrequests.py file. The format of generatedrequests.py is jus a tuple of tuples, where each tuple has a time stamp in seconds (starting at zero) as the first item and the request (without the server part) as the second.


## Known bugs

playlogfiletoserver assumes the lines in the Apache log files are sorted by time. may in some cases not be entirely true.

There are probably more bugs and/or faulty assumptions.








