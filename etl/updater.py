#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 18:43:10 2018

@author: chrisstrods
"""

from etl import download_matches as download
from etl import scrape_at as get_main
from etl import scrape_fw as get_extra
from etl import process


print("GETTING DATAFILES")
download.main(2018,2018,9694,9720)


print("SUCCESSFULLY LOADED DATAFILES")
print("SCRAPING AFLTABLES DATA")
get_main.main(2018,2018)
print("SUCCESSFULLY SCRAPED AFLTABLES DATA")
print("SCRAPING FOOTYWIRE DATA")
get_extra.main(9694,9720)


print("SUCCESSFULLY SCRAPED FOOTYWIRE DATA")
print("POST-PROCESSING SCRAPED DATA")
process.main()
print("SUCCESSFULLY POST-PROCESSED SCRAPED DATA")

print("DATA IS NOW READY FOR ANALYSIS!")

