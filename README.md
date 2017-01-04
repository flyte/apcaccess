![build status](https://travis-ci.org/flyte/apcaccess.svg?branch=develop)

apcaccess
=========

A pure Python version of [apcaccess](http://linux.die.net/man/8/apcaccess). This library may be used as part of a Python project to offer programmatic access to the status information provided by [apcupsd](http://www.apcupsd.org/) over its Network Information Server (NIS) which usually listens on TCP port 3551.


Installation
------------

```bash
pip install apcaccess
```

Command Line Usage
-----

The `apcaccess` command line script will output the same as the original [apcaccess](http://linux.die.net/man/8/apcaccess) and takes the following options:

```bash
$ apcaccess --help
usage: apcaccess [-h] [--host HOST] [--port PORT] [--strip-units]

optional arguments:
  -h, --help     show this help message and exit
  --host HOST
  --port PORT
  --strip-units
```

Example output:

```bash
$ apcaccess --host 10.0.0.15
APC      : 001,053,1270
DATE     : 2017-01-04 10:52:18 +0000  
HOSTNAME : hostname.yourdomain.co.uk
VERSION  : 3.14.12 (29 March 2014) redhat
UPSNAME  : netrack
CABLE    : Custom Cable Smart
DRIVER   : APC Smart UPS (any)
UPSMODE  : Stand Alone
STARTTIME: 2016-09-07 12:05:18 +0100  
MODEL    : SMART-UPS 1400
STATUS   : TRIM ONLINE 
LINEV    : 248.3 Volts
LOADPCT  : 11.4 Percent
BCHARGE  : 100.0 Percent
TIMELEFT : 115.0 Minutes
MBATTCHG : 5 Percent
MINTIMEL : 3 Minutes
MAXTIME  : 0 Seconds
MAXLINEV : 252.2 Volts
MINLINEV : 247.0 Volts
OUTPUTV  : 219.7 Volts
SENSE    : High
DWAKE    : 0 Seconds
DSHUTD   : 180 Seconds
DLOWBATT : 2 Minutes
LOTRANS  : 196.0 Volts
HITRANS  : 253.0 Volts
RETPCT   : 15.0 Percent
ITEMP    : 31.5 C
ALARMDEL : Low Battery
BATTV    : 27.6 Volts
LINEFREQ : 50.0 Hz
LASTXFER : High line voltage
NUMXFERS : 210
XONBATT  : 2017-01-04 09:29:53 +0000  
TONBATT  : 0 Seconds
CUMONBATT: 518 Seconds
XOFFBATT : 2017-01-04 09:29:55 +0000  
LASTSTEST: 2016-10-27 23:23:36 +0100  
SELFTEST : NO
STESTI   : 336
STATFLAG : 0x0500000A
DIPSW    : 0x00
REG1     : 0x00
REG2     : 0x00
REG3     : 0x00
MANDATE  : 07/13/99
SERIALNO : GS9939101425
BATTDATE : 13/11/15
NOMOUTV  : 230 Volts
NOMBATTV : 24.0 Volts
EXTBATTS : 0
FIRMWARE : 70.11.I
END APC  : 2017-01-04 10:52:41 +000
```

Programmatic Usage
------------------

The advantage of this project over the original is that it can be used within another Python application to fetch and parse the output from an APC UPS into a more useful format:

```python
In [1]: from apcaccess import status as apc

In [2]: apc.parse(apc.get(host="10.0.0.15"), strip_units=True)
Out[2]: 
OrderedDict([(u'APC', u'001,053,1270'),
             (u'DATE', u'2017-01-04 11:07:36 +0000'),
             (u'HOSTNAME', u'hostname.yourdomain.co.uk'),
             (u'VERSION', u'3.14.12 (29 March 2014) redhat'),
             (u'UPSNAME', u'netrack'),
             (u'CABLE', u'Custom Cable Smart'),
             (u'DRIVER', u'APC Smart UPS (any)'),
             (u'UPSMODE', u'Stand Alone'),
             (u'STARTTIME', u'2016-09-07 12:05:18 +0100'),
             (u'MODEL', u'SMART-UPS 1400'),
             (u'STATUS', u'TRIM ONLINE'),
             (u'LINEV', u'247.0'),
             (u'LOADPCT', u'11.4'),
             (u'BCHARGE', u'100.0'),
             (u'TIMELEFT', u'111.0'),
             (u'MBATTCHG', u'5'),
             (u'MINTIMEL', u'3'),
             (u'MAXTIME', u'0'),
             (u'MAXLINEV', u'250.9'),
             (u'MINLINEV', u'247.0'),
             (u'OUTPUTV', u'218.4'),
             (u'SENSE', u'High'),
             (u'DWAKE', u'0'),
             (u'DSHUTD', u'180'),
             (u'DLOWBATT', u'2'),
             (u'LOTRANS', u'196.0'),
             (u'HITRANS', u'253.0'),
             (u'RETPCT', u'15.0'),
             (u'ITEMP', u'31.5'),
             (u'ALARMDEL', u'Low Battery'),
             (u'BATTV', u'27.6'),
             (u'LINEFREQ', u'50.0'),
             (u'LASTXFER', u'High line voltage'),
             (u'NUMXFERS', u'210'),
             (u'XONBATT', u'2017-01-04 09:29:53 +0000'),
             (u'TONBATT', u'0'),
             (u'CUMONBATT', u'518'),
             (u'XOFFBATT', u'2017-01-04 09:29:55 +0000'),
             (u'LASTSTEST', u'2016-10-27 23:23:36 +0100'),
             (u'SELFTEST', u'NO'),
             (u'STESTI', u'336'),
             (u'STATFLAG', u'0x0500000A'),
             (u'DIPSW', u'0x00'),
             (u'REG1', u'0x00'),
             (u'REG2', u'0x00'),
             (u'REG3', u'0x00'),
             (u'MANDATE', u'07/13/99'),
             (u'SERIALNO', u'GS9939101425'),
             (u'BATTDATE', u'13/11/15'),
             (u'NOMOUTV', u'230'),
             (u'NOMBATTV', u'24.0'),
             (u'EXTBATTS', u'0'),
             (u'FIRMWARE', u'70.11.I'),
             (u'END APC', u'2017-01-04 11:07:52 +000')])
```
