# steam-library-year-visualizer
**External Module Required - bs4, matplotlib, lxml**

This script scraps release year of games in library from a given steam profile link by
using requests and bs4 and creates a bar chart from the acquired data using matplotlib.

You can use my steam profile link if you just want to see how it works:
https://steamcommunity.com/profiles/76561198977690354/

Here's an example result:

![Figure_1](https://user-images.githubusercontent.com/53193365/161325105-131c4e51-9434-40d2-990a-3e8cc07b553d.png)


For the following cases scraping will fail according to tests:
1) Games removed from the store can't be accessed. For e.g. https://store.steampowered.com/app/254040
2) Some games do not have a release date in the steam store. For e.g. https://store.steampowered.com/app/8980/
3) For profiles with over 500 games the script cannot access all games because steam blocks access as a part of their DDos protection.
