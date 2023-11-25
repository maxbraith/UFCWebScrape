import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy
import math
import csv
import unidecode
from unidecode import unidecode
from csv import writer
import itertools

def ufcStatsScrape():
    #parse site using alphabet
    all_fighter_links = []
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for i in range(len(alphabet)):
        url=f'http://ufcstats.com/statistics/fighters?char={alphabet[i]}&page=all'
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        
        #site request
        site = requests.get(url, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')

        #scrape fighters from each page
        fighterLinks = []
        fighter_links = soup.find_all('a', class_=re.compile("b-link b-link_style_black"))

        #find hrefs
        for link in fighter_links:
            href = link['href']
            if href:
                fighterLinks.append(href)

        #remove link dups
        fighterLinks = list(dict.fromkeys(fighterLinks))
        all_fighter_links.append(fighterLinks)

    all_fighter_links = list(itertools.chain.from_iterable(all_fighter_links))
    print(f'Fighters Found: {len(all_fighter_links)}')


        
    #scrape individual fighter stats
    fighters_statistics = []
    for i in all_fighter_links:
        try:
            site = requests.get(i, headers=headers)
            soup = BeautifulSoup(site.content, 'html.parser')

            #initialize stats
            name = None
            wins = None
            losses = None
            draws = None
            height = None
            weight = None
            reach = None
            stance = None
            dOB = None
            sig_strikes_landed_per_min = None
            sig_striking_accuracy = None
            sig_strike_absorbed_per_min = None
            sig_strike_defense = None
            takedown_average = None
            takedown_accuracy = None
            takedown_defense = None
            sub_average = None

            #scrape name
            tempName = soup.find_all('span', class_=re.compile("b-content__title-highlight"))
            #clean name
            name = tempName[0].text.strip()

            #scrape records
            tempRecord = soup.find_all('span', class_=re.compile('b-content__title-record'))
            #clean wins + losses + draws
            record = tempRecord[0].text.strip()
            listRecord = record.split('-')
            for idx, ele in enumerate(listRecord):
                listRecord[idx] = ele.replace('Record: ', '')
            wins = listRecord[0]
            losses = listRecord[1]
            draws = listRecord[2]
            
            #clean soup for rest of stats
            i_tags = soup.find_all('i')
            for itags in i_tags:
                itags.decompose()
            
            #clean stats
            tempRest = soup.find_all('li', class_=re.compile('b-list__box-list-item b-list__box-list-item_type_block'))
        
        
            height = tempRest[0].text.strip()
            weight = tempRest[1].text.strip()
            reach = tempRest[2].text.strip()
            stance = tempRest[3].text.strip()
            dOB = tempRest[4].text.strip()
            sig_strikes_landed_per_min = tempRest[5].text.strip()
            sig_striking_accuracy = tempRest[6].text.strip()
            sig_strike_absorbed_per_min = tempRest[7].text.strip()
            sig_strike_defense = tempRest[8].text.strip()
            takedown_average = tempRest[10].text.strip()
            takedown_accuracy = tempRest[11].text.strip()
            takedown_defense = tempRest[12].text.strip()
            sub_average = tempRest[13].text.strip()
            
            #notification of scrape
            print(f'Scraping {name}...')
            print(i)


            #adding stats to fighters_statistics to prepare for csv
            fighters_statistics.append([name, wins, losses, draws, height, weight, reach, stance, dOB, sig_strikes_landed_per_min, sig_striking_accuracy, sig_strike_absorbed_per_min, sig_strike_defense, takedown_average, takedown_accuracy, takedown_defense, sub_average])
        except:
            pass
        


        

        #create csv file
        head = ['name', 'wins', 'losses', 'draws', 'height', 'weight', 'reach', 'stance', 'dOB', 'sig_strikes_landed_per_min', 'sig_striking_accuracy_%', 'sig_strike_absorbed_per_min', 'sig_strike_defense(%_of_sig_strikes_not_landed_by_opponent)', 'takedown_average(average_takedown_landed_per_fifteen_min)', 'takedown_accuracy_%', 'takedown_defense(%_of_opponent_takedown_not_landed)', 'sub_average(average_subs_attempted_per_15_mins)']

        with open('ufc_fighters_statistics.csv', 'w', encoding='UTF8', newline='') as scrapedStats:
            writer = csv.writer(scrapedStats)
            writer.writerow(head)
            writer.writerows(fighters_statistics)



ufcStatsScrape()

    




    


    

    




    
            


        
        

        

        





        