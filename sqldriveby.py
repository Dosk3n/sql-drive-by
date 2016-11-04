# !python3
#
# SQLDriveBy v1.0.0a
# A program designed to find multiple websites that
# are vulnerable to sql injection.
# For learning and testing purposes only! I am not
# responsible for any spudid decisions you make!
# by Dosk3n

import bs4, requests, sys, os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def createQuery(engine, term):
	""" A function to create a url query from the search 
	engine selected(char) and the search term(string) """
	search_query = ""
	if(engine == 'y'):
		search_query = "https://uk.search.yahoo.com/search?p=" + term
	elif(engine == 'b'):
		search_query = "http://www.bing.com/search?q=" + term
	else:
		print("\nError[E3]: Not a valid search engine option.")
		print("use tag --help to show options.")
		sys.exit()
	
	return search_query
	
def getSoupPackets(engine, search_query, depth):
	""" Run the search query and return a list of beautifulsoup objects
	for each page based off the depth """
	soup_packets = []
	itteration = 0
	# Get the soup packets based off the search engine selected
	if(engine == 'y'):
	# Loop: Get all the HTML > Add to soup_packets > Follow 'Next' link and repeat
		while (itteration < depth):
			try:
				result = requests.get(search_query)
				try:
					result.raise_for_status()
				except Exception as exc:
					print('Error: %s' % (exc))
				
				soup = bs4.BeautifulSoup(result.text, 'html.parser')
				soup_packets.append(soup)
				
				find_next = soup.find_all('a', class_="next")
				
				search_query = str(find_next[0]['href'])
				
				itteration = itteration + 1
			except:
				# This loop will crash if the depth is greater that count of result
				# pages so we catch the exception and stop the loop
				itteration = depth
				continue
		
		return soup_packets
	elif(engine == 'b'):
		# Bing results for each page uses its query to show the result number to start on
		# for each page. Example page 2 is http://www.bing.com/search?q=index.php%3fid%3d&first=11&FORM=PORE
		# The number 11 means for this page show results starting from number 11. I can use this for
		# going through depth of pages.
		
		# Based on above note, set the first result number
		result_num = 1
		original_search_query = search_query
	
		# Loop: Get all the HTML > Add to soup_packets > Follow 'Next' link and repeat
		while (itteration < depth):
			try:
				result = requests.get(search_query)
				try:
					result.raise_for_status()
				except Exception as exc:
					print('Error: %s' % (exc))
				
				soup = bs4.BeautifulSoup(result.text, 'html.parser')
				soup_packets.append(soup)
				
				find_next = soup.find_all('a', class_="sb_pagN")
				
				result_num = result_num + 10
				search_query = original_search_query + "&first=" + str(result_num) + "&FORM=PORE"
				
				itteration = itteration + 1
			except:
				# This loop will crash if the depth is greater that count of result
				# pages so we catch the exception and stop the loop
				itteration = depth
				continue
				
		return soup_packets
	else:
		print("\nError[E1]: Not a valid search engine option.")
		sys.exit()
	
def getUrlList(engine, soup_packets):
	""" Search and return a list of urls formatted based on search engine """
	print(bcolors.OKBLUE + "INFO: Creating list of URLs" + bcolors.ENDC)
	url_list = []
	# For each soup(html page) loop through and get the URL data
	for soup in soup_packets:
		if(engine == 'y'):
			findsoup = soup.find_all('a', class_=" td-u")
			if(len(findsoup) > 0):
				for i in findsoup:
					# create a dictionary for that URL and add to list
					resultdict = {
						"title" : i.text,
						"url"	: i['href']
					}
					url_list.append(resultdict)
			else:
				print("\nNo results found.")
				sys.exit()
		elif(engine == 'b'):
			# The Bing results are a little harder so grab all urls from the page
			findsoup = soup.find_all('a')
			if(len(findsoup) > 0):
				for i in findsoup:
					try:
						# confirm its an external url by checking for http in the string and
						# removing microsoft terms
						if("http" in i['href'] and "bing" not in i['href'] and "microsoft" not in i['href']):
							# create a dictionary for that URL and add to list
							resultdict = {
								"title" : "n/a",
								"url"	: i['href']
							}
							url_list.append(resultdict)
					except:
						continue
			else:
				print("\nNo results found.")
				sys.exit()
			
			
		else:
			print("\nError[E2]: Not a valid search engine option.")
			print("use --help to show options.")
			sys.exit()
			
	return url_list
	
def getMatchedUrls(url_list, term):
	""" Filter out the results by checking they include our term """
	print(bcolors.OKBLUE + "INFO: Filtering out URLs that include our term and discarding others" + bcolors.ENDC)
	matched_list = []
	# Our url_list contents are formatted as 'title' and 'url'
	for url in url_list:
		if(term in url['url']):
			matched_list.append(url)
			
	return matched_list
	
