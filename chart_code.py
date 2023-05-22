#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Import Packages
import pandas as pd
from mplsoccer import Radar, FontManager, grid
import matplotlib.pyplot as plt
from ipywidgets import widgets, interactive


# In[ ]:


#Load in Desired Fonts
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


# In[ ]:


#Create Function to Create Radar Chart
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
        player1_vals = [player1[x] for x in range(len(player1)) if player1[x] != 'missing']
        for x in range(len(df['Name'])):
            if player_2 in df['Name'][x]:
                player2 = df.loc[x]
        player2_name = player2[0]
        player2_vals = [player2[x] for x in range(len(player2)) if player2[x] != 'missing']
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


# In[ ]:


#Display Chart
player1 = widgets.Dropdown(options = ['Aaron Judge'] + list(df['Name'].unique()), value = 'Aaron Judge', description = 'Player:')
player2 = widgets.Dropdown(options = ['Paul Goldschmidt'] + list(df['Name'].unique()), value = 'Paul Goldschmidt', description = 'Player:')
interactive(comp, player_1=player1, player_2=player2)

