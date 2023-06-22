# steam-library-year-visualizer
**External Modules Required - bs4, selenium, matplotlib, lxml**

This script scraps release year of games in library from a given steam profile link by
using requests and bs4 and creates a bar chart from the acquired data using matplotlib.

Note - Steam no longer shows library data unless you are logged in. The script will
give 60s to log in through selenium in order to get the required data.

Here's an example result:
![Figure_1](https://github.com/JaberHaisan/steam-library-year-visualizer/assets/53193365/c80e171d-a685-4182-9142-6804c3363d2f)


For the following cases scraping will fail according to tests:
1) Games removed from the store can't be accessed. For e.g. https://store.steampowered.com/app/254040
2) Some games do not have a release date in the steam store. For e.g. https://store.steampowered.com/app/8980/