def checkVulnList(url_list):
	""" Check if url is vulnerable to SQLi and add to new list """
	print(bcolors.OKBLUE + "INFO: Testing URLs for SQLi vulnerabilities using ' method" + bcolors.ENDC)
	vuln_list = []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	# Our url_list contents are formatted as 'title' and 'url'
	index_of_list = 0
	num_of_success = 0
	for url in url_list:
		index_of_list = index_of_list + 1
		try:
			os.system('clear')
			header()
			print(bcolors.OKBLUE + "INFO: Please be patient as we are checking", str(len(url_list)), "urls" + bcolors.ENDC)
			print(bcolors.OKBLUE + "INFO: You can press ctrl+c to skip to the next in list" + bcolors.ENDC)
			print("Testing " + str(index_of_list) + "/" + str(len(url_list)) + ": " + url['url'])
			print("Found:", num_of_success)
			result = requests.get(url['url'] + "'", headers=headers)
			
			if("SQL syntax" in result.text):
				vuln_list.append(url)
				num_of_success = num_of_success + 1
			elif("SQL command" in result.text):
				vuln_list.append(url)
				num_of_success = num_of_success + 1
			elif("syntax error" in result.text):
				vuln_list.append(url)
				num_of_success = num_of_success + 1
			elif("Microsoft SQL" in result.text):
				vuln_list.append(url)
				num_of_success = num_of_success + 1
			elif("Query failed" in result.text):
				vuln_list.append(url)
				num_of_success = num_of_success + 1
		except:
			continue
	
	return vuln_list
	
def header():
	""" Display the header at start of program """
	print("#######################################################")
	print(bcolors.FAIL + " (         (       (                                    " + bcolors.ENDC)
	print(bcolors.FAIL + " )\ )  (   )\ )    )\ )                        (        " + bcolors.ENDC)
	print(bcolors.FAIL + "(()/(( )\ (()/(   (()/(  (  (   )     (      ( )\ (     " + bcolors.ENDC)
	print(bcolors.FAIL + " /(_))((_) /(_))__ /(_)) )( )\ /((   ))\ ___ )((_))\ )  " + bcolors.ENDC)
	print(bcolors.WARNING + "(_))((_)_ (_))|___(_))_ (()((_|_))\ /((_)___((_)_(()/(  " + bcolors.ENDC)
	print(bcolors.BOLD + "/ __|/ _ \| |      |   \ " + bcolors.WARNING + "((_|_))((_|_))" + bcolors.ENDC + bcolors.BOLD + "      | _ ) " + bcolors.WARNING + ")(_)) " + bcolors.ENDC)
	print(bcolors.BOLD + "\__ \ (_) | |__    | |) | '_| \ V // -_)     | _ \ || | " + bcolors.ENDC)
	print(bcolors.BOLD + "|___/\__\_\____|   |___/|_| |_|\_/ \___|     |___/\_, | " + bcolors.ENDC)
	print(bcolors.BOLD + " By Dosk3n          v1.0.0                        |__/  " + bcolors.ENDC)
	print("#######################################################")
	print("#  Search Engine SQL Injection vulnerability Finder   #")
	print("#  Website: https://github.com/Dosk3n/sql-drive-by    #")
	print("#######################################################")
	print(bcolors.FAIL + "This program was created for teaching purposes only!" + bcolors.ENDC)
	print(bcolors.FAIL + "By using this program you accept that I am not" + bcolors.ENDC)
	print(bcolors.FAIL + "responsible for any stupid decisions that you make!" + bcolors.ENDC)
	print()
	
def loadingMsg():
	print(bcolors.OKBLUE + "LOADING: The program is drinking its coffee in preperation" + bcolors.ENDC)
	print()
	
def getArgs():
	""" Check the arguments and assign to option or exit with error """
	if(len(sys.argv) < 2):
		print("Invalid parameters. use --help to show options.\n")
		sys.exit()
	
	options = {
		"term"   		  : "index.php?id=",
		"engine" 		  : "y",
		"depth"  		  : "1",
		"find_admin_url"  : False,
		"need_help"		  : False
	}
	
	for arg in sys.argv:
		if("--term=" in arg):
			options['term'] = arg[7:]
		if("--engine=" in arg):
			options['engine'] = arg[9:10]
		if("--depth=" in arg):
			options['depth'] = arg[8:]
		if("--find-admin=" in arg):
			options['find_admin_url'] = arg[13:]
		if("--help" in arg):
			options['need_help'] = True
		
	return options
	
