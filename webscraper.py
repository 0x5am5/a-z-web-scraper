from bs4 import BeautifulSoup
import requests
import csv
from googlesheets import GoogleSheets

# Replace with your own domain and path of the page you want to scrape
domain = 'https://...'
url = domain + '/'

# Making the request and getting the content
headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                          "KHTML, like Gecko) Version/4.0 Safari/534.30"}
response = requests.get(url, timeout=5, headers=headers)
content = BeautifulSoup(response.content, "html.parser")

# Get the element that contains all the terms
wrapping_el = content.find('div', attrs={'class': 'wrapping-el'})
# Get all the links to the terms
terms = wrapping_el.find_all('term')

print('Found ' + str(len(terms)) + ' terms')

# Staring scraped terms
scrapedWordArr = []

# consider doing in batches or testing on a small number first (`for term in terms[:3]:`)
for term in terms:
  print('Getting word: ' + term.find('h2', attrs={'class': 'term'}).text)

  # Get the term
  term = term.find('h2').text
  # Get the definition
  definition = term.find('p', attrs={'class': 'definition'}).text

  if definition and term:
    print('Found: ' + term + ' - ' + definition)

    wordObj = {
      "term": term,
      "definition": definition
    }

    # If found, push to array
    scrapedWordArr.append(wordObj)

# If we have a list of scraped words, compare to google sheets or write to file
if scrapedWordArr.count:
  print('Found ' + str(len(scrapedWordArr)) + ' words')

  # Writing to file
  with open("file.csv", "w", newline='') as file:
    dict_writer = csv.DictWriter(file, scrapedWordArr[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(scrapedWordArr)

  # Writing to google sheets
  print('Connecting to Google Sheets...')
  
  google_sheets = GoogleSheets()

  # Getting list of pre-scraped words
  spreadsheetWordList = google_sheets.get_words()

  # Create seperate lists to differentiate between updating and appending
  addList = []
  updateList = []
  
  # Loop through every scraped word
  for i in range(len(scrapedWordArr)):
    currentWord = scrapedWordArr[i]
    print('Checking ' + str(currentWord.get('term')))
    found = False

    # Loop through every word in spreadsheet and check against current word
    for j in range(len(spreadsheetWordList)):
      currentSpreadsheetWord = spreadsheetWordList[j]

      # if word exists, then we just want to update (optional)
      if currentSpreadsheetWord[0].lower() == currentWord.get('term').lower():
        found = True

        # update according to your spreadsheet. Uses the batchUpdate method (https://developers.google.com/sheets/api/guides/batchupdate)
        updateList.append({
          "range": 'D' + str(j + 2) + ':H',
          "majorDimension": "ROWS",
          "values": [[
            None, # Project manangemn
            None, # Dev
            True, # Agile
            None, # startup
            None, # design
          ]]
        })
        print(currentWord.get('term') +  ' already exists!')
        break

      # If it doesn't exist, then we want to add it
    if not found:
      print('Adding ' + currentWord.get('term'))

      # update according to your spreadsheet. Uses the batchUpdate append (https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append) - 
      addList.append([
        currentWord.get('term'), 
        currentWord.get('definition'), 
        'Added with scraper...', 
        False, # Project management
        False, # Development
        True, # Agile
        False, # Startup
        False, # Design
        url
      ])

  print('Writing to Google Sheets...')
  if addList:
    google_sheets.write_to_sheet(addList)
  
  if updateList:
    google_sheets.update_sheet(updateList)

    