#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 18:07:09 2017

@author: Tim
"""

import requests, os


#base_url = 'https://pdbj.org/eF-site/servlet/Summary?entry_id='
download_url = 'https://pdbj.org/eF-site/servlet/Download?type=efvet&entry_id='

query_list = ['1nsf-A', '1dmk-A', '1yst-H']

storage = 'ef-site_downloads'


def get_url(ID):
    return download_url + ID

def request_url(URL):
    res = requests.get(URL)
    res.raise_for_status()
    return res

def get_files(query_list):
    for ID in query_list:
        url = get_url(ID)
        print(url)
        r = request_url(url)
        destination = os.path.join(storage, f'{ID}.xml.gz')
        with open(destination, 'wb') as f:
            f.write(r.content)
    print('Done')

get_files(query_list)

#Next Steps:
        #1 Unpack .gz
        #2 Parse XML and extract 
        
