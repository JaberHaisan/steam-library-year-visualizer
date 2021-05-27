# steam-library-year-visualizer
**External Module Required - bs4, matplotlib**

Creates a bar chart of release year of games in library from a given steam profile link by
scraping from the game pages in steam.

For the following cases scraping will fail according to tests:
1) Games removed from the store can't be accessed. For e.g. https://store.steampowered.com/app/254040
2) Some games do not have a release date in the steam store. For e.g. https://store.steampowered.com/app/8980/
3) For profiles with over 500 games the script cannot access all games because steam blocks access as a part of their DDos protection.
