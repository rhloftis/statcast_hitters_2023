#!/usr/bin/env python
# coding: utf-8

# # Team 3 Final Project: Statcast Comparison Radar for the 2023 MLB Season
# By Richard Loftis

# For our project, we have developed a dashboard on Python that allows users to compare Statcast performance of metrics of MLB players for the ongoing MLB season.
# 
# Our data source for this project is BaseballSavant (baseballsavant.mlb.com). BaseballSavant is a data collection and visualization website put out by MLB. Unlike most traditional baseball statistic pages which focus on result-based metrics, BaseballSavant uniquely analyzes Statcast metrics, which focus on projected and expected metrics. Officially, according to MLB, Statcast is “a state-of-the-art tracking technology that allows for the collection and analysis of a massive amount of baseball data, in ways that were never possible in the past”. With cameras and radars now installed in every major league ballpark, Statcast can record metrics that cannot be quantified to the naked eye, such as the exit velocity of a batted ball, the sprint speed of a baserunner, or the spin rate of a pitch. With these new collection abilities, new metrics have been created that measure the raw performance of a player’s activities, such as expected metrics. In our project, we use these expected metrics (along with others) that are provided by BaseballSavant to look at the performance of MLB players. Along with this viewing of the individual player, we have created a radar that overlays these metrics for two players, allowing for direct comparisons.
# 
# MLB player statistics are incredibly important to keep track of and help individuals with any type of stake in the game make decisions. With the number of statistics looked at, numbers can be hard to sort through and keep track of, as well as understand in a visually clear way. That is the purpose of our project, to create a visually clear and accurate display allowing individuals to search for any MLB player, see how they have performed using different metrics, and compare it to another player.
# 
# The final product that allows an individual to search for any MLB players and see all their statistics displayed will be useful to many. General managers care about statistics when making decisions for roster construction and player evaluation. They can also see if a player is overvalued or undervalued, and make decisions in player development and trades. A coach may use this data in scouting and creating a game plan, as well as creating strategy, lineups, and making real-time game decisions. A player can use this data to understand their strengths and weaknesses, as well as evaluate their opponents. A sport better may have a large amount of money on the line and being able to quickly search for a player's on-base percentage, or batting average may be the difference in them winning or losing money, based on the decision they make. Overall, many individuals will benefit from this visual tool and make better-informed decisions.   

# ## Step 1: Load in Data using Selenium

# ### Detailed Steps:
# 
# Firstly, we need to import our the necessary packages to extract our data from the BaseballSavant site.  For this we import the selenium package and its other attachments.  With these loaded in, we call selenium and then use the driver to open up our desired webpage which we specified with our URL.  After webdriver opens the webpage, we then specify which table we would like to extract data from and then have webdriver extract the desired information by specifying the rows Xpath.  After we extract this information, we then store it in a list called data and then close the webpage.
# 
# It is important that we have a program which can webscrape BaseballSavant's content rather than just download a CSV file because a player's metrics change with each plate appearance they make.  Since baseball metrics are calculated on the aggregate, BaseballSavant updates their leaderboards daily, meaning we cannot download static data which does not represent accurate performances.

