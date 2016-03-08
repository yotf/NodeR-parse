## Detect the JSON entry and load it into json
##
"""Parse NodeR. 

Usage:
   parse_nodeR.py [-g GPS_FILE] -l LOG_FILE -s START_TIME -e END_TIME -n NODE_NAME -f SF -a ANTENNA

Options:
   -h --help     show this help message and exit
   -g GPS_FILE   the gps csv file for given data
   -l LOG_FILE   the NodeR log file from syslog facility1
   -s START_TIME the start of the period of measurement (CET) "2016-02-27 11:34:14"
   -e END_TIME   the end of the period of measurement (CET) "2016-02-27 11:34:14"
   -n NODE_NAME  the name of the node we are interested in (beta,gamma...)
   -f SF         the spreading factor we want to observe
   -a ANTENNA    which antenna (cesson,janvier,tb)

"""
import sys
import pandas as pd
import json
import re
import base64
from datetime import datetime
import numpy as np
from docopt import docopt
#from collections import deque
#//d = deque(maxlen=6)

cntr = 0
rjson = ""
# st_muguet = "2016-03-04 13:47:18"
# end_carrefour = "2016-03-04 14:42:43"
# st_carrefour = "2016-03-04 15:53:53"
# end_muguet = "2016-03-04 16:26:38"
# st_market = "2016-02-27 11:34:14"
# et_market = "2016-02-27 13:26:23"
args = docopt(__doc__)
print args
greek_alphabet = {
    '1': 'alpha',
    '2': 'beta',
    '3': 'gamma',
    '4': 'delta',
    '5': 'epsilon',
    '6': 'zeta',
    '7': 'eta',
    '8': 'theta',
    '9': 'iota',
    'A': 'kappa',
    'B': 'lamda',
    'C': 'mu',
    'D': 'nu',
    'E': 'xi',
    'F': 'omicron',
}
name_to_num = {k:v for (v,k) in greek_alphabet.iteritems()}
mac = "fab000000000000%s" %name_to_num[args["-n"]]

rxpk_patt = re.compile("""{"rxpk":(\[.*?\])}""")
txpk_patt = re.compile("""{"txpk":(.*?})""")
df = None

def set_cet(tmst):
    """Takes timestamp string and localizes to CET timezone"""
    ret = datetime.strptime(tmst, "%Y-%m-%d %H:%M:%S")
    ret = pd.to_datetime(tmst).tz_localize('CET')
    return ret


def buf2int(buf):
    returnVal  = 0
    for i in range(len(buf)):
        returnVal += buf[i]<<(8*(len(buf)-1-i))
    return returnVal

def parse_json(rj):
    """Extracts MID,srcMAC and dstMAC and stores it alltogether in
    a pandas dataframe (global one)"""
    global df
    sfbw_regex = re.compile("SF(\d+)BW(\d+)")
    b64 = base64.b64decode(rj['data'])
    raw_byte = [(ord(c)) for c in b64]
    dstMAC = "".join("{:02x}".format(b) for b in raw_byte[3:5])
    srcMAC = "".join("{:02x}".format(b) for b in raw_byte[5:13])
    msg_id =  buf2int(raw_byte[15:17])
    rj['msg_id']=msg_id
    rj['srcMAC'] = srcMAC
    rj['dstMAC'] = dstMAC
    rj['SF'],rj['BW'] = sfbw_regex.match(rj['datr']).groups()
    rj['frame'] = rj['data']
    del rj['data']
    del rj['datr']
    tmp = {k: [v] for (k,v) in rj.iteritems()}
    tmp = pd.DataFrame(tmp)
    if df is None:
        df = tmp
    else:
        df = pd.concat([df,tmp])

def parse_and_store(rjson):
    """Just to handle different formats of
    rxpk and txpk. However, can be a different function, yeah for sure
    they don't need to be in same file"""
    rjson = json.loads(rjson)
    if isinstance(rjson, list):
        # we just want the first one
        parse_json(rjson[0])
        # for rj in rjson:
        #     parse_json(rj)
    else:
        parse_json(rjson)
        #        print "".join("{:02x}".format(ord(c)) for c in b64)

    


with open(args["-l"]) as outpt:
    rxpkts =rxpk_patt.findall( outpt.read())
    outpt.seek(0)
    #txpkts = txpk_patt.findall(outpt.read())
    # for tx in txpkts:
    #     parse_and_store(tx)
    for rx in rxpkts:
        parse_and_store(rx)

#df.drop_duplicates(inplace=True,subset="msg_id")
# cause might be reset

#print df.set_index(['msg_id'])

# #print df.set_index(range(0,len(df.index)))

# #remove the ones that were sent before or after my experimental
df.index = pd.to_datetime(df.pop('time'))
df.index = df.index.tz_localize('CET')
#df.set_index(pd.to_datetime(df.time,utc=True),inplace=True)
start_time = set_cet(args["-s"])
end_time = set_cet(args["-e"])
print start_time
print end_time
df =  df[(df.index > start_time)]
print df
df = df[ (df.index < end_time)]
print df
df  =  df[df.srcMAC==mac]
print df
df  = df[df.SF==args["-f"]]
print df
outf = 'NodeR-parsed-%s-%s-SF%s-%s-%s.csv' %(args["-a"],args["-n"], args["-f"],args["-s"],args["-e"])
df.to_csv('NodeR-parsed-%s-%s-SF%s-%s-%s.csv' %(args["-a"],args["-n"], args["-f"],args["-s"],args["-e"]))
print "Saved csv of NodeR data to %s" %outf
#if there is no gps data, just give the first csv
if not args["-g"]:
    sys.exit(1)
gps_df = pd.read_csv(args["-g"])
gps_df.index = pd.to_datetime(gps_df.pop('time'),utc=True)
gps_df.index = gps_df.index.tz_localize('utc').tz_convert('CET')
gps_df = gps_df[~gps_df.index.duplicated()]
gps_df = gps_df.reindex(df.index,method="nearest")
allt = pd.merge(df,gps_df,left_index=True,right_index=True)

outf = 'NodeR-and-GPS-%s-%s-SF%s-%s-%s.csv' %(args["-a"],args["-n"], args["-f"],args["-s"],args["-e"])
allt.to_csv(outf)
print "Saved merged csv of GPS and NodeR to %s" %outf
# #remove the ones that were not sent from my device

# mid_in = [(m in ids.id) for m in df['msg_id']]
# print df.msg_id.isin(ids.id) & ids.id.isin(df.msg_id)
# df = df[mid_in]






