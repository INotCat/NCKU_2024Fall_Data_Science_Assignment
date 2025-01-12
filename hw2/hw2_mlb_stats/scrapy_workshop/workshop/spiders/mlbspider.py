import scrapy
from bs4 import BeautifulSoup
from workshop.items import WorkshopItem
import csv



class MlbspiderSpider(scrapy.Spider):
    name = "mlbspider"
    allowed_domains = ["mlb.com"]
    start_urls = ["https://mlb.com/stats/"]
    page_number = 0
    csv_file = "mlb_player_stats.csv"
    
    #player in th scope=col id=tb-0-header-col<0-17> 
    #value in td scope=row headers="tb-0-header-col<0-17>" data-row="number" thead tr 
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('tbody', class_="notranslate")
        rows = table.find_all('tr')
        
        for row in rows:
            item = WorkshopItem()
            item['PLAYER'] = row.find('th').text
            item['TEAM'] = row.find('td', attrs={'data-col': '1'}).text    
            item['G'] = row.find('td', attrs={'data-col': '2'}).text    
            item['AB'] = row.find('td', attrs={'data-col': '3'}).text    
            item['R'] = row.find('td', attrs={'data-col': '4'}).text    
            item['H'] = row.find('td', attrs={'data-col': '5'}).text    
            # item['B2'] = row.find('td', attrs={'data-col': '6'}).text    
            # item['B3'] = row.find('td', attrs={'data-col': '7'}).text    
            item['HR'] = row.find('td', attrs={'data-col': '8'}).text    
            item['RBI'] = row.find('td', attrs={'data-col': '9'}).text    
            item['BB'] = row.find('td', attrs={'data-col': '10'}).text    
            item['SO'] = row.find('td', attrs={'data-col': '11'}).text    
            item['SB'] = row.find('td', attrs={'data-col': '12'}).text    
            # item['CS'] = row.find('td', attrs={'data-col': '13'}).text    
            item['AVG'] = row.find('td', attrs={'data-col': '14'}).text    
            item['OBP'] = row.find('td', attrs={'data-col': '15'}).text    
            item['SLG'] = row.find('td', attrs={'data-col': '16'}).text    
            item['OPS'] = row.find('td', attrs={'data-col': '17'}).text  
            yield item
    
        self.page_number = self.page_number + 1 
        next_page = self.start_urls[0] + '?page=' + str(self.page_number)
        
        if self.is_valid_page(response):
            yield response.follow(next_page, callback=self.parse) 
            
    def is_valid_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('tbody', class_='notranslate')
        rows = table.find_all('tr') if table else []
        return len(rows) > 0