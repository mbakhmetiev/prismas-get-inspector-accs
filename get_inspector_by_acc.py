import requests
import os
import jmespath
import pandas as pd

pd.set_option('display.max_colwidth', None)

url = "https://api0.prismacloud.io/search/config"

token = os.getenv("prisma_token")

headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': 'application/json; charset=UTF-8',
  'x-redlock-auth': token
}

payload = "{\r\n  \"query\":\"config from cloud.resource where cloud.type = 'aws' AND api.name = 'aws-region'\",\r\n  \"timeRange\":{\"type\":\"to_now\",\"value\":\"epoch\"},\r\n    \"heuristicSearch\":true\r\n}"

response = requests.request("POST", url, headers=headers, data=payload)
json_data = response.json()
accounts = set(jmespath.search("data.items[*].accountName", json_data))

payload = "{\r\n  \"query\":\"config from cloud.resource where finding.source = 'AWS Inspector'\",\r\n  \"timeRange\":{\"type\":\"to_now\",\"value\":\"epoch\"},\r\n    \"heuristicSearch\":true\r\n}"

response = requests.request("POST", url, headers=headers, data=payload)
json_data = response.json()
inspector_accs = set(jmespath.search("data.items[*].accountName", json_data))

with open (f"inspector_accs.txt", 'w') as f:
  f.write("TOTAL ACCOUNTS:\n{0} \
          \nACCOUNTS WITH INSPECTOR:\n{1} \
          \nACCOUNTS W/O INSPECTOR:\n{2}" \
          .format('\n'.join(accounts), \
                  '\n'.join(inspector_accs), \
                  '\n'.join(accounts.difference(inspector_accs))))