# In[10]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
serv_obj = Service("C:\\Users\\rhlof\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver = webdriver.Chrome(service=serv_obj)
url = 'https://baseballsavant.mlb.com/leaderboard/custom?year=2023&type=batter&filter=&sort=4&sortDir=desc&min=1&selections=b_k_percent,b_bb_percent,xba,xslg,xwoba,xobp,xiso,xwobacon,xbacon,exit_velocity_avg,hard_hit_percent,avg_best_speed,&chart=false&x=xba&y=xba&r=no&chartType=beeswarm'
driver.get(url)
wait = WebDriverWait(driver, 10)
xpath = '/html/body/div[2]/div/div/table'
table = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
rows = table.find_elements(By.XPATH, "//tbody/tr")
data = []
for row in rows:
    cells = row.find_elements(By.XPATH, "td")
    data.append([cell.text for cell in cells])
driver.close()


# ## Step 2: Create Pandas DataFrame

# ### Detailed Steps:
# 
# After loading the data into a list, we need to put it into a Pandas dataframe.  We specify the columns names we want and then load in the data in our list to rows in the dataframe.  After this, we have to do some cleaning of our data.  Firstly, our initial list 'data' contains some information about the games which are being played on the given day, which is not useful for our project.  We make sure that we do not include this data by filtering out our list 'data' to include on the necessary statistics.  Also, since we are using another dataset to add more details in the visualization, we need to make sure the player names are identical in both our datasets.  Although we removed all non-player instances in the data list, the player names are not in correct order, so we have to change it from last name, first name format into our desired format, which is first name then last name.  Also, there are some players in the BaseballSavant dataset which include name suffixes which aren't included in the MLBIDS dataset.  These instances are when players include titles such as 'Jr.' or 'III' which are only recognized by one of our datasets.  The names of these players are stored in the list 'bad_names'.  After we take account of these, we then create a new list called 'names' with the proper names, and then replace our initial 'Player' column with these correct values in a column called 'Names'.  We then drop our unecessary columns, 'Player' and 'index'.  After this, we then make sure our columns are in our desired order and are numeric types.  Then, we drop all rows which may have null values.

# In[11]:


data


# In[12]:


import pandas as pd
data1 = [x for x in data if x[0] != '' ]
col_names = ['Rank','Player', 'Year', 'K %', 'BB %','xBA', 'xSLG', 'xwOBA', 'xOBP', 'xISO', 'xwOBACON', 'xBACON', 'Exit Velo', 'Hard Hit %', 'Max Exit Velo']
df = pd.DataFrame(data1, columns = col_names).drop(columns = ['Rank', 'Year'])
names = []
for x in range(len(df['Player'])):
    names.append(df['Player'][x].split(',')[1].strip() + ' ' + df['Player'][x].split(',')[0])
bad_names = ['Brent Rooker Jr.', 'Cedric Mullins II', 'George Springer III', 'Joey Wiemer Jr.', 'Luke Voit III', 
         'MJ Melendez Jr.', 'Nelson Cruz Jr.', 'TJ Friedl Jr.', 'Trey Mancini III']
for x in range(len(names)):
    if names[x] in bad_names:
        split = names[x].split(' ')
        names[x] = split[0] + ' ' + split[1]    
df['Name'] = names
df = df.sort_values(['Name'], ascending = [True]).reset_index()
df = df.drop(columns = ['Player', 'index']).reset_index(drop=True)
df[['K %', 'BB %','xBA', 'xSLG', 'xwOBA', 'xOBP', 'xISO', 'xwOBACON', 'xBACON', 'Exit Velo', 'Hard Hit %', 'Max Exit Velo']] = df[['K %', 'BB %','xBA', 'xSLG', 'xwOBA', 'xOBP', 'xISO', 'xwOBACON', 'xBACON', 'Exit Velo', 'Hard Hit %', 'Max Exit Velo']].apply(pd.to_numeric) 
df = df.loc[:,['Name','xBA', 'xSLG', 'xwOBA', 'xOBP', 'xISO', 'xwOBACON', 'xBACON','Exit Velo', 'Max Exit Velo', 'Hard Hit %','K %', 'BB %']]
for x in df.columns:
    df = df[df[x].notna()]


# In[13]:


df


# ## Step 3: Send Data to an AWS Bucket for URL Retreival

# ### Detailed Steps:
# 
# Since it takes some time for our data to be scraped in from BaseballSavant, we store our dataframe into a csv file and then place that in an AWS bucket.  Being stored under the name 'final_proj_2023.csv', we can then retreive our file using a simple URL instead of having to load in our data using Selenium whenever we want to use the dataframe.  Although this project write up exists in just one Jupyter Notebook file, we originally had it in two files, one where the data was webscraped, uploaded, and stored in an AWS Bucket, and one where we would create our visualization.  With this, we could upload our data in the visualization file by using the bucket item URL.
# 
# Since player performance metrics change daily since games are played each day, it is important that we are able to accurately update our data.  By webscapring BaseballSavant, converting the data into a dataframe, and then storing it in an AWS bucket with an accessible link, we are able to simply run a file and update the data whenever needed.

# In[14]:


import os
import boto3

aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key1']
s3 = boto3.client('s3', region_name='us-east-1', 
                        # Set up AWS credentials 
                        aws_access_key_id=aws_access_key_id, 
                         aws_secret_access_key=aws_secret_access_key)
from io import StringIO
resource = boto3.resource(
    's3',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key
)
from io import StringIO
import csv
bucket = 'bigdata.assignments'
file_name = "final_proj_2023.csv"
csv_buffer = StringIO()
df.to_csv(csv_buffer, index = False, encoding='utf-8-sig')
resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())


