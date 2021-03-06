from scrapy import Spider, Request
from Obamalyrics.items import ObamalyricsItem
import csv
import pandas as pd
import re
import string
#import csv from a certain folder.

Trumpcsv = pd.read_csv("~/Desktop/ObamaTrump/Trump.csv")
#list(set(Obamacsv['artist'].tolist())
artist = Trumpcsv['artist'].tolist()
song = Trumpcsv['song'].tolist()

# artist_ = [re.sub('[^A-Za-z0-9]+', '', art) for art in artist]
artist_ = [''.join(c for c in s if c not in string.punctuation) for s in artist]
artist_1 = [re.sub('[^a-zA-Z0-9 \n\.]', '', s) for s in artist_]
artist_2 = [x.replace(" ", "-") for x in artist_]

song_ = [''.join(c for c in s if c not in string.punctuation) for s in song]
song_1 = [re.sub('[^a-zA-Z0-9 \n\.]', '', s) for s in song_]
song_2 = [x.replace(" ", "-") for x in song_]

songlist=list(zip(artist_2,song_2))
resultlists = ["http://www.metrolyrics.com/"+x[1]+"-lyrics-"+x[0]+".html" for x in songlist]
reslistwithname = list(zip(artist, resultlists, song))


class ObamalyricsSpider(Spider):
	name = 'Obamalyircs_spider'
	allowed_urls = ['https://http://www.metrolyrics.com']
	start_urls = ['http://www.metrolyrics.com/its-everyday-bro-lyrics-jake-paul.html']

	#3. write down result-urls with the extracted names
	#4. get the results!

	#find a way to change blank space to 
	#replace
	def parse(self, response):
		# for url in resultlists:
		for i in range(len(resultlists)):
			# yield Request(url=url,callback=self.parse_lyrics)
			artist = reslistwithname[i][0]
			song = reslistwithname[i][2]
			try:
				yield Request(url=reslistwithname[i][1], meta={'artist': artist, 'song':song}, callback=self.parse_lyrics)
			except:
				next


	def parse_lyrics(self, response):
		try:
			artist = response.meta['artist']
			song = response.meta['song']
		except:
			artist = ""
			song = ""
		try:
			lyric = response.xpath('//div[@id="lyrics-body-text"]//p/text()').extract()
			ly=[x.strip() for x in lyric] 
		except:
			ly= ""

		item = ObamalyricsItem()
		item['artist'] = artist
		item['song'] = song
		item['lyrics']= ly 

		yield item
		
		

