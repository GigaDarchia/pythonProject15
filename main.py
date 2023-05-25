import requests
import json
import sqlite3
from win10toast import ToastNotifier

toaster = ToastNotifier()
key = "VNHUCFBRzd34JGLLzTfSladeRGFUCeO7ljQ47RWA"
url = "https://api.nasa.gov/planetary/apod"
payload = {'api_key': key, 'date': '2023-05-24'}

# request მოდულის ფუნქციები
response = requests.get(url, params=payload)
print(response)
print(response.url)
print(response.headers)
print(response.status_code)

# json ტიპის მონაცემის შენახვა .json ფორმატის ფაილში
result = response.json()

with open('nasa.json', 'w') as file:
    json.dump(result, file, indent=4)

# json-დან სასურველი ინფორმაციის გამოტანა
expl = result['explanation']
print(expl)

# ბაზის შექმნა/ბაზასთან დაკავშირება
conn = sqlite3.connect("nasa.sqlite")
cur = conn.cursor()

# ცხრილის შექმნა
cur.execute('''CREATE TABLE IF NOT EXISTS explanations
            (title explanation)
            ''')

# სასურველი ინფორმაციის ცხრილში შენახვა
cur.execute("INSERT INTO explanations (title) VALUES (?)", (expl,))

# ცვლილების ასახვა
conn.commit()
cur.close()

message = f"API-მ წამოიღო ინფორმაცია: {expl}"
toaster.show_toast(message, duration=5)
