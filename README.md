# JSON files urls of Twitter Stream collection
A collection of urls to the compressed JSON files tweets on the Twitter Stream Archive. https://archive.org/details/twitterstream

In this collection: https://archive.org/details/twitterstream, there are a number of .tar and .zip files that contains the JSON files of tweets. This repository contains a list of urls to these files, stored in `tweetfiles.json`. Those urls are collected using the  `tarfiles.py` script.

In each of those .tar and .zip files, there are a number of .json.bz2 or .json.gz files. The urls to those files are stored in the documents inside the `data` folder in this repository. Those urls are collected using the `jsonfiles.py` script.

**Note:** If the `data` folder is not complete, you can continue completing this dataset by just running the `jsonfiles.py` script.