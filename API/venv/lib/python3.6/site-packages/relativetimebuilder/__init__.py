# -*- coding: utf-8 -*-

# Copyright (c) 2019, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import math

from aniso8601.builders.python import PythonTimeBuilder

class RelativeValueError(ValueError):
    """Raised when an invalid value is given for calendar level accuracy."""

class RelativeTimeBuilder(PythonTimeBuilder):
    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):

        try:
            import dateutil.relativedelta
        except ImportError:
            raise RuntimeError('dateutil must be installed for '
                               'relativedelta support.')

        if ((PnY is not None and '.' in PnY)
                or (PnM is not None and '.' in PnM)):
            #https://github.com/dateutil/dateutil/issues/40
            raise RelativeValueError('Fractional months and years are not '
                                     'defined for relative durations.')

        years = 0
        months = 0
        days = 0
        weeks = 0
        hours = 0
        minutes = 0
        seconds = 0
        microseconds = 0

        floatdays = float(0)
        floatweeks = float(0)
        floathours = float(0)
        floatminutes = float(0)
        floatseconds = float(0)

        if PnY is not None:
            years = cls.cast(PnY, int,
                             thrownmessage='Invalid year string.')

        if PnM is not None:
            months = cls.cast(PnM, int,
                              thrownmessage='Invalid month string.')

        if PnW is not None:
            if '.' in PnW:
                weeks, floatweeks = cls._split_and_cast(PnW, 'Invalid week string.')
            else:
                weeks = cls.cast(PnW, int,
                                 thrownmessage='Invalid week string.')

        if PnD is not None:
            if '.' in PnD:
                days, floatdays = cls._split_and_cast(PnD, 'Invalid day string.')
            else:
                days = cls.cast(PnD, int,
                                thrownmessage='Invalid day string.')

        if TnH is not None:
            if '.' in TnH:
                hours, floathours = cls._split_and_cast(TnH, 'Invalid hour string.')
            else:
                hours = cls.cast(TnH, int,
                                 thrownmessage='Invalid hour string.')

        if TnM is not None:
            if '.' in TnM:
                minutes, floatminutes = cls._split_and_cast(TnM, 'Invalid minute string.')
            else:
                minutes = cls.cast(TnM, int,
                                   thrownmessage='Invalid minute string.')

        if TnS is not None:
            if '.' in TnS:
                seconds, floatseconds = cls._split_and_cast(TnS, 'Invalid second string.')
            else:
                seconds = cls.cast(TnS, int,
                                   thrownmessage='Invalid second string.')

        if floatweeks != 0:
            remainderweeks, remainderdays = cls._split_and_convert(floatweeks, 7)

            weeks += remainderweeks
            floatdays += remainderdays

        if floatdays != 0:
            remainderdays, remainderhours = cls._split_and_convert(floatdays, 24)

            days += remainderdays
            floathours += remainderhours

        if floathours != 0:
            remainderhours, remainderminutes = cls._split_and_convert(floathours, 60)

            hours += remainderhours
            floatminutes += remainderminutes

        if floatminutes != 0:
            remainderminutes, remainderseconds = cls._split_and_convert(floatminutes, 60)

            minutes += remainderminutes
            floatseconds += remainderseconds

        if floatseconds != 0:
            totalseconds = float(seconds) + floatseconds

            totalsecondsstr = cls._expand(totalseconds)

            if '.' in totalsecondsstr:
                secondsstr, remainderstr = totalsecondsstr.split('.')

                seconds = int(secondsstr)

                if len(remainderstr) >= 6:
                    microseconds = int(remainderstr[0:6])
                else:
                    microseconds = int(remainderstr + '0' * (6 - len(remainderstr)))
            else:
                seconds = int(totalseconds)

        return dateutil.relativedelta.relativedelta(years=years,
                                                    months=months,
                                                    weeks=weeks,
                                                    days=days,
                                                    hours=hours,
                                                    minutes=minutes,
                                                    seconds=seconds,
                                                    microseconds=microseconds)

    @staticmethod
    def _expand(f):
        #Expands a float into a decimal string
        #Based on _truncate from the PythonTimeBuilder
        floatstr = repr(f)

        if 'e' in floatstr or 'E' in floatstr:
            #Expand the exponent notation
            eindex = -1

            if 'e' in floatstr:
                eindex = floatstr.index('e')
            else:
                eindex = floatstr.index('E')

            exponent = int(floatstr[eindex + 1:])

            if exponent >= 0:
                return '{0:.{1}f}'.format(f, 0)
            else:
                #2 is a fudge factor to prevent rounding
                return '{0:.{1}f}'.format(f, abs(exponent) + 2)

        return floatstr
