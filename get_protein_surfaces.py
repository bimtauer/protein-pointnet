# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 00:18:55 2019

@author: bimta
"""
from tools.protein_scraper import download_and_unzip_surfaces
from tools.surface_extractor import get_surfaces

#To get surface xmls from ef-site
ef_url = 'https://pdbj.org/eF-site/servlet/Download?type=efvet&entry_id={}'
query_list = ['1nsf-A', '1dmk-A', '1yst-H', ']
surfaces_path = 'ef-site_downloads'

#Run download and unzip
download_and_unzip_surfaces(query_list, ef_url, surfaces_path)

surfaces = get_surfaces(surfaces_path)


#surfaces['1dmk-A']['edges']