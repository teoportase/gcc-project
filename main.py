# Is this the most efficient piece of code? No, not really, but I'm using this as a playground rather than thinking about efficiency for everything

# -----------------------------------------------------------------------------------------------------------------------
#                                                    Libraries
# -----------------------------------------------------------------------------------------------------------------------
import json
import requests
import matplotlib.pyplot as plt

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

        
# # Save new data in a file
# with open('data/data.json', 'w') as file:
#     json.dump(data, file)

# Make lists of the views for ease of access
undertale_values = []
deltarune_values = []

for entry in data:
    undertale_values.append(data[entry]["undertale"])
    deltarune_values.append(data[entry]["deltarune"])


# -----------------------------------------------------------------------------------------------------------------------
#                                              Plotting & other shenanigans
# -----------------------------------------------------------------------------------------------------------------------
# Get total number of views in total and per-article
undertale_views = 0
deltarune_views = 0

for entry in data:
    undertale_views += data[entry]["undertale"]
    deltarune_views += data[entry]["deltarune"]

print(f'Undertale total views: {undertale_views}\nDeltarune total views: {deltarune_views}\nTotal views: {undertale_views + deltarune_views}')


# Plots, plots, and more plots!
fig, axs = plt.subplots(2, 1, layout="constrained")

# Create a bar graph for Undertale
axs[0].bar(data.keys(), undertale_values)
# Create a bar graph for Deltarune
axs[1].bar(data.keys(), deltarune_values)

# Undertale plot settings
axs[0].set_title("Undertale views per month")
axs[0].set_xlabel("Month")
axs[0].set_ylabel("Views")
axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=90)
axs[0].tick_params(axis='x', which='major', labelsize=7)

# Deltarune plot settings
axs[1].set_title("Deltarune views per month")
axs[1].set_xlabel("Month")
axs[1].set_ylabel("Views")
axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=90)
axs[1].tick_params(axis='x', which='major', labelsize=7)



# Show the plot
plt.show()