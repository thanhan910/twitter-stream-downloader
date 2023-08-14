import json

def bz2_pattern_decrypt(pattern_code, year, month, day, hour, minute):
    regex_bz2_patterns_decrypt_meaning = {
        1: r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2",
        2: r"(\d{4})/(\d{2})-b/(\d{2})/(\d{2})/(\d{2}).json.bz2",
        3: r"(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2",
        4: r"(\d{2})/(\d{2})/(\d{2}).json.bz2",
        5: r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.gz",
        6: r"(\d{4})(\d{2})(\d{2})/(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})00.json.gz",
    }

    if pattern_code == 1:
        return f"{year}/{month}/{day}/{hour}/{minute}.json.bz2"
    elif pattern_code == 2:
        return f"{year}/{month}-b/{day}/{hour}/{minute}.json.bz2"
    elif pattern_code == 3:
        return f"{month}/{day}/{hour}/{minute}.json.bz2"
    elif pattern_code == 4:
        return f"{day}/{hour}/{minute}.json.bz2"
    elif pattern_code == 5:
        return f"{year}/{month}/{day}/{hour}/{minute}.json.gz"
    elif pattern_code == 6:
        return f"{year}{month}{day}/{year}{month}{day}{hour}{minute}00.json.gz"
    else:
        return None
    
def format_to_string(year, month, day, hour, minute):
    year = str(year)
    month = f'{month:02d}'
    day = f'{day:02d}'
    hour = f'{hour:02d}'
    minute = f'{minute:02d}'
    return year, month, day, hour, minute

def get_download_urls(year, month, day, hour, minute):

    year, month, day, hour, minute = format_to_string(year, month, day, hour, minute)

    potential_urls = []

    year_month_encrypt = json.load(open("year_month_encrypt.json", "r"))

    regex_tar_patterns_decrypt_str = {
        1: r"twitter-json-scrape-{}-{}.zip",
        2: r"archiveteam-twitter-{}-{}.tar",
        3: r"archiveteam-twitter-stream-{}-{}.tar",
        4: r"archiveteam-twitter-stream-{}-{}-b.tar",
        5: r"twitter-stream-{}-{}-{}.tar",
        6: r"twitter-{}-{}-{}.tar",
        7: r"twitter_stream_{}_{}_{}.tar",
        8: r"twitter-stream-{}-{}-{}.zip",
        9: r"twitter-stream-{}{}{}.tar",
    }

    pattern_code_list = year_month_encrypt[year][month][day]

    for pattern_code in pattern_code_list:
        tar_file = regex_tar_patterns_decrypt_str[pattern_code[0][0]].format(year, month, day)
        bz2_file = bz2_pattern_decrypt(pattern_code[1][0], year, month, day, hour, minute)

        if(len(pattern_code[0]) == 3):
            year_folder = pattern_code[0][1]
            month_folder = pattern_code[0][2]
        else:
            year_folder = year
            month_folder = month


        base_url = f"https://archive.org/download/archiveteam-twitter-stream-{year_folder}-{month_folder}"
        if(year_folder == '2011'):
            base_url = f"https://archive.org/download/archiveteam-twitter-json-2011"
    
        potential_urls.append(f"{base_url}/{tar_file}/{bz2_file}")

    return potential_urls

print(get_download_urls(2022, 1, day = 1, hour = 2, minute = 3))