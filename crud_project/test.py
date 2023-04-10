import requests

BASE= "http://127.0.0.1:5000/"


#test to confirm that a user is created succesfully to the database 
response = requests.put(BASE + "list_users/1",{"name": "Atieno","nationality": "Kenyan", "career":"Software Engineer","age":23})
print(response.json())

input()


#test to confirm that the user created can be retrived
response = requests.get(BASE + "list_users/1",)
print(response.json())


#test to confirm that existing user can be deleted
#in memory data store to helpin testing the delete and update operations
system_user=[{"name":"Jeff","nationality":"Kenya","career":"architect","age":11},
             {"name":"Barrack","nationality":"Ghanian","career":"Artist","age":10},
             {"name":"Milka","nationality":"Ugandan","career":"Product Designer","age":41},
             {"name":"Bestie","nationality":"Senagalese","career":"UX Researcher","age":25},
             {"name":"Seal","nationality":"Egyptian","career":"Farming","age":24}
             ]
for user in range(len(system_user)):
    response = requests.put(BASE + "list_users/" +str(user),system_user[user])
    print (response)
    
response= requests.delete(BASE + "list_users/2")

#expected to delete Milka from system users