#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Import Packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import boto3
from io import StringIO
from io import StringIO
import csv


# In[ ]:


#Web Scrape Data from BaseballSavant using Selenium
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


# In[ ]:


#Format Raw Data into Appropriate Pandas Data Frame
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


# In[ ]:


#Upload the File to an AWS Bucket to Become Publically Accessible
#If you plan to upload data to your own AWS Bucket, follow the instructions below
#If not, skip this portion of the code and we can use the data already stored in my bucket


#I use my own AWS ID and key for this step, replace aws_access_key_id with your own AWS ID and aws_secret_access_key with your own access key
aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key1']
s3 = boto3.client('s3', region_name='us-east-1', 
                        aws_access_key_id=aws_access_key_id, 
                         aws_secret_access_key=aws_secret_access_key)

resource = boto3.resource(
    's3',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key
)

# I use my own bucket for this, replace bucket with your own bucket name
bucket = 'bigdata.assignments'
file_name = "final_proj_2023.csv"
csv_buffer = StringIO()
df.to_csv(csv_buffer, index = False, encoding='utf-8-sig')
resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())

