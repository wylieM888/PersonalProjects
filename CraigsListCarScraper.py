import requests
import csv
import time
from urllib import request, response, error, parse
from bs4 import BeautifulSoup


def getLinks(articleUrl):
    url = ("https://charlotte.craigslist.org" + articleUrl)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')    
    return soup

url = "https://charlotte.craigslist.org/search/cta?hasPic=1&min_price=500&max_price=100000&min_auto_miles=5&max_auto_miles=300000&condition=20&condition=30&condition=60&auto_cylinders=1&auto_cylinders=2&auto_cylinders=3&auto_cylinders=4&auto_cylinders=5&auto_cylinders=6&auto_cylinders=7&auto_fuel_type=1&auto_fuel_type=2&auto_fuel_type=3&auto_fuel_type=4&auto_paint=1&auto_paint=2&auto_paint=20&auto_paint=3&auto_paint=4&auto_paint=5&auto_paint=6&auto_paint=7&auto_paint=8&auto_paint=9&auto_paint=10&auto_paint=11&auto_size=1&auto_size=2&auto_size=3&auto_size=4&auto_title_status=1&auto_title_status=2&auto_title_status=3&auto_transmission=1&auto_transmission=2&auto_bodytype=3&auto_bodytype=4&auto_bodytype=5&auto_bodytype=7&auto_bodytype=8&auto_bodytype=9&auto_bodytype=10&auto_bodytype=12"

response = requests.get(url)
html = response.text
#print('Status code:', response.status_code)


#print("\nFirst part of HTML document fetched as string:\n")
#print(html[:700])

soup = BeautifulSoup(html, 'lxml')
#print(soup.html.title.text)


element = soup.find_all("a", {"class": "header-logo"})
#print(element[0])

table = soup.find('div', {"class": "content"})
newTable = soup.find('p', {"class", "result-info"})

price_search = soup.findAll('span', {"class": "result-price"})

file = open('CraigslistCarDataV2.csv', 'w')
writer = csv.writer(file)
writer.writerow(["Title", "Price", "Condition", "Cylinders", "Fuel Type", "Odometer", "Size", "Color", "Title Status", "Transmission", "Type", "URL"])

inc = 0
list = []

numOfVehicles = 0

for a in table.find_all('a', href = True):
    inc = inc + 1
    if((inc%2) == 0):
        x = a['href']
        if (x != "#"):
            newURL = x
            newResponse = requests.get(x)
            newHTML = newResponse.text
            pageSoup = BeautifulSoup(newHTML, 'lxml')
            #pageSoup = getLinks(newURL)

            #Get title and price
            postTitle = pageSoup.find('span', {"class", "postingtitletext"})
            try:
                #newTitle = postTitle.find(id = "titletextonly").get_text()
                checkThis = pageSoup.find('div', class_= "mapAndAttrs")
                newTitleTester = checkThis.find('b')
                newTitle = str(newTitleTester.get_text()) 
            except:
                print("No title detected")
                newTitle = "NEED TO MANUALLY INPUT"
            try:
                postPrice = postTitle.find(class_ = "price").get_text().replace('$','').strip()
            except:
                postPrice = "$0"

            #Get condition, cylinders, fuel type, odometer, color, title status, and type
            try:
                condition = pageSoup.find(string = "condition: ").findNext(text=True)
            except:
                condition = "NO CONDITION"
            try:
                cylinders = pageSoup.find(string = "cylinders: ").findNext(text=True)
            except:
                cylinders = "NO CYLINDERS"
            try:
                fuel = pageSoup.find(string = "fuel: ").findNext(text=True)
            except:
                fuel = "NO FUEL"
            try:
                odometer = int(pageSoup.find(string = "odometer: ").findNext(text=True))
            except:
                odometer = "NO ODOMETER"
            try:
                color = pageSoup.find(string = "paint color: ").findNext(text=True)
            except:
                color = "NO COLOR"
            try:
                size = pageSoup.find(string = "size: ").findNext(text=True)
            except:
                size = "NO SIZE"
            try:
                titleStatus = pageSoup.find(string = "title status: ").findNext(text=True)
            except:
                titleStatus = "NO TITLE STATUS"
            try:
                transmission = pageSoup.find(string = "transmission: ").findNext(text=True)
            except:
                transmission = "NO TRANSMISSION"
            try:
                carType = pageSoup.find(string = "type: ").findNext(text=True)
            except:
                carType = "NO CAR TYPE"
            print("Title: " + str(newTitle) + "\nPrice: " + str(postPrice) + "\nCondition: " + condition)
            #print("Cyclinders: " + cylinders + "\nFuel: " + fuel + "\nOdometer: " + str(odometer) + "\nColor: " + color)
            #print("Size: " + size + "\nTitle Status: " + titleStatus + "\nTransmission: " + transmission + "\nCar Type: " + carType)
            #print("URL: " + x + "\n")

            numOfVehicles = numOfVehicles + 1
            try:
                writer.writerow([newTitle, postPrice, condition, cylinders, fuel, odometer, color, size, titleStatus, transmission, carType, x])
                time.sleep(1.5)
            except(UnicodeEncodeError):
                newTitle = "NEED TO MANUALLY INPUT"
                writer.writerow([newTitle, postPrice, condition, cylinders, fuel, odometer, color, size, titleStatus, transmission, carType, x])
                time.sleep(1.5)
            print("Vehicle " + str(numOfVehicles) + " loaded.")

