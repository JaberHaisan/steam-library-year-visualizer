# steam_library_year_visualizer.py - Creates a bar chart of release year of games
# in library of given steam profile link.

import requests
import re
import threading
import collections
import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import bs4
import matplotlib.pyplot as plt

# Keep track of games for which no release date could be found.
no_date = []

class SteamGame():
	
	def __init__(self, game_link):
		"""Initializes SteamGame. 
		game_link is a link of a game in steam."""
		res = requests.get(game_link)
		self.soup = bs4.BeautifulSoup(res.text, "lxml")
		self.game_link = game_link
	
	def get_release_date(self):
		"""Returns the string of the release date of the steam game."""
		date_elem = self.soup.select_one("div[class=date]")
		
		# For the following cases scraping will fail according to tests:
		# 1) Games removed from the store can't be accessed. For e.g. https://store.steampowered.com/app/254040
		# 2) Some games do not have a release date in the steam store. For e.g. https://store.steampowered.com/app/8980/
		# Return None for them.
		if date_elem == None:
			no_date.append(self.game_link)
			return None
			
		return date_elem.getText()

def all_game_ids(steam_profile_link):
	"""Return all game ids in library of the given steam profile."""
	# Make sure link ends with a front slash as otherwise library_link will be invalid.
	if not steam_profile_link.endswith("/"):
		steam_profile_link += "/"
		
	# Get game ids.
	library_link = steam_profile_link + "games/?tab=all"
	driver = webdriver.Chrome()
	driver.get(library_link)
	# Need to login before required data can be acquired. Wait at most 60s and raise
	# TimeoutError if exceeded.
	try:
		element = WebDriverWait(driver, 60).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "template[data-profile-gameslist]"))
		)
	except:
		raise TimeoutError("Did not login before time out.")
	finally:
		library_attr = driver.find_element(By.CSS_SELECTOR, "template[data-profile-gameslist]").get_attribute("data-profile-gameslist")
		library_data = json.loads(library_attr)['rgGames']
		driver.quit()

	game_ids = [str(game["appid"]) for game in library_data]
	
	# Raise Error if there are no game ids.
	assert len(game_ids) > 0, "No games found in library."
	
	return game_ids

def get_release_years(game_ids, a_list, total_len):
	"""Adds list of release years for all games in game_ids to given list.
	game_ids is a list of steam game ids.
	a_list is a list.
	total_len is the total length of game ids list (Needed to show how far script has progressed)."""
	for game_id in game_ids:
		link = "https://store.steampowered.com/app/" + game_id
		game = SteamGame(link)
		release_date = game.get_release_date()
		if release_date != None:
			# Last 4 items of the string contain the year in release_date.
			a_list.append(release_date[-4:])
			
		# Show current progress.
		print(f"Currently at: {len(a_list)} / {total_len}", end="\r")

def get_profile_name(steam_profile_link):
	"""Returns profile name from given steam profile link."""
	res = requests.get(steam_profile_link)
	soup = bs4.BeautifulSoup(res.text, "lxml")
	elems = soup.select("span[class=actual_persona_name]")
	name = elems[0].getText()
	
	return name
	
def main():
	profile_link = input("Steam profile link: ")
	
	print("Getting game ids from profile...")
	game_ids = all_game_ids(profile_link)

	# Use multithreading to make getting release years faster.
	
	# If number of games is less than number of threads then games will be
	# incorrectly allocated to threads so determine number of threads according
	# to the number of games.
	total_games = len(game_ids)
	maximum_thread_no = 20
	if total_games < maximum_thread_no:
		threads_no = total_games
	else:
		threads_no = maximum_thread_no
	
	# Determine number of games per thread.
	segment_size = total_games // threads_no

	release_years = []
	threads = []

	n = 0
	for i in range(threads_no):
		segment = game_ids[n: n + segment_size]
		thread = threading.Thread(target=get_release_years, args=(segment, release_years, total_games))
		threads.append(thread)
		n += segment_size
	
	# If there are any remaining games that haven't been added to previous threads add them to
	# this thread.
	if total_games % segment_size != 0:
		segment = game_ids[n:]
		thread = threading.Thread(target=get_release_years, args=(segment, release_years, total_games))
		threads.append(thread)	

	print("Getting release years from games. Please wait...")
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	
	# Print out the links of any games that could not be included.
	if len(no_date) > 0:
		print(f"\n\nThe script was unable to find the release date of {len(no_date)} games.")
		print("This is either due to the game not having a store page or not having")
		print("a release date on the store page. Here are their links:\n")
		print(*no_date, sep="\n")
	
	# Use collections.Counter to get frequency of release year.
	counter = collections.Counter(release_years)
	
	# Sort counter according to release year.
	sorted_counter = dict(sorted(counter.items(), key = lambda n: n[0]))

	# Separate years and frequencies from counter.
	years = sorted_counter.keys()
	frequencies = sorted_counter.values()

	# Create a Bar chart from the data.
	fig = plt.figure(figsize=(10, 12))
	bars = plt.bar(years, frequencies, edgecolor="black", width=0.4)

	for bar in bars:
		yval = bar.get_height()
		plt.text(bar.get_x() - 0.025, yval + 0.5, yval)
		
	fig.autofmt_xdate()
	name = get_profile_name(profile_link)
	
	# Get current date as a formatted string.
	current_date = datetime.now().strftime("%d-%m-%y")
	
	plt.title(f"Number of games in {name}'s steam library by release year ({current_date})")
	
	# Label Axes.
	plt.ylabel("Frequency", fontsize=14)
	plt.xlabel("Release Year", fontsize=14)

	print("\nDrawing barchart...")
	plt.show()

if __name__ == "__main__":
	main()
