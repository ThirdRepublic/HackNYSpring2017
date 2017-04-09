# YahooWeather JSON Processing
# April 8, 2017

from urllib2 import *

def first_in_double_quotes(s):

    """Returns text in between first set of double quotes.
    Example: ' B "A A A" C ' returns 'A A A'.

    Precondition: s contains two double quotes"""

    first_dq = s.index('"')
    post_fdq = s[first_dq+1:]
    second_dq = post_fdq.index('"')
    str_dq = post_fdq[:second_dq]
    return str_dq

def first_in_curly_braces(s):

    """Returns text in between first set of curly braces.
    Example: ' B {A A A} C ' returns 'A A A'.

    Precondition: s contains two curly braces, one opening and one closing"""

    first_dq = s.index('{')
    post_fdq = s[first_dq+1:]
    second_dq = post_fdq.index('}')
    str_dq = post_fdq[:second_dq]
    return str_dq

def forecast(zipcode):

    """Returns forecast in this format:
        location: Ithaca, NY;
        date: Sat, 08 Apr 2017;
        high: 47;
        low: 28;
        condition: Sunny"
        Precondition: zipcode is a 5-digit number
    """

    ###################
    ####ZIPCODE TO CITY
    ###################


    left = "http://maps.googleapis.com/maps/api/geocode/json?address="
    right = "&sensor=true"

    baseurl = left + str(zipcode) + right

    page_content = urlopen(baseurl).read()

    # 21 is length of "formatted_address" and a few spaces
    address_ind = page_content.find("formatted_address") + 21

    pc_trim = page_content[address_ind:]
    address = first_in_double_quotes(pc_trim)
    address_trim = ''

    #stop before zipcode
    for char in address:
        if type(char) != int:
            if address_trim.count(' ') != 2:
                address_trim += char
        else:
            break
    address_trim = address_trim[:-1]

    ####################
    ####CITY TO FORECAST
    ####################

    #components of the string

    left = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22"
    middle = '%2C%20'
    right = '%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    comma_ind = address_trim.find(',')
    a_city = address_trim[:comma_ind]
    a_state = address_trim[comma_ind+2:comma_ind+4]

    # get page contents

    baseurl2 = left + a_city + middle + a_state + right
    page_content2 = urlopen(baseurl2).read()

    # get the forecast
    fc_ind = page_content2.find('forecast')
    pc2_trim = first_in_curly_braces(page_content2[fc_ind:])

    # date
    pc2_postdate = pc2_trim[pc2_trim.find('date')+6:] # cuts everything before date
    date = first_in_double_quotes(pc2_postdate)

    # day
    pc2_postday = pc2_trim[pc2_trim.find('day')+5:]
    day = first_in_double_quotes(pc2_postday)

    # high
    pc2_posthigh = pc2_trim[pc2_trim.find('high')+6:]
    high = first_in_double_quotes(pc2_posthigh)

    # low
    pc2_postlow = pc2_trim[pc2_trim.find('low')+5:]
    low = first_in_double_quotes(pc2_postlow)

    # condition
    pc2_postcond = pc2_trim[pc2_trim.find('text')+6:]
    cond = first_in_double_quotes(pc2_postcond)

    ###########
    ###FORECAST
    ###########

    fc_loc = "Location: " + address_trim
    fc_date = "Date: " + day + ", " + date
    fc_high = "High: " + high
    fc_low = "Low: " + low
    fc_cond = "Condition: " + cond

    forecast = (fc_loc + '; ' + fc_date + '; ' + fc_high + '; ' + fc_low + '; '
                + fc_cond)

    return (forecast)
