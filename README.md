# JSON files urls of Twitter Stream collection
A collection of urls to the compressed JSON files tweets on the Twitter Stream Archive. https://archive.org/details/twitterstream

In this collection: https://archive.org/details/twitterstream, there are a number of .tar and .zip files that contains the JSON files of tweets. This repository contains a list of urls to these files, stored in `tweetfiles.json`. Those urls are collected using the  `tarfiles.py` script.

In each of those .tar and .zip files, there are a number of .json.bz2 or .json.gz files. The urls to those files are stored in the documents inside the `data` folder in this repository. Those urls are collected using the `jsonfiles.py` script.

**Note:** The `data` folder is not complete. You can continue completing this dataset by running the `jsonfiles.py` script. Remember to set the 2 variables to the starting year and month that hasn't completed yet and that you want to collect. (For example, if the folder for the month of February 2015 is not completed, set `start_year` to 2015 and `start_month` to 2 to begin downloading from that month onwards.)