import datetime
import re

def get_timestamp(date):
    timestamp = datetime.datetime.strptime(date, '%d/%b/%Y:%H:%M:%S')
    return timestamp
    
def parseline(line):  
    linedict = {}
    line = line.replace('\\"', '%22')
    quoteprep = line.split('"')
    try:
        (linedict['ipnumber'], tmp, tmp, linedict['date'], tmp, tmp) = quoteprep[0].split(" ")
        (linedict['method'], linedict['path'], linedict['protocol']) = quoteprep[1].split(" ")
        (tmp, linedict['returncode'], linedict['bytestransferred'], tmp) = quoteprep[2].split(" ")
        linedict['url'] = quoteprep[3]
        linedict['date'] = linedict['date'][1:]
        
    except ValueError:
        print line
        raise
    return linedict
    
fi = open('access_log', 'r')
fo = open('generatedrequests.py', 'w')
fo.write('requests = (')

first_timestamp = 0
for line in fi:
    linedict = parseline(line)
    if not first_timestamp:
        first_timestamp = get_timestamp(linedict['date'])
        time_offset = 0
    else:
        time_offset = (get_timestamp(linedict['date']) - first_timestamp).seconds
    lineout = '''(%s,"%s"\n),''' % (str(time_offset), linedict['path'])
    fo.write(lineout)
    
fo.write(')')



    
