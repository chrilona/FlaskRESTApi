import requests

BASE= "http://127.0.0.1:5000/"

#response = requests.get(BASE + "users/1",{"name": "Atieno","nationality": "Kenyan", "career":"Software Engineer","age":23})
#print(response.json())
#input()

response = requests.get(BASE + "users/1",)
print(response.json())