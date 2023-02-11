import requests
from bs4 import BeautifulSoup

def get_crop_season(crop_name):
    # Search the internet for the season that crop is sowed in
    url = f"https://www.google.com/search?q={crop_name}+sowing+season"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")
    if not search_results:
        return None

    # Extract the sowing season from the search results
    season = search_results[0].text
    print(f"{crop_name}: {season}")
    return season

# Load the dataset into a pandas DataFrame
import pandas as pd
df = pd.read_csv("Clean_dataset/3.csv")

# Add a new column to the DataFrame for the sowing season
df["Season"] = None

# Iterate through the crop names column
for i, crop_name in enumerate(df["crop"]):
    season = get_crop_season(crop_name)
    df.at[i, "Season"] = season

# Save the updated DataFrame to a new CSV file
df.to_csv("Clean_dataset/5.csv", index=False)
