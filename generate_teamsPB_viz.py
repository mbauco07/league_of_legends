# -*- coding: utf-8 -*-

#Created on Mon Mar  1 13:29:57 2021

#@author: Marco Bauco
#@about: This file will take an already created pb json file for a league and then create visualisations for the entire league, meaning overall and team specific.
#@input: the name of the json object file

##############################################   GLOBALS/IMPORTS   ############################################## 
from lol_dto.classes import game
import requests
import sys
import pandas as pd
import numpy as np
import leaguepedia_parser as lp
import matplotlib.pyplot as plt
import json
import os
from tqdm import tqdm 

FILE_PATH = 'pb_files/'

##############################################   GLOBALS/IMPORTS   ############################################## 

##############################################   FUNCTIONS  ############################################## 

def Create_Overall_Viz(data, league):
    champNames = []
    champLoses = []
    champWins = []
    width= 0.35
    for champ in data:
        print(champ + ": "+ str(data[champ]['Picks']) + " , " + str(data[champ]['Bans']) + ", " + str(data[champ]['Wins']))
        champNames.append(champ)
        champLoses.append(abs((data[champ]['Picks']+data[champ]['Bans']) - data[champ]['Wins']))
        champWins.append(data[champ]['Wins'])
    fig, ax = plt.subplots()
    ax.barh(champNames, champWins, width , label='Wins', color = 'green' )
    ax.barh(champNames, champLoses, width, label='Loses', color = 'black')

    ax.set_ylabel('Total Games played')
    ax.set_title('Wins and Loses Per Champ in: ' + league )
    ax.legend()

    plt.show()

def Create_Team_Viz(data, league):
    for team in data:
        print(team)
##############################################   FUNCTIONS  ############################################## 

##############################################   MAIN  ############################################## 
#read in file
with open(FILE_PATH+sys.argv[1].split(",")[0].strip(), "r") as f:
    pbJson = json.load(f)
#now split the JSON object into 2 versions the teams specific and overall objects
teamsJson = pbJson['teams']
overallJson = pbJson['overall']

#create the overall viz first
#Create_Overall_Viz(overallJson, sys.argv[1].split(",")[0].strip())
Create_Team_Viz(teamsJson, sys.argv[1].split(",")[0].strip())
##############################################   MAIN  ############################################## 
