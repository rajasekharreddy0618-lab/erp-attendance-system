import json

alerts = [
    {"ip": "10.0.0.15", "type": "Unauthorized SSH Access"},
    {"ip": "192.168.1.50", "type": "Port Scan Detected"}
]

#open file

with open("alerts.txt",mode="a",encoding="utf-8") as file:
    #Use for loop to iterate over alerts dictonary
    for data in alerts:
        ip=data.get("ip","Unknow IP")
        Threat_type=data.get("type","Unknown Threat")

        log_file=f"ALERT:[{Threat_type}] from IP:{ip}\n"
        #Append each lione to file
        file.write(log_file)

print("Alerts successfully saved to alert.txt!")
