# statcast_hitters_2023
Code and other documentation for a chart radar comparing MLB hitters for the 2023 season.

For this project, I have developed a dashboard on Python that allows users to compare Statcast performance of metrics of MLB players for the ongoing MLB season.

My data source for this project is BaseballSavant (baseballsavant.mlb.com). BaseballSavant is a data collection and visualization website put out by MLB. Unlike most traditional baseball statistic pages which focus on result-based metrics, BaseballSavant uniquely analyzes Statcast metrics, which focus on projected and expected metrics. Officially, according to MLB, Statcast is “a state-of-the-art tracking technology that allows for the collection and analysis of a massive amount of baseball data, in ways that were never possible in the past”. With cameras and radars now installed in every major league ballpark, Statcast can record metrics that cannot be quantified to the naked eye, such as the exit velocity of a batted ball, the sprint speed of a baserunner, or the spin rate of a pitch. With these new collection abilities, new metrics have been created that measure the raw performance of a player’s activities, such as expected metrics. In the project, I use these expected metrics (along with others) that are provided by BaseballSavant to look at the performance of MLB players. Along with this viewing of the individual player, I have created a radar that overlays these metrics for two players, allowing for direct comparisons.

MLB player statistics are incredibly important to keep track of and help individuals with any type of stake in the game make decisions. With the number of statistics looked at, numbers can be hard to sort through and keep track of, as well as understand in a visually clear way. That is the purpose of the project, to create a visually clear and accurate display allowing individuals to search for any MLB player, see how they have performed using different metrics, and compare it to another player.

The final product that allows an individual to search for any MLB players and see all their statistics displayed will be useful to many. General managers care about statistics when making decisions for roster construction and player evaluation. They can also see if a player is overvalued or undervalued, and make decisions in player development and trades. A coach may use this data in scouting and creating a game plan, as well as creating strategy, lineups, and making real-time game decisions. A player can use this data to understand their strengths and weaknesses, as well as evaluate their opponents. A sport better may have a large amount of money on the line and being able to quickly search for a player's on-base percentage, or batting average may be the difference in them winning or losing money, based on the decision they make. Overall, many individuals will benefit from this visual tool and make better-informed decisions.

If a user wants to collect the data themselves, they should first run the get_data.py file.  This file will utilize a web scraping package, Selenium, to obtain data from BaseballSavant, properly format that data into a Pandas data frame, and then upload that data into a .csv file stored in an AWS bucket.  However, please note that a user will have to use their own AWS details in order to run this file properly.  If a user doesn't care about scraping this data themselves, then this file can be ignored.

The chart_code.py file then reads in the data and creates our radar chart visualization.  The chart can be viewed in mediums such as Jupyter, Spyder, etc, but cannot be seen from the command prompt.  However, if you are experiencing issues with viewing the chart, an example can be seen in the judge_kepler.png file in the repository.

A more comprehensive and step-by-step explanation of this chart, its interpretation, and its creation is available in the radar_chart.ipynb file in this repository.
