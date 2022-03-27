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
maxID = 3 # 67000
dir = 'text/'
if not os.path.exists(dir):
    os.mkdir(dir)


#-------------------------------------------------------------------------------------------
# MAIN

print('---------------------------------------------------------------------------------\\')
print('Downloading Erowid experience reports')
story_list = []
for i in range(1, maxID):
    fn = dir + 'erowid_' + str(i) + '.txt'
    id = i#random.randint(1,maxID)
    url = baseurl % id

    if os.path.exists(fn):
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
    time.sleep(0.8)
    
    title = page.split('class="title">')[1].split('</div>')[0].replace('\n', '')
    substance = page.split('class="substance">')[1].split('</div>')[0].replace('\n', '')
    author = page.split('class="author">')[1].split('</a>')[0].split('>')[1].replace('\n', '')
    
    print('Title: %s'%title)
    print('Substance: %s'%substance)
    print('Author: %s'%author)

    # get main text and remove common unicode characters
    body = page.split('Start Body -->')[1].split('<!-- End Body')[0]
    body = body.replace('\r','')
    body = body.replace('\n','')
    body = body.replace('\x92',"'")
    body = body.replace('\x93','"')
    body = body.replace('\x94','"')
    body = body.replace('\x97',' -- ')
    body = removeHTML(body)
    body = body.strip()

    story_list.append({'title':title, 'author':author, 'story': body})

    # uncomment to save txt file.
    #writeFile(fn, title + '\n\n' + body + '\n')

# This converts and saves the data as csv
if True:
    with open(f'scraped_{len(story_list)}.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(list(story_list[0].keys()))
        for story_page in story_list:
            writer.writerow([story_page['title'], story_page['author'], story_page['story']])
    
