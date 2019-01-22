#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 18:07:09 2017

@author: Tim
"""

import requests, os
import gzip
import shutil
from bs4 import BeautifulSoup

""" Example parameters:
ef_url = 'https://pdbj.org/eF-site/servlet/Download?type=efvet&entry_id={}'
#rcsb_url = 'https://files.rcsb.org/download/{}.pdb'

query_list = ['wahtever', '1nsf-A', '1dmk-A', '1yst-H']
#query_list2 = [x[:-2].upper() for x in query_list]

surfaces_path = 'ef-site_downloads'
#storage_rcsb = 'rcsb_downloads'
"""
def get_url(base, ID):
    return base.format(ID)

def request_url(URL):
    res = requests.get(URL)
    res.raise_for_status()
    return res

def is_available(request):
    soup = BeautifulSoup(request.content)
    title = soup.find('title')
    if title.contents[0].strip() == 'DB Error':
        return False
    else:
        return True

def get_files(query_list, base, path, ending):
    missing_entries = []
    for ID in query_list:
        if not ID + ending in os.listdir(path):
            url = get_url(base, ID)
            r = request_url(url)
            if is_available(r):
                print('Downloading from ', url)
                destination = os.path.join(path, f'{ID}' + ending)
                with open(destination, 'wb') as f:
                    f.write(r.content)
            else:
                print(f'{ID} is not available at ef-site')
                missing_entries.append(ID)
        else:
            print('Already downloaded ', ID)
    print('Done downloading')
    if len(missing_entries) > 0:
        return missing_entries
    else:
        return None

def unzip(path):
    for filename in os.listdir(path):
        if filename.endswith('.gz'):
            if not filename[:-3] in os.listdir(path):
                print('Unzipping ', filename)
                with gzip.open(os.path.join(path, filename), 'rb') as f_in:
                    with open(os.path.join(path, f'{filename[:-3]}'), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                print(f'Already unzipped {filename}')
    print('Done unzipping')
    return

def download_and_unzip_surfaces(query_list, url, path):
    missing_entries = get_files(query_list, url, path, '.xml.gz')
    unzip(path)
    if missing_entries is not None:
        return missing_entries
    else:
        return None
