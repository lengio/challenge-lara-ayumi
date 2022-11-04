import requests
import datetime
import auth
import example


MAX_SEC = datetime.timedelta(seconds=300)
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

def apiGET():
    req = requests.get("https://api.slangapp.com/challenges/v1/activities", 
    headers={"Authorization": auth.KEY})
    
    status = req.status_code

    if (status == 200):
        return req
    else:
        print(status)
        req.close()
        exit()

def apiGETDummy():
    return example.EXAMPLE

def apiPOST(user_sessions):
    req = requests.post("https://api.slangapp.com/challenges/v1/activities/sessions",
    headers={"Authorization": auth.KEY}, # ← replace with your key
    json=user_sessions) # Keep in mind this should be a dictionary {“user_sessions”: {...}}
    
    status = req.status_code

    if (status == 204):
        print('DONE!')
    else:
        print(status)
        req.close()
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
    
    user_sessions = {}
    
    for user in data_storage:
        sortedlist = sorted(data_storage[user], key=lambda d: d["first_seen_at"]) # nlogn

        # Logging logic
        new_obj = {
            "ended_at": sortedlist[0]["answered_at"],
            "started_at": sortedlist[0]["first_seen_at"],
            "activity_ids": [sortedlist[0]["id"]],
        }

        userActList = []
        
        for entry in sortedlist:
            if(entry["id"] != sortedlist[0]["id"]):
                elapsed_time = strToDatetime(entry["first_seen_at"]) - strToDatetime(new_obj["ended_at"])

                if (elapsed_time > MAX_SEC):
                    new_obj["duration_seconds"] = \
                        (strToDatetime(new_obj["ended_at"]) - strToDatetime(new_obj["started_at"])).total_seconds()

                    userActList.append(new_obj.copy())

                    new_obj = {
                        "ended_at": entry["answered_at"],
                        "started_at": entry["first_seen_at"],
                        "activity_ids": [entry["id"]]
                    }
                else:
                    new_obj["activity_ids"].append(entry["id"])
                    new_obj["ended_at"] = entry["answered_at"]

        new_obj["duration_seconds"] = \
            (strToDatetime(new_obj["ended_at"]) - strToDatetime(new_obj["started_at"])).total_seconds()

        userActList.append(new_obj)

        user_sessions[user] = userActList

    print(user_sessions)
    return user_sessions

def strToDatetime(str):
    return datetime.datetime.strptime(str, DATETIME_FORMAT)

if __name__ == "__main__":
    activities_response = apiGET()
    user_sessions = {"user_sessions": build_user_sessions(activities_response.json())}
    apiPOST(user_sessions)