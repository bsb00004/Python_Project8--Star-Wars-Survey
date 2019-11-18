#!/usr/bin/env python
# coding: utf-8

# ### Project8--Star Wars Survey
# While waiting for Star Wars: The Force Awakens to come out, the team at [FiveThirtyEight](https://fivethirtyeight.com/) became interested in answering some questions about Star Wars fans. In particular, they wondered: does the rest of America realize that “The Empire Strikes Back” is clearly the best of the bunch?
# 
# The team needed to collect data addressing this question. To do this, they surveyed Star Wars fans using the online tool SurveyMonkey. They received 835 total responses, which you download from their [GitHub repository](https://github.com/fivethirtyeight/data/tree/master/star-wars-survey).
# 
# For this project, you'll be cleaning and exploring the data set called __'star_wars.csv'__.
# 
# The data has several columns, including:
# 
# - __RespondentID__ - An anonymized ID for the respondent (person taking the survey)
# - __Gender__ - The respondent's gender
# - __Age__ - The respondent's age
# - __Household Income__ - The respondent's income
# - __Education__ - The respondent's education level
# - __Location (Census Region)__ - The respondent's location
# - __Have you seen any of the 6 films in the Star Wars franchise?__ - Has a Yes or No response
# - __Do you consider yourself to be a fan of the Star Wars film franchise?__ - Has a __Yes__ or __No__ response
# 
# There are several other columns containing answers to questions about the Star Wars movies. For some questions, the respondent had to check one or more boxes. This type of data is difficult to represent in columnar format. As a result, this data set needs a lot of cleaning.
# 
# The following code will read the data into a pandas dataframe:

# In[33]:


import pandas as pd
star_wars = pd.read_csv("star_wars.csv", encoding="ISO-8859-1")

# Exploring the data & Looking for any strange values in the columns and rows.
star_wars.head(10)


# In[34]:


# Review the column names with star_wars.columns.
star_wars.columns


# First, you'll need to remove the invalid rows. For example, __RespondentID__ is supposed to be a unique ID for each respondent, but it's blank in some rows. You'll need to remove any rows with an invalid __RespondentID__.

# In[35]:


# Remove any rows where RespondentID is NaN.
star_wars = star_wars[pd.notnull(star_wars["RespondentID"])]


# In[36]:


# Check the result after removing null values
star_wars.head()
star_wars.columns


# Now looking at the next two columns, which are:
# 
# - Have you seen any of the 6 films in the Star Wars franchise?
# - Do you consider yourself to be a fan of the Star Wars film franchise?
# 
# Both represent __Yes/No__ questions. They can also be __NaN__ where a respondent chooses not to answer a question. We can use the pandas.Series.value_counts() method on a series to see all of the unique values in a column, along with the total number of times each value appears.

# In[37]:



star_wars['Have you seen any of the 6 films in the Star Wars franchise?'].value_counts()
star_wars['Do you consider yourself to be a fan of the Star Wars film franchise?'].value_counts()


# Both columns are currently string types, because the main values they contain are __Yes__ and __No__. We can make the data a bit easier to analyze down the road by converting each column to a Boolean having only the values __True__, __False__, and __NaN__. Booleans are easier to work with because we can select the rows that are __True__ or __False__ without having to do a string comparison.
# 
# We used the pandas.Series.map() method on series objects to perform the conversion. 
# series will end up looking like this:
# - __[True, False, NaN, True]__

# In[38]:


# using a dictionary to define a mapping from each value in series to a new value
yes_no = {"Yes": True, "No": False}
# Converting  both columns to the Boolean type
for col in [
    "Have you seen any of the 6 films in the Star Wars franchise?",
    "Do you consider yourself to be a fan of the Star Wars film franchise?"
    ]:
    star_wars[col] = star_wars[col].map(yes_no)# calling the map() function to perform the mapping

star_wars.head()


# The next six columns represent a single checkbox question. The respondent checked off a series of boxes in response to the question, __Which of the following Star Wars films have you seen? Please select all that apply__.
# 
# The columns for this question are:
# 
# - Which of the following Star Wars films have you seen? Please select all that apply. - Whether or not the respondent saw Star Wars: Episode I The Phantom Menace.
# - Unnamed: 4 - Whether or not the respondent saw Star Wars: Episode II Attack of the Clones.
# - Unnamed: 5 - Whether or not the respondent saw Star Wars: Episode III Revenge of the Sith.
# - Unnamed: 6 - Whether or not the respondent saw Star Wars: Episode IV A New Hope.
# - Unnamed: 7 - Whether or not the respondent saw Star Wars: Episode V The Empire Strikes Back.
# - Unnamed: 8 - Whether or not the respondent saw Star Wars: Episode VI Return of the Jedi.
# 
# For each of these columns, if the value in a cell is the name of the movie, that means the respondent saw the movie. If the value is NaN, the respondent either didn't answer or didn't see the movie. We'll assume that they didn't see the movie.
# 
# We are converting each of these columns to a Boolean, then rename the column something more intuitive. We can convert the values the same way we did earlier, except that we'll need to include the movie title and __NaN__ in the mapping dictionary.

# In[39]:


import numpy as np
# creating dictionary to covert to boolean value 
movie_mapping = {
    "Star Wars: Episode I  The Phantom Menace": True,
    np.nan: False,
    "Star Wars: Episode II  Attack of the Clones": True,
    "Star Wars: Episode III  Revenge of the Sith": True,
    "Star Wars: Episode IV  A New Hope": True,
    "Star Wars: Episode V The Empire Strikes Back": True,
    "Star Wars: Episode VI Return of the Jedi": True
}
# mapping above dictionary from columns
for col in star_wars.columns[3:9]:
    star_wars[col] = star_wars[col].map(movie_mapping)
