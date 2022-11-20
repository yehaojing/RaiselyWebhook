import json
import requests
import pandas as pd
from datetime import datetime

limit = 25

page_id = "<page_id_here>"
access_token = "<access_token_here>"
url = f"https://graph.facebook.com/v15.0/{page_id}/posts?fields=insights.metric(post_impressions, post_reactions_by_type_total),created_time&limit={limit}&access_token={access_token}"

final_list = []
paginate = True
limit_max = 150
limit_sum = 0


while paginate or limit_sum >= limit_max:
    response = requests.get(url).json()
    print(url)
    print(json.dumps(response, indent="\t"))
    if "data" in response.keys():

        if response['paging']['next']:
            url = response['paging']['next']
        else:
            paginate = False

        data = [{
            "created_time": datetime.strptime(insight['created_time'], "%Y-%m-%dT%H:%M:%S+%f"),
            "post_impressions": insight['insights']['data'][0]['values'][0]['value'],
            "post_reactions": insight['insights']['data'][1]['values'][0]['value']
        } for insight in response['data']]

        limit_sum += limit

        final_list.extend(data)
    elif "error" in response.keys():
        paginate = False

df = pd.DataFrame(final_list)
df.to_csv("meta_insights.csv")

print(json.dumps(final_list, indent="\t", default=str))