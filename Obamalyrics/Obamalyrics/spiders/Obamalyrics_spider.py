from scarpy import Spider
from Obamalyrics.items import ObamalyricsItem
import csv
import pandas as pd
import re
import string
#import csv from a certain folder.

Obamacsv = pd.read_csv("~/Desktop/ObamaTrump/Obama.csv")
#list(set(Obamacsv['artist'].tolist())
artist = Obamacsv['artist'].tolist()
song = Obamacsv['song'].tolist()

# artist_ = [re.sub('[^A-Za-z0-9]+', '', art) for art in artist]
artist_ = [''.join(c for c in s if c not in string.punctuation) for s in artist]
artist_1 = [re.sub('[^a-zA-Z0-9 \n\.]', '', s) for s in artist_]
artist_2 = [x.replace(" ", "-") for x in artist_]

song_ = [''.join(c for c in s if c not in string.punctuation) for s in song]
song_1 = [re.sub('[^a-zA-Z0-9 \n\.]', '', s) for s in song_]
song_2 = [x.replace(" ", "-") for x in song_]

songlist=list(zip(artist_2,song_2))
resultlists = ["http://www.metrolyrics.com/"+x[1]+"-lyrics-"+x[0]+".html" for x in songlist]

class ObamalyricsSpider(Spider):
	name = 'Obamalyircs_spider'
	allowed_urls = ['https://http://www.metrolyrics.com']
	start_urls = ['http://www.metrolyrics.com/humble-lyrics-kendrick-lamar.html']

	#3. write down result-urls with the extracted names
	#4. get the results!

	#find a way to change blank space to 
	#replace
	def parse_1(self, response):
		for url in resultlists:
			yield Request(url=url,callback=self.parse)

	def parse(self, response):
		lyric = response.xpath('//div[@id="lyrics-body-text"]//p/text()').extract()
		ly=[x.strip() for x in lyric] 

		item = ObamalyricsItem()
		item['lyrics']= ly 

		yield item
		
		

