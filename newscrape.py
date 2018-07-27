# newscrape.py
'''
This is the main program file for the new scraping software I've written to do my paper
'''

from classes import Transaction, BuyerSeller, WhatAmI
from datetime import date, timedelta, datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


def calcnumpages(numrecs):
    numpages = numrecs // 20
    if numrecs % 20 == 0:
        numpages = numpages - 1
    return numpages + 1


def defineconstants():
    ''' This is a function that returns the constants that are used in the program.
     All constants are defined with variable names in ALLCAPS. '''

    # MONTHS is a dictionary of months for looking up months on the NOD websites
    MONTHS = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
              9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    # COUNTIES is a dictionary of the counties that we will actually perform a scrape for.
    # NOTE: There is a countydict in the classes.py file that lists all counties in Nebraska for future use.

    COUNTIES =   {
                    31: 'Burt',
                    #25: 'Butler',
                    #43: 'Colfax',
                    #24: 'Cuming',
                    #28: 'Hamilton',
                    #7:  'Madison',
                    #46: 'Merrick',
                    #10: 'Platte',
                    #22: 'Saline',
                    #6:  'Saunders',
                    #16: 'Seward',
                    #53: 'Stanton',
                    #29: 'Washington',
                    #27: 'Wayne'
                    }

    return MONTHS, COUNTIES



def printwelcomemsg():
    ''' This functino just prints a welcome message'''
    print('This program will get information from the Nebraska Deeds Online website in order to "scrape"')
    print('HTML data for importing into my spreadsheet.')
    print()


def getdates():
    ''' This function gets the dates that we are going to find '''
    begdate = input('Enter beginning date (mmddyyyy): ')
    enddate = input('Enter ending date    (mmddyyyy): ')
    if begdate != '':
        begdate = datetime.strptime(begdate, '%m%d%Y')
    if enddate != '':
        enddate = datetime.strptime(enddate, '%m%d%Y')  # this is the complete ending date for the period we are going to scrape
    else:
        enddate = datetime.today()
        if enddate.weekday() <= 3:
            days2add = 4 - enddate.weekday()
        else:
            days2add = 11 - enddate.weekday()
        enddate = enddate + timedelta(days=days2add)
        begdate = enddate + timedelta(days=-6)
    return begdate, enddate


def getnumpages(driver, county, lookup, bm, bd, by, em, ed, ey):
    driver.get(lookup)
    driver.find_element_by_link_text("Advanced Options").click()
    driver.find_element_by_id("cmbMonth1").click()
    Select(driver.find_element_by_id("cmbMonth1")).select_by_visible_text(bm)
    driver.find_element_by_id("cmbMonth1").click()
    driver.find_element_by_id("cmbDay1").click()
    Select(driver.find_element_by_id("cmbDay1")).select_by_visible_text(bd)
    driver.find_element_by_id("cmbDay1").click()
    driver.find_element_by_id("cmbYear1").click()
    Select(driver.find_element_by_id("cmbYear1")).select_by_visible_text(by)
    driver.find_element_by_id("cmbYear1").click()
    driver.find_element_by_id("cmbMonth2").click()
    Select(driver.find_element_by_id("cmbMonth2")).select_by_visible_text(em)
    driver.find_element_by_id("cmbMonth2").click()
    driver.find_element_by_id("cmbDay2").click()
    Select(driver.find_element_by_id("cmbDay2")).select_by_visible_text(ed)
    driver.find_element_by_id("cmbDay2").click()
    driver.find_element_by_id("cmbYear2").click()
    Select(driver.find_element_by_id("cmbYear2")).select_by_visible_text(ey)
    driver.find_element_by_id("cmbYear2").click()
    driver.find_element_by_id("btnSubmit3").click()
    numrecs = driver.find_element_by_class_name('text-heading')
    numrecs = int(numrecs.text.split()[0])
    numpages = calcnumpages(numrecs)
    return numpages


