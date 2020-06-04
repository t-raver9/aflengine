#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 18:43:10 2018

@author: chrisstrods
"""

import download_matches as download
import scrape_at as get_main
import scrape_fw as get_extra
import process

SYEAR = 2020
EYEAR = 2020
SCODE = 9928
ECODE = 9936


if __name__ == "__main__":
    print("1.GETTING DATAFILES")
    #download.main(SYEAR, EYEAR, SCODE, ECODE)
    print("1.SUCCESSFULLY LOADED DATAFILES")
    print("2.SCRAPING AFLTABLES DATA")
    get_main.main(SYEAR, EYEAR)
    print("2.SUCCESSFULLY SCRAPED AFLTABLES DATA")
    print("3.SCRAPING FOOTYWIRE DATA")
    get_extra.main(SCODE, ECODE)
    print("3.SUCCESSFULLY SCRAPED FOOTYWIRE DATA")
    print("4.POST-PROCESSING SCRAPED DATA")
    process.main()
    print("4.SUCCESSFULLY POST-PROCESSED SCRAPED DATA")
    
    print("DATA IS NOW READY FOR ANALYSIS!")
