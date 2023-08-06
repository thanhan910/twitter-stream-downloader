import os

def get_download_urls(year, month, day = None, hour = None, minute = None):

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

    print(potential_pattern)
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

    return potential_urls


year = 2021
month = 1
day = 1
hour = 1
minute = 30
print(get_download_urls(year, month, day, hour, minute))