star_wars.head()


# After calling the __map()__ method on a series, the column should only contain the values __True__ and __False_-.
# 
# Next, we'll need to rename the columns to better reflect what they represent. We can use the __pandas.DataFrame.rename()__ method on dataframes to accomplish this.
# 
# The __df.rename()__ method works a lot like __map()__. We pass it a dictionary that maps the current column names to new ones.
# 
# This method will only rename the columns we specify in the dictionary, and won't change the names of other columns. The code above will rename the

# In[40]:


# Renaming each of the columns above so the names are more intuitive
star_wars = star_wars.rename(columns={
        "Which of the following Star Wars films have you seen? Please select all that apply.": "seen_1",
        "Unnamed: 4": "seen_2",
        "Unnamed: 5": "seen_3",
        "Unnamed: 6": "seen_4",
        "Unnamed: 7": "seen_5",
        "Unnamed: 8": "seen_6"
        })

star_wars.head()


# The next six columns ask the respondent to rank the Star Wars movies in order of least favorite to most favorite. __1__ means the film was the most favorite, and __6__ means it was the least favorite. Each of the following columns can contain the value __1, 2, 3, 4, 5, 6, or NaN__:
# 
# - Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film. - How much the respondent liked Star Wars: Episode I The Phantom Menace
# - Unnamed: 10 - How much the respondent liked Star Wars: Episode II Attack of the Clones
# - Unnamed: 11 - How much the respondent liked Star Wars: Episode III Revenge of the Sith
# - Unnamed: 12 - How much the respondent liked Star Wars: Episode IV A New Hope
# - Unnamed: 13 - How much the respondent liked Star Wars: Episode V The Empire Strikes Back
# - Unnamed: 14 - How much the respondent liked Star Wars: Episode VI Return of the Jedi
# 
# Fortunately, these columns don't require a lot of cleanup. We are converting each column to a numeric type, though, then renaming the columns so that we can tell what they represent more easily.
# 
# We can do the numeric conversion with the pandas.DataFrame.astype() method on dataframes.

# In[43]:


# Converting each of the columns above to a float type
star_wars[star_wars.columns[9:15]] = star_wars[star_wars.columns[9:15]].astype(float)
# Renaming each column a more descriptive name
star_wars = star_wars.rename(columns={
        "Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.": "ranking_1",
        "Unnamed: 10": "ranking_2",
        "Unnamed: 11": "ranking_3",
        "Unnamed: 12": "ranking_4",
        "Unnamed: 13": "ranking_5",
        "Unnamed: 14": "ranking_6"
        })

star_wars.head()


# Now that we've cleaned up the ranking columns, we can find the highest-ranked movie more quickly. To do this, take the mean of each of the ranking columns using the pandas.DataFrame.mean() method on dataframes.

# In[44]:


# Computing mean of each of the renking columns
star_wars[star_wars.columns[9:15]].mean()


# #### Making a bar chart of each ranking.

# In[45]:


# matplotlib inline is used for juypter notebook
get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt

plt.bar(range(6), star_wars[star_wars.columns[9:15]].mean())


# ### Rankings
# So far, we've cleaned up the data, renamed several columns, and computed the average ranking of each movie. As I suspected, it looks like the "original" movies are rated much more highly than the newer ones.
# 
# That means we can figure out how many people have seen each movie just by taking the sum of the column (even though they contain Boolean values).

# In[46]:


# computing the sum of each of the seen columns.
star_wars[star_wars.columns[3:9]].sum()


# In[47]:


# Making a bar chart of each ranking
plt.bar(range(6), star_wars[star_wars.columns[3:9]].sum())


# ### View counts
# It appears that the original movies were seen by more respondents than the newer movies. This reinforces what we saw in the rankings, where the earlier movies seem to be more popular.
# 
# We know which movies the survey population as a whole has ranked the highest. Now let's examine how certain segments of the survey population responded. There are several columns that segment our data into two groups. Here are a few examples:
# 
# - Do you consider yourself to be a fan of the Star Wars film franchise? - __True__ or __False__
# - Do you consider yourself to be a fan of the Star Trek franchise? - __Yes__ or __No__
# - Gender - __Male__ or __Female__
# 
# We can split a dataframe into two groups based on a binary column by creating two subsets of that column.The subsets will allow us to compute the most viewed movie, the highest-ranked movie, and other statistics separately for each group.

# In[48]:


# Spliting the data into two groups based on one of the binary columns above
males = star_wars[star_wars["Gender"] == "Male"]
females = star_wars[star_wars["Gender"] == "Female"]


# In[49]:


# plotting seperatly for each group from ranking columns
plt.bar(range(6), males[males.columns[9:15]].mean())
plt.show()

plt.bar(range(6), females[females.columns[9:15]].mean())
plt.show()


# In[50]:


# plotting seperatly for each group from seen columns
plt.bar(range(6), males[males.columns[3:9]].sum())
plt.show()

plt.bar(range(6), females[females.columns[3:9]].sum())
plt.show()


# ### Male/Female differences in favorite Star Wars movie and most seen movie
# Interestingly, more males watches episodes 1-3, but males liked them far less than females did.
# 
# #### Here are some potential next steps:
# 
# - Try to segment the data based on columns like __Education, Location (Census Region), and Which character shot first?__, which aren't binary. Are they any interesting patterns?
# - Clean up columns __15__ to __29__, which contain data on the characters respondents view favorably and unfavorably.
#     - Which character do respondents like the most?
#     - Which character do respondents dislike the most?
#     - Which character is the most controversial (split between likes and dislikes)?

# In[ ]:




