import requests
import pandas as pd

url = "https://api.raisely.com/v3/donations?private=true&limit=1000sort=createdAt&order=desc"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <put_auth_token_here>"
}

final_list = []
paginate = True

while paginate:
    response = requests.get(url, headers=headers).json()
    data = [{
        "donation_amount": donation['amount']/100,
        "postcode": donation['user']['postcode'],
        "private": donation['user']["private"],
        "donation_datetime": donation["date"]
    } for donation in response['data']]

    idx = 0
    for row in data:
        if row["private"]:
            data[idx]["gender"] = row["private"].get('gender')
            data[idx]["dob"] = row["private"].get('dateOfBirth')
        else:
            data[idx]["gender"] = None
            data[idx]["dob"] = None
        data[idx].pop('private')
        idx += 1
    
    final_list.extend(data)

    if response.json()['pagination']['nextUrl']:
        url = response['pagination']['nextUrl']
    else:
        paginate = False

df = pd.DataFrame(final_list)
df.to_csv("raisely_donation.csv")