# ## Load in Necessary Packages

# ### Detailed Steps:
# 
# For our visualization we will be creating a metric radar via the mplsoccer package.  To create this, we need to install the mplsoccer package, as well as matplotlib. Additionally, since the user of the graph will be able to select their desired players from a dropdown menu, we need to import the ipywidgets package.  After loading in our packages, we are also uploading some specific fonts to use in our visualization.

# In[15]:


import pandas as pd
from mplsoccer import Radar, FontManager, grid
import matplotlib.pyplot as plt
from ipywidgets import widgets, interactive


# In[16]:


URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-Regular.ttf')
serif_regular = FontManager(URL1)
URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-ExtraLight.ttf')
serif_extra_light = FontManager(URL2)
URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
        'RubikMonoOne-Regular.ttf')
rubik_regular = FontManager(URL3)
URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
robotto_thin = FontManager(URL4)
URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')
robotto_bold = FontManager(URL5)


# ## Create Function for Visualization

# ### Specific Details:
# 
# Now create our function to make our visualization.  For our inputs, we take two player names which we will use as our comparisons.  After taking these inputs, our function retreives these names from our BaseballSavant dataset.  Additionally, we are loading in our datasets: the BaseballSavant data as well as the MLB IDs dataset provided by Razzball, which we use so we can provide additional information about the player in our visualization, specifically their team and position.  The Razzball dataset is stored in an AWS bucket and is given a public URL, which we will use to access the data in our radar.  In order to make sure the names in the BaseballSavant and MLB IDs sets match, we are also doing some final cleaning.  As well as this, we make sure that if there are any N/A values in our BaseballSavant dataset, we replace them with the string 'missing'. With our names, we then extract their statistics and store them in a list called values.  We also make sure that we only put in the values which are present in the player's row.  After we have their stats, we then take then calculate the values that are in the 5th and 95th percentile for each metric we are looking at.  These values will be used as the ranges for each metric we observe.  We also create a list called params which is the names of all the metrics that will be plotted on the visualization.
# 
# After this we create a function called get_teampos, which retreives the player's team and position from the MLB IDs dataset.  However, there are some names in the dataset that still do not match those in the BaseballSavant set, so we have to specify those player names in the function creation to make sure they have their proper teams and positions.  After creating our function, we then call it on the player name and store their team and position in to variables.  With this, we are ready to begin creating the visualization.
# 
# Using the Radar function from mplsoccer, we load in the player values and the range values.  Additionally, we make sure our visualization knows that for K %, it is better to have a lower value than high value.  We also specify that we want 10 rings in our radar.  With our radar_inner function, we specify that we want our rings to be light grey.  With the rings_output function, we specify that we want the color of our first player's radar to be red and our second player to be blue, as well as wanting our visualization to be a comparison radar.  After this, we specify the font we want for our labels.
# 
# Next, we add the titles for our visualization.  We set our main title as "Statcast Comparison Radar for the 2023 MLB Season".  We also set our endnote title, which credits the data as coming from BaseballSavant, lists who created the visualization, as well as adknowledging that the visualization is inspired by similar radars created by Statsbomb. Then, we but titles that display the player's name, team, and position.  The font color for these player specific titles are specified to be the same color as their radar chart. Lastly, we set the background color of the visualization

