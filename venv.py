import requests

def check_ip_threat(ip_address:str)->dict:
    url=f"https://ipapi.co/{ip_address}/json"
    response=requests.get(url,"timeout=5")
    try:
        if response.status_code==200:
            data=response.json()
            return{
                "ip":ip_address,
                "city":data.get("city"),
                "org":data.get("org")
            }
        else:
           return {"error": "Failed to fetch threat intelligence"}
        
    except requests.exception.RequestsExpceptions as err:
        return {"Network failure!!{err}"}
    
print(check_ip_threat("8.8.8.8"))
