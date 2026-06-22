
import requests
import pandas
url="https://api.mfapi.in/mf/125497"
response=requests.get(url)
data=response.json()
nav_data=data['data']
df=pandas.DataFrame(nav_data)
print(df.head())
print(df.shape)
df.to_csv("C:/Users/user/mutual-fund-analytics/data/raw/hdfc_top100_nav.csv", index=False)
print("saved succesfully")


import requests
import pandas as pd

funds = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for name, code in funds.items():
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)
    data = response.json()
    
    nav_data = data['data']
    df = pd.DataFrame(nav_data)
    
    print(f"{name}: {df.shape}")
    
    df.to_csv(f"C:/Users/user/mutual-fund-analytics/data/raw/{name}_nav.csv", index=False)

print("All 5 funds saved!")
