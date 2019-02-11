from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import csv
import re

driver = webdriver.Chrome()
driver.maximize_window() #For maximizing window
driver.implicitly_wait(5) #gives an implicit wait for 20 seconds

#driver.get("https://genius.com/search?q=Obama")
driver.get("https://genius.com/search?q=Trump")

print(driver.window_handles)

lyrics_button = driver.find_elements_by_xpath('//div[@ng-repeat = "section in $ctrl.sections"]/search-result-section/div/a')[1]
lyrics_button.click()


# elem = driver.switch_to.active_element
# print(elem.text)
# try:
# 	driver.switchTo().frame("modal_window-content modal_window-content--narrow_width modal_window-content--white_background");
# except Exception as e:
# 	print(e)

# driver.switch_to.frame(driver.find_element_by_xpath('//div[@class = "modal_window-content modal_window-content--narrow_width modal_window-content--white_background"]'))
# driver.find_element_by_xpath('//div[@class = "modal_window-content modal_window-content--narrow_width modal_window-content--white_background"]').send_keys(Keys.NULL)
popup = driver.find_element_by_xpath('/html/body/div[4]')

# driver.switch_to_frame("fpapi_comm_iframe")
# try:
# 	driver.switch_to_alert()
# except Exception as e: 
# 	print(e)
# elem = driver.switch_to.active_element
# print(elem.text)
#@ng-if="$scrollable_data_ctrl.models.length
#1. infinite scroll -> list -> for loop
#2. open new tab, get lyrics, and close

SCROLL_PAUSE_TIME = 3

while True:

	# Get scroll height
	### This is the difference. Moving this *inside* the loop
	### means that it checks if scrollTo is still scrolling 

	last_height = driver.execute_script("return document.body.scrollHeight")
	lastpopupheight = 0
	popupheight = 1
	# Scroll down to bottom
	while popupheight != lastpopupheight:
		driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
		popuplist = driver.find_element_by_xpath('/html/body/div[4]/div[1]/ng-transclude/search-result-paginated-section/scrollable-data/div[1]')
		lastpopupheight = popupheight
		popupheight = popuplist.size['height']
		time.sleep(1)
	# Wait to load page
	time.sleep(SCROLL_PAUSE_TIME)

	# Calculate new scroll height and compare with last scroll height
	new_height = driver.execute_script("return document.body.scrollHeight")
	if new_height == last_height:

		# try again (can be removed)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")

		# check if the page height has remained the same
		if new_height == last_height:
		# if so, you are done
			break
		# if not, move on to the next loop
		else:
			last_height = new_height
			continue

get_lyrics_buttons = driver.find_elements_by_xpath('//scrollable-data[@src = "$ctrl.infinite_scroll_data"]/div/transclude-injecting-local-scope/search-result-item/div/mini-song-card/a')
lyricslist = list()

for lyrics_button in get_lyrics_buttons:
	lyricslist.append(lyrics_button.get_attribute('href'))
print(lyricslist)
# get_lyrics_buttons.click()

#3. get the infinite scroll going 
#4. get them all in one.
#5. get lyrics from somewhere else

print(str(get_lyrics_buttons))
csv_file = open("lyric.csv","w",encoding="utf-8")
writer = csv.writer(csv_file)

actions = ActionChains(driver)

for lyric in lyricslist:
	driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
	driver.get(lyric)

	# actions.key_down(Keys.COMMAND).click(lyrics_button).key_up(Keys.COMMAND).perform()
	# driver.switch_to.window(driver.window_handles[1])

# get_humble_button = driver.find_element_by_xpath('//scrollable-data[@src = "$ctrl.infinite_scroll_data"]/div/transclude-injecting-local-scope/search-result-item/div/mini-song-card/a')

# get_humble_button.click()
	# wait_lyrics = WebDriverWait(driver, 1)
	lyric_dict = {}
	
	songtitle = driver.find_element_by_xpath('.//h1[@class ="header_with_cover_art-primary_info-title"]').text
	artist = driver.find_element_by_xpath('.//a[@class ="header_with_cover_art-primary_info-primary_artist"]').text
	# lyrcs = driver.find_element_by_xpath('.//div[@class="lyrics"]/section/p').text

	print(songtitle)
	print(artist)
	# print(lyrics) gotta get lyrics from another website

	# selectLinkOpeninNewTab = Keys.send_keys(Keys.COMMAND+Keys.RETURN)
	# driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
	# link = driver.find_element_by_xpath('.//song-primary-album/div/span[2]/a').get_attribute('href')
	# driver.get(link)
	# Make the tests...
	try:
		actions1 = ActionChains(driver)
		about = driver.find_element_by_xpath((('.//a[@ng-bind="album.name"]')))
		actions1.key_down(Keys.COMMAND).click(about).key_up(Keys.COMMAND).perform()
		
		#song-primary-album/div/span[2]/a

		# driver.findElement(By.linkText(('.//song-primary-album/div/span[2]/a').get_attribute('href'))).sendKeys(selectLinkOpeninNewTab)
		# driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
		driver.switch_to.window(driver.window_handles[1])
		time.sleep(2)
		try:
			album = driver.find_element_by_xpath('.//h1[@class = "header_with_cover_art-primary_info-title header_with_cover_art-primary_info-title--white"]').text
		except Exception as e: 
			album = 'none'

		try:
			year = driver.find_element_by_xpath('.//div[@ng-if = "$ctrl.page_data.album.release_date_components"]').text 
			year = int(re.findall('\d{4}', year)[0]) #findall always return a list
		except:
			year = 'none'

		print(album)
		print(year)

		# driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
		driver.close()

		lyrics_dict ={"title": songtitle, "artist": artist, "album":album, "year":year}
		writer.writerow(lyrics_dict.values())
		print(lyrics_dict)
		# driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
		# driver.switch_to.window(driver.window_handles[1])
		# driver.close()
		driver.switch_to.window(driver.window_handles[0])
		time.sleep(3)

	except Exception as e:
		album = 'none'
		year = 'none'
		
		#next
			



