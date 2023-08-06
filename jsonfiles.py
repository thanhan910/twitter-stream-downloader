import json
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# DEFINE THE FOLLOWING VARIABLES BEFORE RUNNING THIS SCRIPT
# Remember to skip the years and months that we already have
start_year = 2012
start_month = 3


def get_files_from_tar_file(url):
    # Given an url of the tar file on the Internet Archive, return a list of URLs of the files inside the tar file.

    print(url)

    response = requests.get(url)

    print(response.status_code)

    while response.status_code != 200:

        print(f"Failed to fetch URL: {url}")

        status_code = response.status_code

        if str(status_code).startswith("5"):
            print("Server error. Retrying...")
            response = requests.get(url)
            print(response.status_code)
            continue

        elif str(status_code).startswith("4"):
            print("Client error. Aborting...")
            return []

        else:
            print("Unknown error. Aborting...")
            return []

    soup = BeautifulSoup(response.content, "html.parser")

    print("Finish parsing HTML as soup")

    files = []

    for link in soup.find_all("a", href=True):
        # if link['href'].endswith('.gz'):
        absolute_url = urljoin(url, link["href"])
        files.append(absolute_url)

    print("Finish getting href list")

    return files

# Load the filenames from the json file
tweetfiles = json.loads(open("tweetfiles.json", "r").read())


# for each tar/zip file, get the list of files inside it

for year in tweetfiles.keys():
    
    # If we already have enough data for those years, skip them
    if(int(year) <= start_year - 1):
        continue

    for month in tweetfiles[year].keys():
        # If we already have enough data for those months in that year, skip them
        if(int(year) == start_year and int(month) <= start_month - 1):
            continue

        # if directory not created, create it
        if not os.path.exists(f"data/{year}/{month}"):
            os.makedirs(f"data/{year}/{month}")

        for folder_url in tweetfiles[year][month].keys():

            files = get_files_from_tar_file(folder_url)

            folder_name = folder_url.split("/")[-2]

            open(f"{year}/{month}/{folder_name}.json", "w").write(json.dumps(files))