def displayResults(vuln_list):
	""" Display the results to the user """
	print()
	if(len(vuln_list) == 0):
		print(bcolors.WARNING + "No vulnerable websites returned" + bcolors.ENDC)
		sys.exit()
	else:
		print(bcolors.OKBLUE + "INFO: Removing duplicate results" + bcolors.ENDC)
		
		# Since Bing will start repeating the last page if number of pages of results
		# is less that the depth we need to remove any duplicate results
		unique_vuln_list = [] # An empty list to add the unique lines to
		for result in vuln_list:
			if(result not in unique_vuln_list):
				unique_vuln_list.append(result)
		
		print(bcolors.FAIL + str(len(unique_vuln_list)) + " possibly vulnerable website(s) returned" + bcolors.ENDC)
		for i in unique_vuln_list:
			print("Title:", i['title'], "\nURL:", i['url'], "\n")
	
def findAdmin(find_admin_url):
	""" Takes a url and checks against a list of possible locations for HTTP status 200 """
	# Remove the final / in URL if it is there
	if(find_admin_url[len(find_admin_url)-1] == '/'):
		find_admin_url = find_admin_url[:len(find_admin_url)-1]
		
	# Check for http/https at the start and error if missing
	# Since we dont know if the user wants http or https we cant
	# add it automatically as we cant just guess
	if(find_admin_url[:4] != "http"):
		print("Error: Make sure to include http:// or https:// in your URL\n")
		sys.exit()
	
	# Check file with list of admin locations exists and if it does
	# create a variable with all locations
	locations = []
	if(os.path.exists("admin_list")):
		admin_list_file = open("admin_list", "r")
		locations = admin_list_file.readlines()
		admin_list_file.close
	else:
		print("Error: Unable to locate file: admin_list\n")
		sys.exit()
	
	# admin_list file exists so lets start looking for admin pages
	found_pages = []
	index_of_list = 0
	num_of_success = 0
	for location in locations:
		index_of_list = index_of_list + 1
		try:
			url = find_admin_url + location
			# Since I am getting the locations from a text file they include \n at the
			# end of each line so I remove that from the url string here
			url = url[:url.index('\n')]
			result = requests.get(url)
			
			os.system('clear')
			header()
			print(bcolors.OKBLUE + "INFO: Please be patient as we are checking", str(len(locations)), "locations" + bcolors.ENDC)
			print(bcolors.OKBLUE + "INFO: You can press ctrl+c to skip to the next in list" + bcolors.ENDC)
			print(bcolors.OKBLUE + "INFO: This checks to see if the location exists or returns a 404 error" + bcolors.ENDC)
			print("Checking " + str(index_of_list) + "/" + str(len(locations)) + ": " + url)
			print("Found:", num_of_success)
			
			
			if(result.status_code == 200):
				found_pages.append(url)
				num_of_success = num_of_success + 1
		except:
			handle_ctrl_c()
			continue
		
	return found_pages
	
def displayAdminResults(found_pages):
	""" Display the results to the user """
	print()
	if(len(found_pages) == 0):
		print(bcolors.WARNING + "No admin locations found" + bcolors.ENDC)
		sys.exit()
	else:
		print(bcolors.FAIL + str(len(found_pages)) + " possible admin page(s) returned" + bcolors.ENDC)
		for i in found_pages:
			print("Location:", i, "\n")
		
def handle_ctrl_c():
	""" Provide options to a user who presses ctrl+c when in a try loop """
	answer = input("\nAn exception was encountered with the current url or the user pressed CTRL+C \nDo you want to quit(q) or skip to the next URL in list(s)? q/S: ")
	if(answer == "q"):
		sys.exit()
		
def helpMsg():
	""" Show options available to user """
	print("""
Example: python3 sqldriveby.py --term=page.php?id= --engine=y --depth=3
Example: python3 sqldriveby.py --find-admin="http://www.yourpage.com"
Required Arguments:
	
	--term=     The parameter to search for. Example: --term=index.php?id=
	
Optional Arguments:
	
	--engine=   The search engine to use (y=Yahoo / b=Bing)
	
	--depth=    The number of pages of results to search through
	
Additional Features:
	--find-admin=    Try to find the admin page via a dictionary list
			 Example --find-admin="http://www.yourpage.com"
	
	""")
	
	
	
def main():
	os.system('clear')
	header()
	
	options = getArgs()						# Get arguments from command line
	term   = options['term']				
	engine = options['engine']
	depth  = int(options['depth'])
	find_admin_url = options['find_admin_url']	# This is False by default unless user sets a url
	need_help = options['need_help']
	
	# Check if looking for admin page otherwise run default program
	if(need_help):
		helpMsg()
	elif(find_admin_url):
		loadingMsg()
		found_pages = findAdmin(find_admin_url)
		displayAdminResults(found_pages)
	else:
		loadingMsg()
		search_query = createQuery(engine, term)
		soup_packets = getSoupPackets(engine, search_query, depth)
		url_list = getUrlList(engine, soup_packets)
		matched_list = getMatchedUrls(url_list, term)
		vuln_list = checkVulnList(matched_list)
		displayResults(vuln_list)
	
	
main()