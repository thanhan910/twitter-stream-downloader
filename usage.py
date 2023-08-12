import json
import bz2
import gzip
from urllib.request import urlopen
import os

def get_potential_patterns(year, month, day = None, hour = None, minute = None):
    if(day == None):
        potential_pattern = [f"{month:02d}/", f"{year}{month:02d}"]

        if(year == 2013 and month == 12):
            potential_pattern.append(f"{year}/{month:02d}-b/")
    
    elif(hour == None):
        potential_pattern = [f"{month:02d}/{day:02d}/", f"{year}{month:02d}{day:02d}"]

        if(year == 2013 and month == 12):
            potential_pattern.append(f"{year}/{month:02d}-b/{day:02d}/")

    elif(minute == None):
        potential_pattern = [f"{month:02d}/{day:02d}/{hour:02d}/", f"{year}{month:02d}{day:02d}{hour:02d}"]

        if(year == 2013 and month == 12):
            potential_pattern.append(f"{year}/{month:02d}-b/{day:02d}/{hour:02d}/")

    else:
        potential_pattern = [f"{month:02d}/{day:02d}/{hour:02d}/{minute:02d}", f"{year}{month:02d}{day:02d}{hour:02d}{minute:02d}"]

        if(year == 2013 and month == 12):
            potential_pattern.append(f"{year}/{month:02d}-b/{day:02d}/{hour:02d}/{minute:02d}")

    return potential_pattern

def get_download_urls_using_local_data(year, month, day = None, hour = None, minute = None):

    if(day == None):
        potential_pattern = [f"{month:02d}/", f"{year}{month:02d}"]

        if(year == 2013 and month == 12):
            potential_pattern.append(f"{year}/{month:02d}-b/")
    
    elif(hour == None):
        potential_pattern = [f"{month:02d}/{day:02d}/", f"{year}{month:02d}{day:02d}"]

        if(year == 2013 and month == 12):
            potential_pattern.append(f"{year}/{month:02d}-b/{day:02d}/")

    elif(minute == None):
        potential_pattern = [f"{month:02d}/{day:02d}/{hour:02d}/", f"{year}{month:02d}{day:02d}{hour:02d}"]

        if(year == 2013 and month == 12):
            potential_pattern.append(f"{year}/{month:02d}-b/{day:02d}/{hour:02d}/")

    else:
        potential_pattern = [f"{month:02d}/{day:02d}/{hour:02d}/{minute:02d}", f"{year}{month:02d}{day:02d}{hour:02d}{minute:02d}"]

        if(year == 2013 and month == 12):
            potential_pattern.append(f"{year}/{month:02d}-b/{day:02d}/{hour:02d}/{minute:02d}")

    print("potential_pattern:", potential_pattern)
    # Get all potential urls
    potential_urls = []
    for dirpath, dirnames, filenames in os.walk(f"data/{year}/{month:02d}"):
        for filename in [f for f in filenames if f.endswith(".txt")]:
            data = open(os.path.join(dirpath, filename), "r").read().split("\n")
            base_url = f"https://archive.org/download/archiveteam-twitter-stream-{year}-{month:02d}/{filename.removesuffix('.txt')}"
            if(year == 2011):
                base_url = f"https://archive.org/download/archiveteam-twitter-json-2011/twitter-json-scrape-2011-{month:02d}.zip"
            for pattern in potential_pattern:
                potential_urls.extend([f"{base_url}/{line}" for line in data if(pattern in line)])
    print("potential_urls:", potential_urls)

    return potential_urls

def get_download_urls_using_stored_data_on_github(year, month, day = None, hour = None, minute = None):

    potential_pattern = get_potential_patterns(year, month, day, hour, minute)

    
    # Get all potential urls

    potential_urls = []

    filenames = json.loads(urlopen('https://raw.githubusercontent.com/thanhan910/twitter-stream-json-urls/main/data_folder_structure.json').read().decode())[str(year)][str(month).zfill(2)]

    print(filenames)


    for filename in [f for f in filenames if f.endswith(".txt")]:
        data = urlopen(f"https://raw.githubusercontent.com/thanhan910/twitter-stream-json-urls/main/data/{year}/{month:02d}/{filename}").read().decode().split("\n")
        base_url = f"https://archive.org/download/archiveteam-twitter-stream-{year}-{month:02d}/{filename.removesuffix('.txt')}"
        if(year == 2011):
            base_url = f"https://archive.org/download/archiveteam-twitter-json-2011/twitter-json-scrape-2011-{month:02d}.zip"
        for pattern in potential_pattern:
            potential_urls.extend([f"{base_url}/{line}" for line in data if(pattern in line)])
    print("potential_urls:", potential_urls)

    return potential_urls




def read_compressed_json(url):
    # try:
        with urlopen(url) as response:
            if url.endswith('.json.bz2'):
                with bz2.open(response, 'rt', encoding='utf-8') as file:
                    data = [json.loads(line) for line in file.readlines()]
            elif url.endswith('.json.gz'):
                with gzip.open(response, 'rt', encoding='utf-8') as file:
                    data = [json.loads(line) for line in file.readlines()]
            else:
                raise ValueError("Unsupported file format. Only .json.bz2 and .json.gz are supported.")

        return data

    # except Exception as e:
    #     print(f"Error: {e}")
    #     return None

# Example usage

urls = get_download_urls_using_stored_data_on_github(2020, 10, 2)
for url in urls:
    json_data = read_compressed_json(url)
    if json_data:
        print(json_data)
    break
