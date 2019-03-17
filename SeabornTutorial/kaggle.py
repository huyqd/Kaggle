##
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

##
# Read datas
median_house_hold_income = pd.read_csv('./input/MedianHouseholdIncome2015.csv', encoding="windows-1252")
percentage_people_below_poverty_level = pd.read_csv('./input/PercentagePeopleBelowPovertyLevel.csv', encoding="windows-1252")
percent_over_25_completed_highSchool = pd.read_csv('./input/PercentOver25CompletedHighSchool.csv', encoding="windows-1252")
share_race_city = pd.read_csv('./input/ShareRaceByCity.csv', encoding="windows-1252")
kill = pd.read_csv('./input/PoliceKillingsUS.csv', encoding="windows-1252")

## Inspect
median_house_hold_income.head()
median_house_hold_income.info()
percentage_people_below_poverty_level.head()
percent_over_25_completed_highSchool.head()
share_race_city.head()
kill.head()

## Barplot
# Poverty rate of each state
percentage_people_below_poverty_level.poverty_rate.replace(['-'], 0.0, inplace=True)
percentage_people_below_poverty_level.columns = ['state', 'city', 'poverty_rate']
percentage_people_below_poverty_level.poverty_rate = percentage_people_below_poverty_level.poverty_rate.astype(float)
poverty_ratio = (percentage_people_below_poverty_level[['state', 'poverty_rate']]
                 .groupby('state')
                 .mean().squeeze()
                 .sort_values(ascending=False))

poverty_ratio = poverty_ratio.reset_index()
poverty_ratio.columns = ['state', 'poverty_ratio']


# visualization
plt.figure(figsize=(15, 10))
sns.barplot(x='state', y='poverty_ratio', data=poverty_ratio)
plt.xticks(rotation=45)
plt.xlabel('States')
plt.ylabel('Poverty Rate')
plt.title('Poverty Rate Given States')
## Highschool ratio
percent_over_25_completed_highSchool.percent_completed_hs.replace(['-'], 0.0, inplace=True)
percent_over_25_completed_highSchool.columns = ['state', 'city', 'highschool_rate']
percent_over_25_completed_highSchool.highschool_rate = percent_over_25_completed_highSchool.highschool_rate.astype(
    float)
highschool_ratio = (percent_over_25_completed_highSchool[['state', 'highschool_rate']]
                    .groupby('state')
                    .mean().squeeze()
                    .sort_values(ascending=False))

highschool_ratio = highschool_ratio.reset_index()
highschool_ratio.columns = ['state', 'highschool_ratio']

##
kill.head()
popular_name = kill.name.str.rsplit(' ', 1, expand=True)[1].value_counts().head(15)
type(popular_name)
plt.figure(figsize=(15,10))
sns.barplot(x=popular_name.index, y=popular_name.values, palette=sns.cubehelix_palette(len(popular_name)))

##
share_race_city.head()
share_race_city = share_race_city.rename(columns={'Geographic area': 'state'})
share_race_city = share_race_city.drop(columns='City')
share_race_city = share_race_city.set_index('state').replace('(X)', 0).replace('-', 0).astype(float)
tmp = share_race_city.groupby('state').sum().sum(axis=1)
share_race_city_ratio = share_race_city.groupby('state').sum().divide(tmp, axis=0)
share_race_city_ratio = share_race_city_ratio.reset_index()
# visualization
f, ax = plt.subplots(figsize=(9, 15))
sns.barplot(x='share_white', y='state', color='green', alpha=0.5, label='White', data=share_race_city_ratio)
sns.barplot(x='share_black', y='state', color='blue', alpha=0.7, label='African American', data=share_race_city_ratio)
sns.barplot(x='share_native_american', y='state', color='cyan', alpha=0.6, label='Native American', data=share_race_city_ratio)
sns.barplot(x='share_asian', y='state', color='yellow', alpha=0.6, label='Asian', data=share_race_city_ratio)
sns.barplot(x='share_hispanic', y='state', color='red', alpha=0.6, label='Hispanic', data=share_race_city_ratio)

ax.legend(loc='lower right', frameon=True)  # legendlarin gorunurlugu
ax.set(xlabel='Percentage of Races', ylabel='States', title="Percentage of State's Population According to Races ")

##
data = highschool_ratio.merge(poverty_ratio, on='state', how='inner')
data = data.set_index('state')
data = data.divide(data.max(), axis=1)
data = data.reset_index()

# visualize
f, ax1 = plt.subplots(figsize=(20, 10))
sns.pointplot(x='state', y='poverty_ratio', data=data, color='lime', alpha=0.8)
sns.pointplot(x='state', y='highschool_ratio', data=data, color='red', alpha=0.8)
plt.text(40, 0.6, 'high school graduate ratio', color='red', fontsize=17, style='italic')
plt.text(40, 0.55, 'poverty ratio', color='lime', fontsize=18, style='italic')
plt.xlabel('States', fontsize=15, color='blue')
plt.ylabel('Values', fontsize=15, color='blue')
plt.title('High School Graduate  VS  Poverty Rate', fontsize=20, color='blue')
plt.grid()

##
g = sns.jointplot(x='highschool_ratio', y='poverty_ratio', data=data, kind="resid", height=7)
##
pal = sns.cubehelix_palette(2, rot=-.5, dark=.3)
sns.violinplot(data=data, palette=pal, inner="points")
plt.show()