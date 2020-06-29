from datetime import datetime, timedelta
import math

def datetime_range(start, end, delta):
    while start < end:
        yield start
        start += delta

dts = [dt.strftime('%Y-%m-%d %H:%M') for dt in
       datetime_range(datetime(2016, 9, 1, 7, 0), datetime(2016, 9, 1, 18, 0+15),    #year, month, day, hour, minute, second
       timedelta(minutes=15))]
print(dts)  #2016-09-01 09:00
dts_len=len(dts)
print(len(dts))

rows = math.sqrt(dts_len)
rup = math.ceil(rows)
for x in range(2):
    #print(x)
    for y in range(3):
        print(y)

        print()
        #0-0, 0-1, 0,2... 1-0, 1-1.. sanāk pirmā rinda  un visas kollonas, otrā rinda un visas kolonnas
        #katrai x vērtībai no 0 līdz 3  atbilst  y vērtības no 0 līdz 5.
