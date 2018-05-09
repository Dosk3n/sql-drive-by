# Sql-drive-by v1.1.1

## Disclaimer

This program was created for teaching purposes only! By using this program, you accept that I am not responsible for any actions that you take as a result of using this program.

## Description

Sql-drive-by is a program designed to find multiple websites that are vulnerable to sql injection by running a term through a search engine, testing its results and returning the vulnerable sites as a list. Additional features allow the user to search a website for potential admin pages.

## Videos

Finding sites: https://youtu.be/lQF2GZ98lw4

## Motivation

This program was created when I was teaching a friend (Shout out to Jay =P) about website vulnerabilities and was finding it difficult to find an sql injection vulnerable website to show how to test for the vulnerability. I wanted a program that not only made it easier to find these sites but also emphasizes how many sites out these are still vulnerable to SQLi and why people should be paying more attention to fixing these issues.

## Requirements

Python 3, Requests and BeautifulSoup4.

## Installation

###Installation in Kali Linux:
Note: Kali already has python3 installed so only needs Beautifulsoup4 and requests installed and just needs ran using python3 rather than python on the command line. See Usage for examples.
#### Install the required packages:
$ sudo apt-get update
<br />$ sudo apt-get install python3-bs4
<br />$ sudo apt-get install python3-requests
<br /><br />
Clone or download this git to a location of your choice.
<br /><br />
Done.

## Usage

$ python3 sqldriveby.py --term=page.php?id= --engine=y --depth=3
<br /><br />
$ python3 sqldriveby.py --find-admin="http://www.yourpage.com"
<br /><br />
$ python3 sqldriveby.py --help

Required Arguments:
	
	--term=     The parameter to search for. Example: --term=index.php?id=
	
Optional Arguments:
	
	--engine=   The search engine to use (y=Yahoo / b=Bing) (Default: Yahoo)
	
	--depth=    The number of pages of results to search through
	
Additional Features:

	--find-admin=    Try to find the admin page via a dictionary list
			 Example --find-admin="http://www.yourpage.com"
	

## Help

This program requires python 3 so if your system has both python 2 and python 3 you must run the program using python3 from command line. If your system only has python3 installed, you can run the program using python from command line.
