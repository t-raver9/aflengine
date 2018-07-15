#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 18:43:10 2018

@author: chrisstrods
"""

from scraper import get_matches as get
from scraper import get_extra_data as get_extra
from scraper import scrape
from scraper import process




print("GETTING DATAFILES")
<<<<<<< HEAD
#get.main(2018,2018,9631,9648)
=======
get.main(2018,2018,9639,9639)
>>>>>>> 762e01abebcf012455e289ad1dc3a68ce9d7ff22
print("SUCCESSFULLY LOADED DATAFILES")
print("SCRAPING AFLTABLES DATA")
#scrape.main(2018,2018)
print("SUCCESSFULLY SCRAPED AFLTABLES DATA")
print("SCRAPING FOOTYWIRE DATA")
<<<<<<< HEAD
get_extra.main(9514,9648)
=======
get_extra.main(9639,9639)
>>>>>>> 762e01abebcf012455e289ad1dc3a68ce9d7ff22
print("SUCCESSFULLY SCRAPED FOOTYWIRE DATA")
print("POST-PROCESSING SCRAPED DATA")
process.main()
print("SUCCESSFULLY POST-PROCESSED SCRAPED DATA")

print("DATA IS NOW READY FOR ANALYSIS!")