# In[17]:


def comp(player_1, player_2):
        df = pd.read_csv('https://s3.amazonaws.com/bigdata.assignments/final_proj_2023.csv')
        df.fillna('missing', inplace = True)
        mlbids = pd.read_csv('https://s3.amazonaws.com/bigdata.assignments/mlb_ids+-+Sheet1.csv')
        for x in range(len(mlbids)):
            mlbids['Name'][x] = mlbids['Name'][x].replace("’", "'")
        for x in range(len(df['Name'])):
            if player_1 in df['Name'][x]:
                player1 = df.loc[x]
        player1_name = player1[0]
        player1_vals = []
        for x in range(len(player1)):
            if player1[x] != 'missing':
                player1_vals.append(player1[x])
        for x in range(len(df['Name'])):
            if player_2 in df['Name'][x]:
                player2 = df.loc[x]
        player2_name = player2[0]
        player2_vals = []
        for x in range(len(player2)):
            if player2[x] != 'missing':
                player2_vals.append(player2[x])
        player1_vals = player1_vals[1:]
        player2_vals = player2_vals[1:]
        high = [round(x,3) for x in df.quantile(0.95)]
        low = [round(x,3) for x in df.quantile(0.05)]
        params = [x for x in df.columns[1:]]
        def get_teampos(player_name):
            if player_name == 'Will Smith':
                team = mlbids[mlbids['Name'] == player_name].iloc[1,5]
                position = mlbids[mlbids['Name'] == player_name].iloc[1,6]
            elif player_name == 'Franchy Cordero':
                team = 'NYY'
                position = '1B/OF'
            elif player_name == 'Ji Man Choi':
                team = 'PIT'
                position = '1B'
            elif player_name == 'Yuli Gurriel':
                team = 'MIA'
                position = '1B'
            else:
                team = mlbids[mlbids['Name'] == player_name].iloc[0,5]
                position = mlbids[mlbids['Name'] == player_name].iloc[0,6]
            return(team, position)
        info1 = get_teampos(player1_name)
        team1 = info1[0]
        pos1 = info1[1]
        info2 = get_teampos(player2_name)
        team2 = info2[0]
        pos2 = info2[1]
        radar = Radar(params, low, high, lower_is_better = ['K %'],round_int=[False]*len(params),
              num_rings=10, ring_width=1, center_circle_radius=1)
        fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)
        radar.setup_axis(ax=axs['radar'], facecolor = 'none')
        rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='gainsboro', edgecolor='lightgrey')
        radar_output = radar.draw_radar_compare(player1_vals, player2_vals, ax=axs['radar'],
                                        kwargs_radar={'facecolor': 'lightcoral', 'alpha': 0.6, 'edgecolor': 'red'},
                                        kwargs_compare={'facecolor': 'cornflowerblue', 'alpha': 0.6, 'edgecolor' : 'navy'})
        radar_poly, radar_poly2, vertices1, vertices2 = radar_output
        range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=15,
                                       fontproperties=robotto_thin.prop)
        param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=15,
                                       fontproperties=robotto_bold.prop)
        fig.text(
                0.5, 0.97, "Statcast Comparison Radar for the 2023 MLB Season", size=35,
                ha="center", fontproperties=robotto_bold.prop, color="#000000"
            )
        endnote_text = axs['endnote'].text(0.99, 0.5, 'Inspired By: StatsBomb\nData provided by BaseballSavant and Razzball\nBy Richard Loftis', fontsize=15,
                                   fontproperties=robotto_thin.prop, ha='right', va='center')
        title1_text = axs['title'].text(0.01, -0.25, player1_name, fontsize=25, color='crimson',
                                fontproperties=robotto_bold.prop, ha='left', va='center')
        title2_text = axs['title'].text(0.01, -.6, team1 + ', ' + pos1, fontsize=20,
                                fontproperties=robotto_thin.prop,
                                ha='left', va='center', color='crimson')
        title3_text = axs['title'].text(0.99, -0.25, player2_name, fontsize=25,
                                fontproperties=robotto_bold.prop,
                                ha='right', va='center', color='blue')
        title4_text = axs['title'].text(0.99, -.6, team2 + ', ' + pos2, fontsize=20,
                                fontproperties=robotto_thin.prop,
                                ha='right', va='center', color='blue')


