# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class WorkshopPipeline:
    def process_item(self, item, spider):
        item['PLAYER'] = self.process_player(item['PLAYER'])
        return item
    
    def process_player(self, raw_name):
        raw_name = re.sub(r'\u200c+', '', raw_name) #remove \u200c
        raw_name = re.sub(r'[0-9]', '', raw_name)  #remove number
        
        # KyleK TuckerTuckerRF, group according to the capital letters and 
        #(Kyle)K (Tucker)TuckerRF => only two groups = match and the concate the string
        pattern = r'(\b[A-Z][a-z]+)[A-Z]?\s([A-Z][a-z]+)' 
        
        clean_name = ''
        
        matches = re.findall(pattern, raw_name)
        if matches:
            for match in matches:
                first_name, last_name = match
                clean_name = str(first_name) + ' ' + str(last_name)

        return clean_name.strip() if clean_name else raw_name
