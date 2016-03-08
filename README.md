# NodeR-parse


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
