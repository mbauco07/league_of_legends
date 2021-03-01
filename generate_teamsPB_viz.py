# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:29:57 2021

@author: Marco Bauco
@about: This file will take an already created pb json file for a league and then create visualisations for the entire league, meaning overall and team specific.
@input: the name of the json object file
"""

##############################################   GLOBALS/IMPORTS   ############################################## 
from lol_dto.classes import game
import requests
import sys
import pandas as pd
import numpy as np
import leaguepedia_parser as lp
import matplotlib as plt
import json
import os
from tqdm import tqdm 

FILE_PATH = 'pb_files/'

##############################################   GLOBALS/IMPORTS   ############################################## 

##############################################   FUNCTIONS  ############################################## 

def Create_Overall_Viz(data):
    print(data)

##############################################   FUNCTIONS  ############################################## 

##############################################   MAIN  ############################################## 
#read in file
with open(FILE_PATH+sys.argv[1].split(",")[0].strip(), "r") as f:
    pbJson = json.load(f)
#now split the JSON object into 2 versions the teams specific and overall objects
teamsJson = pbJson['teams']
overallJson = pbJson['overall']

#create the overall viz first
Create_Overall_Viz(overallJson)
##############################################   MAIN  ############################################## 
