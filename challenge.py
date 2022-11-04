import requests
import auth

def apiGET():
    return requests.get("https://api.slangapp.com/challenges/v1/activities", 
    headers={"Authorization": auth.KEY})

def apiPOST(user_sessions):
    requests.post("https://api.slangapp.com/challenges/v1/activities/sessions",
    headers={"Authorization": auth.KEY}, # ← replace with your key
    json=user_sessions) # Keep in mind this should be a dictionary {“user_sessions”: {...}}

def build_user_sessions(data):
    print(data)

if __name__ == "__main__":
    build_user_sessions('hello')