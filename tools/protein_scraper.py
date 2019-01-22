#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 18:07:09 2017

@author: Tim
"""

import requests, os
import gzip
import shutil

""" Example parameters:
ef_url = 'https://pdbj.org/eF-site/servlet/Download?type=efvet&entry_id={}'
#rcsb_url = 'https://files.rcsb.org/download/{}.pdb'

query_list = ['1nsf-A', '1dmk-A', '1yst-H']
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

def get_files(query_list, base, path, ending):
    for ID in query_list:
        if not ID + ending in os.listdir(path):
            url = get_url(base, ID)
            print('Downloading from ', url)
            r = request_url(url)
            destination = os.path.join(path, f'{ID}' + ending)
            with open(destination, 'wb') as f:
                f.write(r.content)
        else:
            print('Already downloaded ', ID)
    print('Done downloading')
    return

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
    get_files(query_list, url, path, '.xml.gz')
    unzip(path)
    return