# ## Call Function to Create Visualization

# ### Detailed Steps:
# 
# After creating our function, we set our default players to be compared as Aaron Judge and Paul Goldschmidt, both the reigning MVPs from their respect leagues.  We set the player1 and player2 variables as widget items, allowing for the user to select not only the specified players for the comparison chart, but use a drop down list to compare any two players in the entire dataset.  We do this by calling the interactive function on our created function 'comp' with the arguments for that function being the two widget items we just created.  After executing that cell, our radar chart is created.

# In[18]:


player1 = widgets.Dropdown(options = ['Aaron Judge'] + list(df['Name'].unique()), value = 'Aaron Judge', description = 'Player:')
player2 = widgets.Dropdown(options = ['Paul Goldschmidt'] + list(df['Name'].unique()), value = 'Paul Goldschmidt', description = 'Player:')


# In[19]:


interactive(comp, player_1=player1, player_2=player2)


# ## Radar Interpretation:
# 
# With our visualization, we a plotting hitting performance metrics onto a radar chart.  Put simply, the larger and more circular a player's radar chart looks, the better they are performing in our selected metrics.  With this comparison feature, a user can tell who is having the better season as a hitter, which answers our inital business question.  With this information, a general manager can compare two players who they may be interested in acquiring and determine who is better.  Coaches and those who set the lineups can also use this visualization to compare different batters they already have in their teams and decide who should play over another player.  Additionally, sports bettors can use this information and visualization to help inform their bets.  Also, since many of these metrics may not be common knowledge for even the average baseball fan, we have attached a glossary at the bottom of this file to help give specific interpretations and definitions for each metric mentioned.
# 
# For example, as of 4/16/23, the New York Yankees are dealing with a lot of injured players on their roster, specifically with their outfield, where two everyday starters in Giancarlo Stanton and Harrison Bader are unavailable to play.  With these holes in the current roster, their manager would have to choose players to step into their place and take over the starting position.  Two candidates for a starting spot are outfielders Franchy Cordero and Aaron Hicks.  If the manager of the Yankees, Aaron Boone, was having a difficult time choosing who to start between Cordero and Hicks, our visualization tool would be very helpful in projecting who would perform best.  Boone could choose to compare Hicks' and Cordero's metrics with our tool and see that Cordero is outperforming Hicks in nearly every metric and would likley be a more effective replacement for Stanton or Bader, as can be seen below:

# In[66]:


player1 = widgets.Dropdown(options = ['Aaron Hicks'] + list(df['Name'].unique()), value = 'Aaron Hicks', description = 'Player:')
player2 = widgets.Dropdown(options = ['Franchy Cordero'] + list(df['Name'].unique()), value = 'Franchy Cordero', description = 'Player:')


# In[67]:


interactive(comp, player_1=player1, player_2=player2)


# ## Glossary:

# ### xBA:
# 
# Expected Batting Average (xBA): xBA measures the likelihood that a batted ball will become a hit. Each batted ball is assigned an xBA based on how often comparable balls -- in terms of exit velocity, launch angle and, on certain types of batted balls, Sprint Speed -- have become hits since Statcast was implemented Major League wide in 2015. By comparing expected numbers to real-world outcomes over a period of time, it can be possible to identify which hitters (or pitchers) are over- or under-performing their demonstrated skill.

