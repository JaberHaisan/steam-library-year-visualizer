# steam-library-year-visualizer
**External Modules Required - bs4, matplotlib, lxml**

This script scraps release year of games in library from a given steam profile link by
using requests and bs4 and creates a bar chart from the acquired data using matplotlib.

Here's an example result:
![Figure_1](https://user-images.githubusercontent.com/53193365/176496699-ee6677d0-7657-498f-a012-66bc913d9422.png)

For the following cases scraping will fail according to tests:
1) Games removed from the store can't be accessed. For e.g. https://store.steampowered.com/app/254040
2) Some games do not have a release date in the steam store. For e.g. https://store.steampowered.com/app/8980/
