# -*- coding: utf-8 -*-

# Copyright (c) 2019, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import unittest
import dateutil.relativedelta

from aniso8601 import compat
from aniso8601.utcoffset import UTCOffset
from relativetimebuilder import RelativeTimeBuilder, RelativeValueError

class TestRelativeTimeBuilder(unittest.TestCase):
    def test_build_duration(self):
        testtuples = (({'PnY': '1'},
                       dateutil.relativedelta.relativedelta(years=1)),
                      ({'PnM': '1'},
                      #Add the relative ‘days’ argument to the absolute day. Notice that the ‘weeks’ argument is multiplied by 7 and added to ‘days’.
                      #http://dateutil.readthedocs.org/en/latest/relativedelta.html
                       dateutil.relativedelta.relativedelta(months=1)),
                      ({'PnW': '1'},
                       dateutil.relativedelta.relativedelta(days=7)),
                      ({'PnW': '1.5'},
                       dateutil.relativedelta.relativedelta(days=10, hours=12)),
                      ({'PnD': '1'},
                       dateutil.relativedelta.relativedelta(days=1)),
                      ({'PnD': '1.5'},
                       dateutil.relativedelta.relativedelta(days=1, hours=12)),
                      ({'PnY': '1', 'PnM': '2', 'PnD': '3'},
                       dateutil.relativedelta.relativedelta(years=1, months=2,
                                                            days=3)),
                      ({'PnY': '1', 'PnM': '2', 'PnD': '3.5'},
                       dateutil.relativedelta.relativedelta(years=1, months=2,
                                                            days=3, hours=12)),
                      ({'PnY': '1', 'PnM': '2', 'PnD': '3',
                        'TnH': '4', 'TnM': '54', 'TnS': '6.5'},
                       dateutil.relativedelta.relativedelta(years=1, months=2,
                                                            days=3, hours=4,
                                                            minutes=54,
                                                            seconds=6,
                                                            microseconds=
                                                            500000)),
                      ({'PnY': '0003', 'PnM': '06', 'PnD': '04',
                        'TnH': '12', 'TnM': '30', 'TnS': '05'},
                       dateutil.relativedelta.relativedelta(years=3, months=6,
                                                            days=4, hours=12,
                                                            minutes=30,
                                                            seconds=5)),
                      ({'PnY': '0003', 'PnM': '06', 'PnD': '04',
                        'TnH': '12', 'TnM': '30', 'TnS': '05.5'},
                       dateutil.relativedelta.relativedelta(years=3, months=6,
                                                            days=4, hours=12,
                                                            minutes=30,
                                                            seconds=5,
                                                            microseconds=
                                                            500000)),
                      ({'TnH': '4', 'TnM': '54', 'TnS': '6.5'},
                       dateutil.relativedelta.relativedelta(hours=4,
                                                            minutes=54,
                                                            seconds=6,
                                                            microseconds=
                                                            500000)),
                      ({'TnH': '4', 'TnM': '54', 'TnS': '28.512400'},
                       dateutil.relativedelta.relativedelta(hours=4,
                                                            minutes=54,
                                                            seconds=28,
                                                            microseconds=
                                                            512400)),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      ({'PnW': '1.9999999999999999'},
                       dateutil.relativedelta.relativedelta(days=13, hours=23,
                                                            minutes=59,
                                                            seconds=59,
                                                            microseconds=
                                                            999999)),
                      ({'PnD': '1.9999999999999999'},
                       dateutil.relativedelta.relativedelta(days=1, hours=23,
                                                            minutes=59,
                                                            seconds=59,
                                                            microseconds=
                                                            999999)),
                      ({'TnH': '14.9999999999999999'},
                       dateutil.relativedelta.relativedelta(hours=14,
                                                            minutes=59,
                                                            seconds=59,
                                                            microseconds=
                                                            999999)),
                      ({'TnM': '0.00000000999'},
                       dateutil.relativedelta.relativedelta(0)),
                      ({'TnM': '0.0000000999'},
                       dateutil.relativedelta.relativedelta(microseconds=5)),
                      ({'TnS': '0.0000001'},
                       dateutil.relativedelta.relativedelta(0)),
                      ({'TnS': '2.0000048'},
                       dateutil.relativedelta.relativedelta(seconds=2,
                                                            microseconds=4)),
                      ({'PnY': '0001', 'PnM': '02', 'PnD': '03',
                        'TnH': '14', 'TnM': '43', 'TnS': '59.9999997'},
                       dateutil.relativedelta.relativedelta(years=1, months=2,
                                                            days=3, hours=14,
                                                            minutes=43,
                                                            seconds=59,
                                                            microseconds=
                                                            999999)),
                      ({'PnY': '1', 'PnM': '2', 'PnW': '4', 'PnD': '3',
                        'TnH': '5', 'TnM': '6', 'TnS': '7.0000091011'},
                       dateutil.relativedelta.relativedelta(years=1, months=2,
                                                            days=31, hours=5,
                                                            minutes=6,
                                                            seconds=7,
                                                            microseconds=9)))

        for testtuple in testtuples:
            result = RelativeTimeBuilder.build_duration(**testtuple[0])
            self.assertEqual(result, testtuple[1])

    def test_build_duration_fractional_year(self):
        with self.assertRaises(RelativeValueError):
            RelativeTimeBuilder.build_duration(PnY='1.5')

    def test_build_duration_fractional_month(self):
        with self.assertRaises(RelativeValueError):
            RelativeTimeBuilder.build_duration(PnM='1.5')

    def test_build_duration_nodateutil(self):
        import sys
        import dateutil

        dateutil_import = dateutil

        sys.modules['dateutil'] = None

        with self.assertRaises(RuntimeError):
            RelativeTimeBuilder.build_duration()

        #Reinstall dateutil
        sys.modules['dateutil'] = dateutil_import

    def test_build_interval(self):
        #Intervals are contingent on durations, make sure they work
        #<duration>/<end>
        testtuples = (({'end': (('1981', '04', '05', None, None, None, 'date'),
                                ('01', '01', '00', None, 'time'), 'datetime'),
                        'duration': (None, '1', None, None, None, None, None,
                                     'duration')},
                       datetime.datetime(year=1981, month=4, day=5,
                                         hour=1, minute=1),
                       datetime.datetime(year=1981, month=3, day=5,
                                         hour=1, minute=1)),
                      ({'end': ('1981', '04', '05', None, None, None, 'date'),
                        'duration': (None, '1', None, None, None, None, None,
                                     'duration')},
                       datetime.date(year=1981, month=4, day=5),
                       datetime.date(year=1981, month=3, day=5)),
                      ({'end': ('2014', '11', '12', None, None, None, 'date'),
                        'duration': (None, None, None, None, '1', None, None,
                                     'duration')},
                       datetime.date(year=2014, month=11, day=12),
                       datetime.datetime(year=2014, month=11, day=11,
                                         hour=23)),
                      ({'end': ('2014', '11', '12', None, None, None, 'date'),
                        'duration': (None, None, None, None, '4', '54', '6.5',
                                     'duration')},
                       datetime.date(year=2014, month=11, day=12),
                       datetime.datetime(year=2014, month=11, day=11,
                                         hour=19, minute=5, second=53,
                                         microsecond=500000)),
                      ({'end': (('2050', '03', '01',
                                 None, None, None, 'date'),
                                ('13', '00', '00',
                                 (False, True, None, None,
                                  'Z', 'timezone'), 'time'), 'datetime'),
                        'duration': (None, None, None,
                                     None, '10', None, None, 'duration')},
                       datetime.datetime(year=2050, month=3, day=1,
                                         hour=13,
                                         tzinfo=UTCOffset(name='UTC',
                                                          minutes=0)),
                       datetime.datetime(year=2050, month=3, day=1,
                                         hour=3,
                                         tzinfo=UTCOffset(name='UTC',
                                                          minutes=0))),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      #https://bitbucket.org/nielsenb/aniso8601/issues/21/sub-microsecond-precision-is-lost-when
                      ({'end': ('1989', '03', '01',
                                None, None, None, 'date'),
                        'duration': (None, None, '1.9999999999999999',
                                     None, None, None,
                                     None, 'duration')},
                       datetime.date(year=1989, month=3, day=1),
                       datetime.datetime(year=1989, month=2, day=15,
                                         hour=0, minute=0, second=0,
                                         microsecond=1)),
                      ({'end': ('1989', '03', '01',
                                None, None, None, 'date'),
                        'duration': (None, None, None,
                                     '1.9999999999999999', None, None,
                                     None, 'duration')},
                       datetime.date(year=1989, month=3, day=1),
                       datetime.datetime(year=1989, month=2, day=27,
                                         hour=0, minute=0, second=0,
                                         microsecond=1)),
                      ({'end': ('2001', '01', '01',
                                None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, '14.9999999999999999', None,
                                     None, 'duration')},
                       datetime.date(year=2001, month=1, day=1),
                       datetime.datetime(year=2000, month=12, day=31,
                                         hour=9, minute=0, second=0,
                                         microsecond=1)),
                      ({'end': ('2001', '01', '01',
                                None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, '0.00000000999',
                                     None, 'duration')},
                       datetime.date(year=2001, month=1, day=1),
                       datetime.datetime(year=2001, month=1, day=1)),
                      ({'end': ('2001', '01', '01',
                                None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, '0.0000000999',
                                     None, 'duration')},
                       datetime.date(year=2001, month=1, day=1),
                       datetime.datetime(year=2000, month=12, day=31,
                                         hour=23, minute=59, second=59,
                                         microsecond=999995)),
                      ({'end': ('2018', '03', '06', None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, None,
                                     '0.0000001', 'duration')},
                       datetime.date(year=2018, month=3, day=6),
                       datetime.datetime(year=2018, month=3, day=6)),
                      ({'end': ('2018', '03', '06', None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, None,
                                     '2.0000048', 'duration')},
                       datetime.date(year=2018, month=3, day=6),
                       datetime.datetime(year=2018, month=3, day=5,
                                         hour=23, minute=59, second=57,
                                         microsecond=999996)),
                      #<start>/<duration>
                      ({'start': ('2018', '03', '06',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, None,
                                     '0.0000001', 'duration')},
                       datetime.date(year=2018, month=3, day=6),
                       datetime.datetime(year=2018, month=3, day=6)),
                      ({'start': ('2018', '03', '06',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, None,
                                     '2.0000048', 'duration')},
                       datetime.date(year=2018, month=3, day=6),
                       datetime.datetime(year=2018, month=3, day=6,
                                         hour=0, minute=0, second=2,
                                         microsecond=4)),
                      ({'start': (('1981', '04', '05',
                                   None, None, None, 'date'),
                                  ('01', '01', '00', None, 'time'),
                                  'datetime'),
                        'duration': (None, '1', None,
                                     '1', None, '1', None, 'duration')},
                       datetime.datetime(year=1981, month=4, day=5,
                                         hour=1, minute=1),
                       datetime.datetime(year=1981, month=5, day=6,
                                         hour=1, minute=2)),
                      ({'start': ('1981', '04', '05',
                                  None, None, None, 'date'),
                        'duration': (None, '1', None,
                                     '1', None, None, None, 'duration')},
                       datetime.date(year=1981, month=4, day=5),
                       datetime.date(year=1981, month=5, day=6)),
                      ({'start': ('2014', '11', '12',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, '1', None, None, 'duration')},
                       datetime.date(year=2014, month=11, day=12),
                       datetime.datetime(year=2014, month=11, day=12,
                                         hour=1, minute=0)),
                      ({'start': ('2014', '11', '12',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, '4', '54', '6.5', 'duration')},
                       datetime.date(year=2014, month=11, day=12),
                       datetime.datetime(year=2014, month=11, day=12,
                                         hour=4, minute=54, second=6,
                                         microsecond=500000)),
                      ({'start': ('2014', '11', '12',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, '4', '54', '6.5', 'duration')},
                       datetime.date(year=2014, month=11, day=12),
                       datetime.datetime(year=2014, month=11, day=12,
                                         hour=4, minute=54, second=6,
                                         microsecond=500000)),
                      ({'start': (('2050', '03', '01',
                                   None, None, None, 'date'),
                                  ('13', '00', '00',
                                   (False, True, None, None,
                                    'Z', 'timezone'), 'time'), 'datetime'),
                        'duration': (None, None, None,
                                     None, '10', None, None, 'duration')},
                       datetime.datetime(year=2050, month=3, day=1,
                                         hour=13,
                                         tzinfo=UTCOffset(name='UTC',
                                                          minutes=0)),
                       datetime.datetime(year=2050, month=3, day=1,
                                         hour=23,
                                         tzinfo=UTCOffset(name='UTC',
                                                          minutes=0))),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      #https://bitbucket.org/nielsenb/aniso8601/issues/21/sub-microsecond-precision-is-lost-when
                      ({'start': ('1989', '03', '01',
                                  None, None, None, 'date'),
                        'duration': (None, None, '1.9999999999999999',
                                     None, None, None,
                                     None, 'duration')},
                       datetime.date(year=1989, month=3, day=1),
                       datetime.datetime(year=1989, month=3, day=14,
                                         hour=23, minute=59, second=59,
                                         microsecond=999999)),
                      ({'start': ('1989', '03', '01',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     '1.9999999999999999', None, None,
                                     None, 'duration')},
                       datetime.date(year=1989, month=3, day=1),
                       datetime.datetime(year=1989, month=3, day=2,
                                         hour=23, minute=59, second=59,
                                         microsecond=999999)),
                      ({'start': ('2001', '01', '01',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, '14.9999999999999999', None,
                                     None, 'duration')},
                       datetime.date(year=2001, month=1, day=1),
                       datetime.datetime(year=2001, month=1, day=1,
                                         hour=14, minute=59, second=59,
                                         microsecond=999999)),
                      ({'start': ('2001', '01', '01',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, '0.00000000999',
                                     None, 'duration')},
                       datetime.date(year=2001, month=1, day=1),
                       datetime.datetime(year=2001, month=1, day=1)),
                      ({'start': ('2001', '01', '01',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, '0.0000000999',
                                     None, 'duration')},
                       datetime.date(year=2001, month=1, day=1),
                       datetime.datetime(year=2001, month=1, day=1,
                                         hour=0, minute=0, second=0,
                                         microsecond=5)),
                      ({'start': ('2018', '03', '06',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, None,
                                     '0.0000001', 'duration')},
                       datetime.date(year=2018, month=3, day=6),
                       datetime.datetime(year=2018, month=3, day=6)),
                      ({'start': ('2018', '03', '06',
                                  None, None, None, 'date'),
                        'duration': (None, None, None,
                                     None, None, None,
                                     '2.0000048', 'duration')},
                       datetime.date(year=2018, month=3, day=6),
                       datetime.datetime(year=2018, month=3, day=6,
                                         hour=0, minute=0, second=2,
                                         microsecond=4)),
                      #<start>/<end>
                      ({'start': (('1980', '03', '05',
                                   None, None, None, 'date'),
                                  ('01', '01', '00', None, 'time'),
                                  'datetime'),
                        'end': (('1981', '04', '05',
                                 None, None, None, 'date'),
                                ('01', '01', '00', None, 'time'),
                                'datetime')},
                       datetime.datetime(year=1980, month=3, day=5,
                                         hour=1, minute=1),
                       datetime.datetime(year=1981, month=4, day=5,
                                         hour=1, minute=1)),
                      ({'start': (('1980', '03', '05',
                                   None, None, None, 'date'),
                                  ('01', '01', '00', None, 'time'),
                                  'datetime'),
                        'end': ('1981', '04', '05', None, None, None, 'date')},
                       datetime.datetime(year=1980, month=3, day=5,
                                         hour=1, minute=1),
                       datetime.date(year=1981, month=4, day=5)),
                      ({'start': ('1980', '03', '05',
                                  None, None, None, 'date'),
                        'end': (('1981', '04', '05',
                                 None, None, None, 'date'),
                                ('01', '01', '00', None, 'time'),
                                'datetime')},
                       datetime.date(year=1980, month=3, day=5),
                       datetime.datetime(year=1981, month=4, day=5,
                                         hour=1, minute=1)),
                      ({'start': ('1980', '03', '05',
                                  None, None, None, 'date'),
                        'end': ('1981', '04', '05',
                                None, None, None, 'date')},
                       datetime.date(year=1980, month=3, day=5),
                       datetime.date(year=1981, month=4, day=5)),
                      ({'start': ('1981', '04', '05',
                                  None, None, None, 'date'),
                        'end': ('1980', '03', '05',
                                None, None, None, 'date')},
                       datetime.date(year=1981, month=4, day=5),
                       datetime.date(year=1980, month=3, day=5)),
                      ({'start': (('2050', '03', '01',
                                   None, None, None, 'date'),
                                  ('13', '00', '00',
                                   (False, True, None, None,
                                    'Z', 'timezone'), 'time'), 'datetime'),
                        'end': (('2050', '05', '11',
                                 None, None, None, 'date'),
                                ('15', '30', '00',
                                 (False, True, None, None,
                                  'Z', 'timezone'), 'time'), 'datetime')},
                       datetime.datetime(year=2050, month=3, day=1,
                                         hour=13,
                                         tzinfo=UTCOffset(name='UTC',
                                                          minutes=0)),
                       datetime.datetime(year=2050, month=5, day=11,
                                         hour=15, minute=30,
                                         tzinfo=UTCOffset(name='UTC',
                                                          minutes=0))),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      ({'start': (('1980', '03', '05',
                                   None, None, None, 'date'),
                                  ('01', '01', '00.0000001',
                                   None, 'time'), 'datetime'),
                        'end': (('1981', '04', '05',
                                 None, None, None, 'date'),
                                ('14', '43', '59.9999997', None, 'time'),
                                'datetime')},
                       datetime.datetime(year=1980, month=3, day=5,
                                         hour=1, minute=1),
                       datetime.datetime(year=1981, month=4, day=5,
                                         hour=14, minute=43, second=59,
                                         microsecond=999999)),
                      #Some relativedelta examples
                      #http://dateutil.readthedocs.org/en/latest/examples.html#relativedelta-examples
                      ({'start': ('2003', '1', '27',
                                  None, None, None, 'date'),
                        'duration': (None, '1', None,
                                     None, None, None, None, 'duration')},
                       datetime.date(year=2003, month=1, day=27),
                       datetime.date(year=2003, month=2, day=27)),
                      ({'start': ('2003', '1', '31',
                                  None, None, None, 'date'),
                        'duration': (None, '1', None,
                                     None, None, None, None, 'duration')},
                       datetime.date(year=2003, month=1, day=31),
                       datetime.date(year=2003, month=2, day=28)),
                      ({'start': ('2003', '1', '31',
                                  None, None, None, 'date'),
                        'duration': (None, '2', None,
                                     None, None, None, None, 'duration')},
                       datetime.date(year=2003, month=1, day=31),
                       datetime.date(year=2003, month=3, day=31)),
                      ({'start': ('2000', '2', '28',
                                  None, None, None, 'date'),
                        'duration': ('1', None, None,
                                     None, None, None, None, 'duration')},
                       datetime.date(year=2000, month=2, day=28),
                       datetime.date(year=2001, month=2, day=28)),
                      ({'start': ('1999', '2', '28',
                                  None, None, None, 'date'),
                        'duration': ('1', None, None,
                                     None, None, None, None, 'duration')},
                       datetime.date(year=1999, month=2, day=28),
                       datetime.date(year=2000, month=2, day=28)),
                      ({'start': ('1999', '3', '1',
                                  None, None, None, 'date'),
                        'duration': ('1', None, None,
                                     None, None, None, None, 'duration')},
                       datetime.date(year=1999, month=3, day=1),
                       datetime.date(year=2000, month=3, day=1)),
                      ({'end': ('2001', '2', '28',
                                None, None, None, 'date'),
                        'duration': ('1', None, None,
                                     None, None, None, None, 'duration')},
                       datetime.date(year=2001, month=2, day=28),
                       datetime.date(year=2000, month=2, day=28)),
                      ({'end': ('2001', '3', '1',
                                None, None, None, 'date'),
                        'duration': ('1', None, None,
                                     None, None, None, None, 'duration')},
                       datetime.date(year=2001, month=3, day=1),
                       datetime.date(year=2000, month=3, day=1)))

        for testtuple in testtuples:
            result = RelativeTimeBuilder.build_interval(**testtuple[0])
            self.assertEqual(result[0], testtuple[1])
            self.assertEqual(result[1], testtuple[2])

    def test_build_repeating_interval(self):
        #Repeating intervals are contingent on durations, make sure they work
        args = {'Rnn': '3', 'interval': (('1981', '04', '05',
                                          None, None, None, 'date'),
                                         None,
                                         (None, None, None,
                                          '1', None, None,
                                          None, 'duration'),
                                         'interval')}
        results = list(RelativeTimeBuilder.build_repeating_interval(**args))

        self.assertEqual(results[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(results[1], datetime.date(year=1981, month=4, day=6))
        self.assertEqual(results[2], datetime.date(year=1981, month=4, day=7))

        args = {'Rnn': '11', 'interval': (None,
                                          (('1980', '03', '05',
                                            None, None, None, 'date'),
                                           ('01', '01', '00',
                                            None, 'time'), 'datetime'),
                                          (None, None, None,
                                           None, '1', '2',
                                           None, 'duration'),
                                          'interval')}
        results = list(RelativeTimeBuilder.build_repeating_interval(**args))

        for dateindex in compat.range(0, 11):
            self.assertEqual(results[dateindex],
                             datetime.datetime(year=1980, month=3, day=5,
                                               hour=1, minute=1)
                             - dateindex * datetime.timedelta(hours=1,
                                                              minutes=2))

        #Make sure relative is correctly applied for months
        #https://bitbucket.org/nielsenb/aniso8601/issues/12/month-intervals-calculated-incorrectly-or
        args = {'Rnn': '4', 'interval': ((('2017', '04', '30',
                                           None, None, None, 'date'),
                                          ('00', '00', '00',
                                           None, 'time'), 'datetime'),
                                         None,
                                         (None, '1', None,
                                          None, None, None, None, 'duration'),
                                         'interval')}
        results = list(RelativeTimeBuilder.build_repeating_interval(**args))

        self.assertEqual(results[0],
                         datetime.datetime(year=2017, month=4, day=30))
        self.assertEqual(results[1],
                         datetime.datetime(year=2017, month=5, day=30))
        self.assertEqual(results[2],
                         datetime.datetime(year=2017, month=6, day=30))
        self.assertEqual(results[3],
                         datetime.datetime(year=2017, month=7, day=30))

        args = {'R': True, 'interval': (None,
                                        (('1980', '03', '05',
                                          None, None, None, 'date'),
                                         ('01', '01', '00',
                                          None, 'time'), 'datetime'),
                                        (None, None, None,
                                         None, '1', '2', None, 'duration'),
                                        'interval')}
        resultgenerator = RelativeTimeBuilder.build_repeating_interval(**args)

        for dateindex in compat.range(0, 11):
            self.assertEqual(next(resultgenerator),
                             datetime.datetime(year=1980, month=3, day=5,
                                               hour=1, minute=1)
                             - dateindex * datetime.timedelta(hours=1,
                                                              minutes=2))

    def test_expand(self):
        self.assertEqual(RelativeTimeBuilder._expand(0), '0')
        self.assertEqual(RelativeTimeBuilder._expand(1.0), '1.0')
        self.assertEqual(RelativeTimeBuilder._expand(0.1), '0.1')
        self.assertEqual(RelativeTimeBuilder._expand(0.01), '0.01')
        self.assertEqual(RelativeTimeBuilder._expand(1e10), '10000000000.0')
        self.assertEqual(RelativeTimeBuilder._expand(1e-10), '0.000000000100')
        self.assertEqual(RelativeTimeBuilder._expand(0.0000000001), '0.000000000100')
        self.assertEqual(RelativeTimeBuilder._expand(0.9999999999), '0.9999999999')
        self.assertEqual(RelativeTimeBuilder._expand(0.000095), '0.0000950')
        self.assertEqual(RelativeTimeBuilder._expand(0.00006), '0.0000600')
        self.assertEqual(RelativeTimeBuilder._expand(0.00005), '0.0000500')
        self.assertEqual(RelativeTimeBuilder._expand(0.000005), '0.00000500')
        self.assertEqual(RelativeTimeBuilder._expand(0.00000051), '0.000000510')
        self.assertEqual(RelativeTimeBuilder._expand(28.512400), '28.5124')
