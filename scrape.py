from bs4 import BeautifulSoup
import requests, openpyxl
import pandas as pd

class Scrape:
    def __init__(self):
        self.excel = openpyxl.Workbook()
        self.sheet = self.excel.active
        self.sheet.title = 'IMDB TOP RATED MOVIES'
        self.sheet.append(["Rank", "Name", "Release Year", "Rating"])

    def createData(self):
        try:
            #To delete rows so that data does not get appended again and again on button clicks
            while(self.sheet.max_row > 1):
                    self.sheet.delete_rows(2)

            src = requests.get("https://www.imdb.com/chart/top/")
            src.raise_for_status() #throws error if src url is invalid

            soup = BeautifulSoup(src.text, 'html.parser')
            
            movies = soup.find('tbody', class_="lister-list").find_all('tr')
            print(len(movies))

            for i in movies:
                rank = i.find('td', class_="titleColumn").get_text(strip=True).split('.')[0]
                name = i.find('td', class_="titleColumn").a.text
                year = i.find('td', class_="titleColumn").span.text.strip('()')
                ratings = i.find('td', class_="ratingColumn imdbRating").strong.text
                
                self.sheet.append([rank, name, year, ratings])
            self.excel.save('data/IMDB Top Rated Movies.xlsx')

        except Exception as e:
            return False, e

        return True, "File created Sucessfully!"