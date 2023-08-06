import json
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Remember to skip the years and months that we already have data for
if os.path.exists("start.txt"):
    start_year = int(open("start.txt", "r").read().split("-")[0])
    start_month = int(open("start.txt", "r").read().split("-")[1])



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
# Usually takes 1-2 minutes to run per tar/zip file, if the status code is 200. 
# Sometimes the status code starts with 5 when the server is busy, and the script will retry until it gets a 200 status code. If you see a 5 status code, don't worry, it will retry automatically. But you can stop the script and redownload again later if you want.
for year in tweetfiles.keys():
    
    # If we already have enough data for those years, skip them
    if(int(year) <= start_year - 1):
        continue

    for month in tweetfiles[year].keys():
        # If we already have enough data for those months in that year, skip them
        if(int(year) == start_year and int(month) <= start_month - 1):
            continue

        save_to_folder = f"data/{year}/{int(month):02d}"

        # if directory not created, create it
        if not os.path.exists(save_to_folder):
            os.makedirs(save_to_folder)

        for tar_file_url in tweetfiles[year][month].keys():

            files = get_files_from_tar_file(tar_file_url)

            tar_file_name = tar_file_url.split("/")[-2]

            open(f"{save_to_folder}/{tar_file_name}.json", "w").write(json.dumps(files))

        next_month = int(month) + 1
        next_year = int(year)
        if next_month > 12:
            next_month = 1
            next_year += 1        
        open("start.txt", "w").write(f"{next_year}-{next_month}")
