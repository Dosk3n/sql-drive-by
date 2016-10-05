# Sql-drive-by v1.0.0

## Disclaimer

This program was created for teaching purposes only! By using this program you accept that I am not responsible for any stupid decisions that you make!

## Description

Sql-drive-by is a program designed to find multiple websites that are vulnerable to sql injection by running a term through a serch engine and testing its results. Additional features allow the user to search a website for potential admin pages.

## Motivation

This program was created when I was teaching a friend (Shoutout to Jay =P) about website vulnrabilities and was finding it difficult to find an sql injection vulnrable website to show how to test for the vulnerability. I wanted a program that not only made it easier to find these sites but also emphasises how many sites out these are still vulnrable to SQLi and why people should be paying more attention to fixing these issues.

## Requirements

Python 3 and BeautifulSoup4.

## Installation

###Installation in Kali Linux:
Note: Kali already has python3 installed so only needs Beautifulsoup4 installed and just needs ran using python3 rather than python on the command line. See Usage for examples.
#### Install the required packages:
$ sudo apt-get update
<br />$ sudo apt-get install python3-bs4
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

## Help

This program requires python 3 so if your system has both python 2 and python 3 you must run the program using python3 from command line. If your system only has python3 installed you can run the program using python from command line.
