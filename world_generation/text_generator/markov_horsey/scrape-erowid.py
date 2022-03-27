#!/usr/bin/env python

# Fetch random Erowid experience reports and save them into the "text/" folder.
# Runs forever until you hit control-C to quit it

from __future__ import division

import os, sys, csv, time, urllib.request, random, re


#-------------------------------------------------------------------------------------------
# HELPERS AND SETUP

def writeFile(fn,data):
    f = open(fn,'w'); f.write(data); f.close()

def removeHTML(s):
    htmlRegexes = ['</?.{1,30}?>']
    for htmlRegex in htmlRegexes:
        s = re.sub(htmlRegex, '', s)
    return s

baseurl = 'http://www.erowid.org/experiences/exp.php?ID=%s'
maxID = 2 # 67000
dir = 'text/'
if not os.path.exists(dir):
    os.mkdir(dir)


#-------------------------------------------------------------------------------------------
# MAIN

print('---------------------------------------------------------------------------------\\')
print('Downloading Erowid experience reports')
print('Hit control-C to quit')
story_dict = []
for i in range(1, maxID):
    id = i#random.randint(1,maxID)
    url = baseurl % id

    if os.path.exists(dir + 'erowid_' + str(i) + '.txt'):
        print('We already downloaded that one.  Skipping #'+str(i))
        continue

    print('-----')
    print('Fetching url: %s'%url)
    with urllib.request.urlopen(url) as res:
        page = res.read().decode("ISO-8859-1")

    if 'Unable to view experience' in page:
        print('No report at that ID number.')
        continue

    # sleeping to not get ip banned for spam, after continue calls.
    time.sleep(1)
    
    # find the list of substances
    dosechart = page.split('DoseChart')[1]
    lines = dosechart.splitlines()
    substances = []
    for line in lines:
        if '<td><a ' in line:
            substance = line.split("'>")[1].split('<')[0]
            substanceUrl = line.split("href='")[1].split("'")[0]
            substanceUrl = substanceUrl.split('/')[-2]
            substances.append(substanceUrl)
    substances = sorted(list(set(substances)))
    fn = dir + 'erowid_' + str(i) + '.txt'
    title = page.split('class="title">')[1].split('</div>')[0]

    print('Substances: %s'%substances)
    print('Filename: %s'%fn)
    print('Title: %s'%title)

    # get main text and remove common unicode characters
    body = page.split('Start Body -->')[1].split('<!-- End Body')[0]
    body = body.replace('\r','')
    body = body.replace('\x92',"'")
    body = body.replace('\x93','"')
    body = body.replace('\x94','"')
    body = body.replace('\x97',' -- ')
    body = removeHTML(body)
    body = body.strip()

    story_dict.append({'title':title, 'story': body})

    # uncomment to save txt file.
    #writeFile(fn, title + '\n\n' + body + '\n')
if True:
    with open('dict.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in story_dict:
            print(key, value)
            writer.writerow([value[0], value[1]])
    
