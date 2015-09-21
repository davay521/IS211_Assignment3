#David vayman
#IS211_Assignment3
"""Url: http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"""


#IMPORT MODULES
import csv
import urllib2
import argparse
import re
import operator
import datetime
import collections

def main():

    def downloadData(url):
        """ Opens csv file from the url"""
        response = urllib2.urlopen(url)
        return response

            

    def dataTable(data):
        """ takes the csv data and puts it into a dictionary"""

        fileInput = csv.reader(data)
        keys = 1
        dictionary = {}

        for row in fileInput:
            dictionary[keys] = row
            keys += 1

        return dictionary

    def processData(table):
        
        images = [] #initializes list images
        browsers = []#initializes list browsers
        browserCount = {'Chrome': 0, 'Firefox': 0, 'MSIE': 0, 'Safari': 0}
        hours = collections.defaultdict(int)
        dateFormat = "%Y-%m-%d %H:%M:%S"

        for key, row in table.iteritems():      
            imageSearch = (re.findall(r'.gif$|.png$|.jpg$|.jpeg$', row[0], re.I | re.M))
            browserSearch = (re.findall(r'Chrome/|Firefox/|MSIE|'
                                         r'Version/\d.\d.\d\sSafari|Version/\d.\d\s\b[a-z0-9]+/[a-z0-9]+\b\sSafari',
                                         row[2], re.I | re.M))

            newDate = datetime.datetime.strptime(row[1], dateFormat)
            hours[newDate.hour] += 1       # creates a key 

            if len(imageSearch) != 0:        # appends to a new list
                images.append(imageSearch[0])

            if len(browserSearch) != 0:    # appends to a new list
                browsers.append(browserSearch[0])

        for i in browsers:      # counts the number of hits per browser

            if i[:3] == 'Fir': #checks for Fir for the first 3 characters of firefox
                browserCount['Firefox'] += 1
            elif i[:3] == 'Chr':#Checks for chr for the first 3 characters of chrome
                browserCount['Chrome'] += 1
            elif i[:3] == 'MSI':#checks for MSI for the first 3 characters of MSIE
                browserCount['MSIE'] += 1
            else:#if no match adds 1 to safari
                browserCount['Safari'] += 1

        mostPopular = max(browserCount.iteritems(), key=operator.itemgetter(1))
        hitsHour = sorted(hours.iteritems(), key=operator.itemgetter(1))[::-1]  
        imagePercent = (float(len(images))/float(len(table))) * 100

        return imagePercent, mostPopular[0], hitsHour

    #command line script

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url of csv file")
    args = parser.parse_args()

    if args.url:
        try:
            serverData = downloadData(args.url)
            if not serverData:                     # returns false, fails to connect
                print "Unable to connect to server "

            else:
                table = data_table(serverData)
                results = process_data(table)

                print "Image requests account for {0}% of all requests".format(results[0])
                print "{0} is the most popular browser".format(results[1])

                for hour in results[2]:
                    print "Hour {0} has {1} hits".format(hour[0], hour[1])

        except ValueError:
            print 'Your URL is not vaild System Shutdown'

    else:
        print "Please enter a valid --url"

if __name__ == "__main__":

    main()