# ### xSLG:
# 
# Expected Slugging Percentage (xSLG): xSLG is formulated using exit velocity, launch angle and, on certain types of batted balls, Sprint Speed.  In the same way that each batted ball is assigned an expected batting average, every batted ball is given a single, double, triple and home run probability based on the results of comparable batted balls since Statcast was implemented Major League wide in 2015.  All hit types are valued in the same fashion for Expected Slugging Percentage as they are in the formula for standard slugging percentage, with doubles being worth twice as much, triples being worth three times as much and homers being worth four times as much as singles. The single, double, triple and home run probabilities for an individual batted ball are plugged into the formula for slugging percentage -- (1B + 2Bx2 + 3Bx3 + HRx4)/AB) -- to get a player's Expected Slugging Percentage on said batted ball.

# ### xwOBA:
# 
# Expected Weighted On-base Average (xwOBA): xwOBA is formulated using exit velocity, launch angle and, on certain types of batted balls, Sprint Speed. All hit types are valued in the same fashion for xwOBA as they are in the formula for standard wOBA: (unintentional BB factor x unintentional BB + HBP factor x HBP + 1B factor x 1B + 2B factor x 2B + 3B factor x 3B + HR factor x HR)/(AB + unintentional BB + SF + HBP), where "factor" indicates the adjusted run expectancy of a batting event in the context of the season as a whole. Unlike xOBP, xwOBA accounts for how a player reached base -- instead of simply considering whether a player reached base. The value for each method of reaching base is determined by how much that event is worth in relation to projected runs scored (example: a double is worth more than a single).

# ### xOBP
# 
# Expected On-base Percentage (xOBP): xOBP is formulated using exit velocity, launch angle and, on certain types of batted balls, Sprint Speed.  This measure refers to how frequently a batter is expected to reache base on a per plate appearance based on the results of their batted balls and at bats.  Unlike xwOBA, xOBP does not take into account the values of reaching different bases.

# ### xISO:
# 
# Expected Isolated Power (xISO): xISO is formulated using exit velocity, launch angle and, on certain types of batted balls, Sprint Speed.  xISO measures the raw power of a hitter by taking only the player's batted balls' probabilities of being extra-base hits -- and the type of extra-base hit -- into account.  

# ### xwOBACON:
# 
# Expected Weighted On-base Average on Contact (xwOBACON): xwOBACON is formulated using exit velocity, launch angle and, on certain types of batted balls, Sprint Speed. xwOBACON is a very similar measure to xwOBA, except xwOBACON takes into account a player's xwOBA when looking at balls put in contact.  This metrics eliminates the impact of walks and strike outs when looking at a player's performance at the plate, instead focusing on only their contact quality.

# ### xBACON:
# 
# Expected Batting Average on Contact (xBACON): xBACON is very similar to xwOBACON, except it does not added weighted values for the xBA of balls that are put in play.  Often, xBACON is used as an alternative to another metric called BABIP, which measures a player's batting average exclusively on balls hit into the field of play, removing outcomes not affected by the opposing defense (such as home runs).  xBACON is able to take into account home runs in its calculation, making it a better alternative to BABIP.

# ###  Average Exit Velocity:
# 
# Exit Velocity (EV) measures the speed of the baseball as it comes off the bat, immediately after a batter makes contact. In this instance, we are looking at a player's average exit velocity for instances where they made contact.

# ### Maximum Exit Velocity:
# 
# Similar to average exit velocity, maximum exit velocity is the highest speed in which a baseball has come off the respective player's bat through the entirety of the season.

# ### Hard Hit Rate:
# 
# Hard Hit Rate is the percentage of batted balls for a player which were marked as having an exit velocity of 95 miles per hour or higher.

# ### K%:
# 
# K% is the percentage of at bats which ended in a strike out for the batter.

# ### BB%:
# 
# BB% is the percentage of at bats which ended in the batter walking for the season.
