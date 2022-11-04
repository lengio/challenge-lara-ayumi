import requests
import auth
import example

def apiGET():
    req = requests.get("https://api.slangapp.com/challenges/v1/activities", 
    headers={"Authorization": auth.KEY})
    
    return req
    # status = req.status_code

    # if (status == 200):
    #     return req
    # else:
    #     print(status)
    #     req.close()
    #     exit()

def apiGETDummy():
    return example.EXAMPLE

def apiPOST(user_sessions):
    try:
        requests.post("https://api.slangapp.com/challenges/v1/activities/sessions",
        headers={"Authorization": auth.KEY}, # ← replace with your key
        json=user_sessions) # Keep in mind this should be a dictionary {“user_sessions”: {...}}

    except Exception as e:
        print(e.args[0])
        exit()

def build_user_sessions(data):
    data_storage = {}
    
    # Linear time
    for activity in data["activities"]:
        obj = {
            'id': activity['id'],
            'answered_at': activity['answered_at'],
            'first_seen_at': activity['first_seen_at'],
        }

        try:
            q = data_storage[activity["user_id"]]
        except KeyError:
            q = []

        q.append(obj)
        data_storage[activity["user_id"]] = q
    
    print(data_storage)

if __name__ == "__main__":
    # activities_response = apiGET()
    # build_user_sessions(activities_response.json())

    build_user_sessions(apiGETDummy())