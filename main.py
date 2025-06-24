import json
import requests
import matplotlib

# Required for getting access. Format: <client name>/<version> (<contact information>) <library/framework name>/<version>
header = {
    "User-Agent": "gcc-project/v1 (Johnsterbravo)"
}

# Links below can also be accessed in the browser to see the data
# Get monthly page views for the English page of Undertale from 2015-09-01 to 2025-06-20
undertale_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/Undertale/monthly/20150901/20250620'

# Get monthly page views for the English page of Deltarune from 2018-10-01 to 2025-06-20
deltarune_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/Deltarune/monthly/20181001/20250620'

# Responses
undertale_response = requests.get(undertale_url, headers=header)
deltarune_response = requests.get(deltarune_url, headers=header)

# JSON with data
undertale_dict = undertale_response.json()
deltarune_dict = deltarune_response.json()

# Save data in json files
with open('data/undertale.json', 'w') as file:
    json.dump(undertale_dict, file)

with open('data/deltarune.json', 'w') as file:
    json.dump(deltarune_dict, file)