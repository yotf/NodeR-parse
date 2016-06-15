#Overview
This code was used for analyzing measurements of a LoRa network deployed in Rennes using Kerlink LoRa IoT stations and custom-made LoRa motes. 
The network deployment, the measurement and the results is described in more detail in https://hal-institut-mines-telecom.archives-ouvertes.fr/hal-01331966/document

Some of the data that was gathered and parsed by the parse_nodeR.py was visualized using Google maps and is available on the following link https://www.google.com/maps/d/viewer?mid=1_-30lffhl8i49GLAaq-KUkrWtE8 (note that a Google account is needed to access and be able to interact with it fully. Sorry to all affected ) 

All data will soon be available also on github. 


# NodeR-parse


```Usage:
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
   ```
   