def getrangedata(driver, county, lookup, bm, bd, by, em, ed, ey):
    driver.get(lookup)
    driver.find_element_by_link_text("Advanced Options").click()
    driver.find_element_by_id("cmbMonth1").click()
    Select(driver.find_element_by_id("cmbMonth1")).select_by_visible_text(bm)
    driver.find_element_by_id("cmbMonth1").click()
    driver.find_element_by_id("cmbDay1").click()
    Select(driver.find_element_by_id("cmbDay1")).select_by_visible_text(bd)
    driver.find_element_by_id("cmbDay1").click()
    driver.find_element_by_id("cmbYear1").click()
    Select(driver.find_element_by_id("cmbYear1")).select_by_visible_text(by)
    driver.find_element_by_id("cmbYear1").click()
    driver.find_element_by_id("cmbMonth2").click()
    Select(driver.find_element_by_id("cmbMonth2")).select_by_visible_text(em)
    driver.find_element_by_id("cmbMonth2").click()
    driver.find_element_by_id("cmbDay2").click()
    Select(driver.find_element_by_id("cmbDay2")).select_by_visible_text(ed)
    driver.find_element_by_id("cmbDay2").click()
    driver.find_element_by_id("cmbYear2").click()
    Select(driver.find_element_by_id("cmbYear2")).select_by_visible_text(ey)
    driver.find_element_by_id("cmbYear2").click()
    driver.find_element_by_id("btnSubmit3").click()
    numrecs = driver.find_element_by_class_name('text-heading')
    numrecs = int(numrecs.text.split()[0])
    numpages = calcnumpages(numrecs)
    if numpages == 0:
        return
    for x in range(1, numpages + 1):
        if x == 1:
            pass
        elif x >= 2 and x <= 10:
            driver.find_element_by_link_text(str(x)).click()
        else:
            raise ReferenceError('Too many pages -- Not enough links')
        page = driver.page_source
    return page

def scrape(page, county):
    #r = requests.get(url)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.table  # find the table references
    reclist = []
    grantorlist = []
    granteelist = []
    mygrantorlist = []
    mygranteelist = []

    #with open(f, 'a', newline='') as outfile:
    if table is None:
        pass
    else:
        for br in table.find_all('br'):  # finds the <br> and replaces with newlines (for the names)
            br.replace_with('\n')

        table_rows = table.find_all('tr')  # returns a list of table rows
        for tr in table_rows:
            td = tr.find_all('td')  # finds the table data
            row = [i.text for i in td]  # returns a list of data in each row from NDO. row is type list.
            if len(row) == 5:
                row.append(county)
                if row[0][-9:].strip() == 'Replatted':
                    note = '(Replatted)'
                    row[0] = row[0][-20:-10].strip()
                else:
                    row[0] = row[0][-10:].strip()
                    note = ''
                row[1] = row[1].strip()
                row[2] = row[2].strip()
                row[3] = row[3].strip()
                # Transaction(instrument, xactdate, deedtype, county, notes=None)
                proprec = Transaction(None, row[0], row[4], row[5])
                legallist = row[1].split('\n')

                grantorlist = row[2].split('\n')
                granteelist = row[3].split('\n')

                if note != '':
                    proprec.addnotes(note)
                reclist.append(proprec)



def main():
    ''' This is the main program. '''
    printwelcomemsg()
    begdate, enddate = getdates()
    MONTHS, COUNTIES = defineconstants()
    driver = webdriver.Chrome()

    for county in COUNTIES.keys():
        # lookup is the home page of the county we are going to find data for
        lookup = 'http://www.nebraskadeedsonline.us/search.aspx?county=' + str(county)
        # do a quick check for the whole week to see how many pages we need to find
        pagecount = getnumpages(driver, county, lookup,
                       MONTHS[begdate.month], str(begdate.day), str(begdate.year),
                       MONTHS[enddate.month], str(enddate.day), str(enddate.year))

        if pagecount <= 10:
            page = getrangedata(driver, county, lookup,
                              MONTHS[begdate.month], str(begdate.day), str(begdate.year),
                              MONTHS[enddate.month], str(enddate.day), str(enddate.year))
            scrape(page, county)
        else:
            raise ValueError('Exceeded 200 objects in range')

    #endfor loop
    driver.close()

main()