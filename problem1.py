import csv
import sys
import os
import math
import urlparse

# The idea is to automatically generate a number and perform some kind of operations on it 
# which shortens the url and store it somewhere(in a file or database, for this implementation
# I have used a text file). Every time a url is entered a new number is generted and I converted
# the number into "base 62" string [{0-9}, {a-z}, {A-Z}]. so even if same url is entered twice
# it will give different result every time. I then stored the number, the long url and shortened
# result into a text file (separated by ','). For geting the orignal url a reverse lookup can be
# performed (base62 to base 10 and then lookup into the text file or database)

class shortner(object):
    def __init__(self):
	self.fname = "urls.txt"
	self.content = []
        self.c_input = ''
        self.base_url = ''

    # Instead writing the result to a database I am wrting my result to a text file
    # The data variable is a combination of 3 parameters each separated by ','
    # param[1] -- the auto increment id
    # param[2] -- the long url
    # param[3] -- the corresponding shortened url
    def write_to_file(self,data):
        with open(self.fname, "a") as myfile:
            myfile.write(data + '\n')

    # Function to return the auto incremented id
    def get_next_id(self):
        content = open(self.fname).read().splitlines()
	if content == []:
	    return 1
	else:
            last = content[-1]
            _id = last.split(',')[0]
            return int(_id) + 1

    # Function to convert the remainder variable in while loop to its 
    # corrseponding "base 62" encoding 
    def int_to_char(self, num):
        # num is a digit ( between 0 and 9)
        if num < 10:
            return chr(num + 48) # ASCII char (0 + 48) corresponds to '0'
        elif 10 <= num <= 35:
            return chr(num + 55) # ASCII char (10 + 55) corresponds to 'A'
        elif 36 <= num < 62:
            return chr(num + 61) # ASCII char (36 + 61) corresponds to 'a'
    

    # Function to perform base 62 conversion on the auto incremented number
    def encode(self,number):
        string = ''
        while number > 0:
            remainder = number % 62
            string = self.int_to_char(remainder) + string
            number /= 62
        return string

    # Function to calculate the shortened url
    def short_url(self,longurl):
        self.c_input = longurl
	self.baseurl = self.c_input.split('?=')[0]
        new_id = self.get_next_id()
        s_url = self.encode(new_id)
        s_url = self.baseurl + '?=' + s_url
        data = str(new_id) + ',' + str(self.c_input) + ',' + str(s_url)
        self.write_to_file(data)
	return s_url
    
    # Wrapper function for the class which calls other methods to perform
    # url shortening operation
    def shorten(self,longurl):
        parts = urlparse.urlsplit(longurl)
	try:
            # check if the input given is a file or not. If its not a file
            # then simply call the "short_url" function else open the file,
            # get a list of all its content(urls) and call the "short_url" 
            # one by one
            if not os.path.isfile(longurl):
                return self.short_url(longurl) 
	    else:
	        urls = open(longurl).read().splitlines()
	        for items in urls:
		    self.short_url(items)
	except Exception:
		print "YOUR INPUT CANNOT BE PARSED"
		    
