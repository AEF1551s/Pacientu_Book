# from datetime import datetime, timedelta
#
# def datetime_delta(hour1, minute1, hour2, minute2, interval): #parametri, kuros var mainīt laika intervālu???
#     def datetime_range(start, end, delta):
#         while start < end:
#             start += delta
#
#     dts = [dt.strftime('%Y/%m/%d %H:%M') for dt in
#            datetime_range(datetime(2016, 9, 1, hour1, minute1), datetime(2016, 9, 1, hour2, minute2 + 15),  # year, month, day, hour, minute, second
#                 timedelta(minutes=interval))]

#NOT IN USE, BECAUSE DATETIME FORMAT, TIME TO, TIME FROM, AND CALENDAR TIME FORMAT IS NOT IDEAL FOR STORING IN SQLITE3 .DB FILES.
# . INSTEAD A HARDCODED LIST OF VALUES ARE USED. IN THE FUTURE TIME INTERVAL, END AND START COULD BE CHANGED.
