from datetime import datetime
from math import floor

from dateutil.parser import parse

class Timelapsed:
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2629800
    YEAR = datetime.now().year
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    MONTHSL = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    NOTATIONS = {
        'NOW': ['just now', 'now', 'n'],
        'MIN': [' minute ago', 'min', 'm'],
        'MINS': [' minutes ago', 'mins', 'm'],
        'HOUR': [' hour ago', 'hr', 'h'],
        'HOURS': [' hours ago', 'hrs', 'h'],
        'DAY': ['yesterday', 'dy', 'd'],
        'DAYS': [' days ago', 'dys', 'd'],
        'WEEK': [' week ago', 'wk', 'w'],
        'WEEKS': [' weeks ago', 'wks', 'w']
    }

    @classmethod
    def from_timestamp(cls, timestamp, notation='lng', safe=True, debug=False):
        try:
            microseconds = datetime.fromtimestamp(timestamp).timestamp()
            seconds_lapsed = (datetime.now().timestamp() - microseconds) / 1000;
            return cls.deduct_seconds(seconds_lapsed, 'timestampStr', microseconds, notation);
        except ValueError as e:
            if not safe and not debug:
                raise ValueError('Timestamp out of range')
            elif safe and not debug:
                return 'V/E'
            return 'N/A'
        except TypeError as e:
            if not safe and not debug:
                raise TypeError('Integer is required')
            elif safe and not debug:
                return 'T/E'
            return 'N/A'
    
    @classmethod
    def from_datetimestring(cls, datetimestring, notation='lng', safe=True, debug=False):
        try:
            microseconds = parse(datetimestring).timestamp()
            seconds_lapsed = (datetime.now().timestamp() - microseconds) / 1000;
            return cls.deduct_seconds(seconds_lapsed, 'dateStrStr', microseconds, notation);
        except ValueError as e:
            if not safe and not debug:
                raise ValueError('Timestamp out of range')
            elif safe and not debug:
                return 'V/E'
            return 'N/A'
        except TypeError as e:
            if not safe and not debug:
                raise TypeError('Integer is required')
            elif safe and not debug:
                return 'T/E'
            return 'N/A'

    @classmethod
    def deduct_seconds(cls, seconds_lapsed, datetype, microseconds, notation):
        timestrings = 0;
        if notation == 'twitter':
            timestrings = 2;
        elif notation == 'mid':
            timestrings = 1;
        elif notation == 'lng' or notation == None:
            timestrings = 0;
        else:
            raise Exception("Unknown notation format!\nCurrently accepted formats are 'twitter', 'mid' and 'lng' only!")
        
        if seconds_lapsed < cls.MINUTE:
            return cls.NOTATIONS['NOW'][timestrings]
        elif seconds_lapsed >= cls.MINUTE and seconds_lapsed < cls.HOUR:
            postTime = floor(seconds_lapsed / cls.MINUTE);
            if postTime == 1:
                return str(postTime) + cls.NOTATIONS['MIN'][timestrings]
            else:
                return str(postTime) + cls.NOTATIONS['MINS'][timestrings]
        elif seconds_lapsed >= cls.HOUR and seconds_lapsed < cls.DAY:
            postTime = floor(seconds_lapsed / cls.HOUR);
            if postTime == 1:
                return str(postTime) + cls.NOTATIONS['HOUR'][timestrings]
            else:
                return str(postTime) + cls.NOTATIONS['HOURS'][timestrings]
        elif seconds_lapsed >= cls.DAY and seconds_lapsed < cls.WEEK:
            postTime = floor(seconds_lapsed / cls.DAY);
            if postTime == 1:
                if timestrings == 0:
                    return cls.NOTATIONS['DAY'][timestrings]
                else:
                    return str(postTime) + cls.NOTATIONS['DAY'][timestrings]
            else:
                return str(postTime) + cls.NOTATIONS['DAYS'][timestrings]
        elif seconds_lapsed >= cls.WEEK and seconds_lapsed < cls.MONTH:
            postTime = floor(seconds_lapsed / cls.WEEK);
            if postTime == 1:
                return str(postTime) + cls.NOTATIONS['WEEK'][timestrings]
            else:
                return str(postTime) + cls.NOTATIONS['WEEKS'][timestrings]
        else:
            if datetype == 'dateStrStr':
                return cls.parsedateStr(microseconds, notation, datetype='dateStrStr');
            elif datetype == 'timestampStr':
                return cls.parsedateStr(microseconds, notation, datetype='timestampStr');
    
    @classmethod
    def parsedateStr(cls, microseconds, notation, datetype):
        if datetype == 'dateStrStr':
            thedateObj = parse(microseconds)
        elif datetype == 'timestampStr':
            thedateObj = datetime.fromtimestamp(microseconds)
        else:
            raise Exception("Unknown datetime format!")

        theDate = thedateObj.day
        if notation == 'twitter' or notation == 'mid':
            monthStr = MONTHS;
        elif notation == 'lng' or not notation:
            monthStr = MONTHSL;
        else:
            raise Exception("Unknown notation format!");

        theMonth = thedateObj.month
        theYear = thedateObj.year
        if theYear < cls.YEAR:
            return theDate + ' ' + theMonth + ', ' + theYear;
        else:
            return theDate + ' ' + theMonth;
