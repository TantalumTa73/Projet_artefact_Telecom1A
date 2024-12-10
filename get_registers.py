import requests

url = "http://proj103.r2.enst.fr"

for i in range(5):
    for j in range(5):
        print(f"Équipe {i+1}, Registre {j+1}")
        r = requests.get(url+f"/api/udta?idx={j+1}&t={i+1}")
        try:
            print(json.dumps(r.json(),indent=4))
        except:
            print(r.content.decode('utf-8'))
