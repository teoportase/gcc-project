# -----------------------------------------------------------------------------------------------------------------------
#                                                    Libraries
# -----------------------------------------------------------------------------------------------------------------------
import json
import requests
import matplotlib as plt

# -----------------------------------------------------------------------------------------------------------------------
#                                                Getting the data
# -----------------------------------------------------------------------------------------------------------------------


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

# Dictionaries with data
undertale_dict = undertale_response.json()
deltarune_dict = deltarune_response.json()

# -----------------------------------------------------------------------------------------------------------------------
#                                                   Functions
# -----------------------------------------------------------------------------------------------------------------------

# Format the dates from the data into more readable dates
def format_date(date):
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    year = date[0:4]
    month = date[4:6]

    new_date = months[int(month)-1] + " " + year

    return new_date

# Add values from a dictionary to another based on a timestamp
def add_values(data, key, dictionary):
    for item in dictionary["items"]:
        date = format_date(item["timestamp"])
        views = item["views"]

        entry = {
            key: views
        }

        if date in data:
            data[date].update(entry)
        else:
            data[date] = entry
    
    return data


# -----------------------------------------------------------------------------------------------------------------------
#                                                Data processing
# -----------------------------------------------------------------------------------------------------------------------

# Cleaned up data
data = {}

# Add all Undertale views
data = add_values(data, "undertale", undertale_dict)

# Add all Deltarune views
data = add_values(data, "deltarune", deltarune_dict)

# Add Deltarune to years prior to its existence
for entry in data:
    if "deltarune" not in data[entry]:
        data[entry].update({"deltarune": 0})
        
# Save new data in a file
with open('data/data.json', 'w') as file:
    json.dump(data, file)


# -----------------------------------------------------------------------------------------------------------------------
#                                                   Plotting
# -----------------------------------------------------------------------------------------------------------------------
# fig, ax = plt.subplots()
# ax.plot()