inc = 0

while(True):
    nextButton = soup.find(class_ = "button next", href=True)
    nextUrl = "https://charlotte.craigslist.org" + nextButton['href']
    nextResponse = requests.get(nextUrl)
    nextHtml = nextResponse.text
    nextSoup = BeautifulSoup(nextHtml, 'lxml')
    #nextSoup = getLinks(nextButton['href'])

    nextTable = nextSoup.find('div', {"class": "content"})
    print()
    print("\n******New Page*******")

    for a in nextTable.find_all('a', href = True):
        inc = inc + 1
        if((inc%2) == 0):
            x = a['href']
            if (x != "#"):
                newURL = x
                try:
                    newResponse = requests.get(newUrl)
                    newHTML = newResponse.text
                    pageSoup = BeautifulSoup(newHTML, 'lxml')
                except:
                    newResponse2 = requests.get(newURL)
                    newHTML2 = newResponse2.text
                    pageSoup = BeautifulSoup(newHTML2, 'lxml')

                #Get title and price
                postTitle = pageSoup.find('span', {"class", "postingtitletext"})
                try:
                    checkThis = pageSoup.find('div', class_= "mapAndAttrs")
                    newTitleTester = checkThis.find('b')
                    newTitle = str(newTitleTester.get_text())
                except:
                    newTitle = "NEED TO MANUALLY INPUT"
                try:
                    postPrice = postTitle.find(class_ = "price").get_text()
                except(AttributeError):
                    postPrice = "$0"

                #Get condition, cylinders, fuel type, odometer, color, title status, and type
                condition = pageSoup.find(string = "condition: ").findNext(text=True)
                cylinders = pageSoup.find(string = "cylinders: ").findNext(text=True)
                fuel = pageSoup.find(string = "fuel: ").findNext(text=True)
                odometer = int(pageSoup.find(string = "odometer: ").findNext(text=True))
                color = pageSoup.find(string = "paint color: ").findNext(text=True)
                size = pageSoup.find(string = "size: ").findNext(text=True)
                titleStatus = pageSoup.find(string = "title status: ").findNext(text=True)
                transmission = pageSoup.find(string = "transmission: ").findNext(text=True)
                carType = pageSoup.find(string = "type: ").findNext(text=True)
                #print("Title: " + newTitle + "\nPrice: " + postPrice + "\nCondition: " + condition)
                #print("Cyclinders: " + cylinders + "\nFuel: " + fuel + "\nOdometer: " + str(odometer) + "\nColor: " + color)
                #print("Size: " + size + "\nTitle Status: " + titleStatus + "\nTransmission: " + transmission + "\nCar Type: " + carType)
                #print("URL: " + x + "\n")

                numOfVehicles = numOfVehicles + 1
                try:
                    writer.writerow([newTitle, postPrice, condition, cylinders, fuel, odometer, color, size, titleStatus, transmission, carType, x])
                    time.sleep(1.5)
                except(UnicodeEncodeError):
                    newTitle = "NEED TO MANUALLY INPUT"
                    writer.writerow([newTitle, postPrice, condition, cylinders, fuel, odometer, color, size, titleStatus, transmission, carType, x])
                    time.sleep(1.5)
                print("Vehicle " + str(numOfVehicles)  + " loaded.")
    #try:
    #    soup = BeautifulSoup(nextHtml, 'lxml')
    #except:
    #    soup = nextSoup
    #print(soup.html.title.text)
    time.sleep(3)
    numOfVehicles = numOfVehicles + 1
    if (numOfVehicles > 500):
        print("*******COMPLETE***********")
        break
    

            
file.close()

