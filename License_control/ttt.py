import datetime as td

s = '2019-12-16'
now = td.datetime.now()
future_time = td.datetime.strptime(s, '%Y-%m-%d')

res = future_time - now
print(res.days)
