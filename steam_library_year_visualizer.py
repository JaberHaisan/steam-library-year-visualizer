# steam_library_year_visualizer.py - Creates a bar chart of release year of games
# in library of given steam profile link.

import requests
import bs4
import re
import threading
import collections
import matplotlib.pyplot as plt

class SteamGame():
	
	def __init__(self, game_link):
		"""Initializes SteamGame. 
		game_link is a link of a game in steam."""
		res = requests.get(game_link)
		self.soup = bs4.BeautifulSoup(res.text, "lxml")
	
	def get_release_date(self):
		"""Returns the string of the release date of the steam game."""
		elems = self.soup.select("div[class=date]")
		
		# For the following cases scraping will fail according to tests:
		# 1) Games removed from the store can't be accessed. For e.g. https://store.steampowered.com/app/254040
		# 2) Some games do not have a release date in the steam store. For e.g. https://store.steampowered.com/app/8980/
		# Return None for them.
		if len(elems) == 0:
			return None
			
		return elems[0].getText()

def all_game_ids(steam_profile_link):
	"""Return all game ids in library of the given steam profile."""
	# Make sure link ends with a front slash as otherwise library_link
	# will be invalid.
	if not steam_profile_link.endswith("/"):
		steam_profile_link += "/"
	
	# Get game ids.
	library_link = steam_profile_link + "games/?tab=all"
	res = requests.get(library_link)
	game_ids = re.findall(r'"appid":(\d*),', res.text)
	
	# Raise Error if there are no game ids.
	assert len(game_ids) > 0, "No games found in library."
	
	return game_ids

def get_release_years(game_ids, a_list, total_len):
	"""Adds list of release years for all games in game_ids to given list.
	game_ids is a list of steam game ids.
	a_list is a list.
	total_len is the total length of game ids list (Needed to show how far script has progressed)."""
	release_years = []
	
	for game_id in game_ids:
		link = "https://store.steampowered.com/app/" + game_id
		game = SteamGame(link)
		release_date = game.get_release_date()
		if release_date != None:
			# Last 4 items of the string contain the year in release_date.
			release_years.append(release_date[-4:])
		
	a_list.extend(release_years)
	
	# Show current progress.
	print(f"Currently at: {len(a_list)} / {total_len}", end="\r")

def main():
	profile_link = input("Steam profile link: ")
	
	game_ids = all_game_ids(profile_link)

	# Use multithreading to make getting release years faster.
	threads_no = 20
	segment_size = len(game_ids) // threads_no

	release_years = []
	threads = []

	n = 0
	for i in range(threads_no):
		segment = game_ids[n: n + segment_size]
		thread = threading.Thread(target=get_release_years, args=(segment, release_years, len(game_ids)))
		threads.append(thread)
		n += segment_size
	
	# If there any remaining games that haven't been added to previous threads add them to
	# this thread.
	if len(game_ids) % segment_size != 0:
		segment = game_ids[n:]
		thread = threading.Thread(target=get_release_years, args=(segment, release_years, len(game_ids)))
		threads.append(thread)	

	print("Getting release years from games. Please wait...")
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	
	# Use collections.Counter to get frequency of release year.
	counter = collections.Counter(release_years)
	
	# Sort counter according to release year.
	sorted_counter = dict(sorted(counter.items(), key = lambda n: n[0]))

	# Separate years and frequencies from counter.
	years = sorted_counter.keys()
	frequencies = sorted_counter.values()

	# Create a Bar chart from the data.
	fig = plt.figure()
	plt.bar(years, frequencies, edgecolor="black")
	fig.autofmt_xdate()
	plt.title("Number of games in library by release year")
	
	# Label Axes.
	plt.ylabel("Frequency", fontsize=14)
	plt.xlabel("Release Year", fontsize=14)
	
	plt.show()

if __name__ == "__main__":
	main()
