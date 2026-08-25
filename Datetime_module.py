from datetime import datetime,timezone,timedelta

issued_time="2026-07-29 18:00:00"

pairse_time=datetime.strptime(issued_time,"%Y-%m-%d %H:%M:%S")#Parise time

Expire_time=pairse_time+timedelta(hours=2) #using timedelta for add hours

print("Before parsing type of time",type(issued_time))
print("parsied time=",pairse_time)
print("After parsing time",type(pairse_time))

print("Session expire at:",Expire_time)