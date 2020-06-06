#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install notebook --upgrade --user
import pandas as pd
import plotly.express as px
import csv
from ipywidgets import interact


# In[2]:


file = open('tweets.csv')
file_reader = csv.reader(file)
file_list = list(file_reader)

#Generate a data frame out of the raw data

df=pd.DataFrame(file_list,columns=['text','created_at','retweet_count','favorite_count'])
print(df)


# In[3]:


#Split the created_at time of each tweet into month, day, and hour time

time = df['created_at']
for i in range(1,len(time)):
    a = time[i].split(' ')
    b = a[0].split('-')
    c = a[1].split(':')
    time[i] = [b[0],b[1],c[0],c[0]+':'+c[1]]
time_df = pd.DataFrame(list(time.drop(0)),columns=['Month','Day','Hour','Hour_Minute'])

#Create three histograms to show the amount of tweets Trump has posted according to the change of month, day,and hour

month_hist = px.histogram(time_df,x='Month')
month_hist.show()

day_hist = px.histogram(time_df,x='Day')
day_hist.show()

hour_hist = px.histogram(time_df,x='Hour')
hour_hist.show()


# In[4]:


'''The above histograms demonstrate the tweeting habits of Donald Trump in 2019 with regard to month, 
day in a month, and hour in a day.
The first histogram shows that the number of tweets Trump posted in 2019 increased from January to December in 2019. 
Particularly, he tweeted least in February and most in December.

The second histogram shows that the number of tweets Trump posted in each month in 2019 was generally distributed evenly
throughout a month. However, Trump liked to tweet in the 11st day in a month.

The third histogram shows that Trump liked to tweet between 11:00 and 14:00. Trump was also vigorous that he also often tweeted
after 12 am and kept tweeting till 4 am. '''


# In[5]:


#This function is used to distill one item that appears most frequently in an array

def most_frequent(arr):
    max_count = 0;
    max_item = arr[0]
    for i in range(len(arr)):
        total_count = 1;
        for j in range(i+1,len(arr)):
            if(arr[i] == arr[j]):
                total_count +=1
        if(total_count > max_count):
            max_count = total_count
            max_item = arr[i]
    return max_item


# In[6]:


#This cell is used to distill tags from all words Trump has used in his original tweets

text = df['text']
all_sentences = []

retweet = list(df['retweet_count'])
favorite = list(df['favorite_count'])

#A list of all original tweets Trump has posted in 2019 (RT excluded)
original_tweets = []


for i in range(1,len(text)):
    
    sentences_in_this_tweet = []
    
    temp1 = text[i].replace('!','. ')
    temp2 = temp1.replace('?','. ')
    temp3 = temp2.replace('; ','. ')
    temp4 = temp3.replace(': ','. ')
    sentences = temp4.split('. ')
    for j in sentences:
        if(j[0:2]!='RT'):
            https_index = j.find('https:',0)
            if https_index!=(-1):
                all_sentences.append(j[0:https_index])
                sentences_in_this_tweet.append(j[0:https_index])
            else:
                all_sentences.append(j)
                sentences_in_this_tweet.append(j)
                this_original_tweet = []
                this_original_tweet.append(sentences_in_this_tweet)
                this_original_tweet.append(time[i])
                this_original_tweet.append(retweet[i])
                this_original_tweet.append(favorite[i])
    original_tweets.append(this_original_tweet)    
    
#Get tags each original tweet has used
for i in range(len(original_tweets)):
    tags = []
    for sentences in original_tweets[i][0]:
        for word in sentences.split(' '):
            if word != '' and word[0] == '#':
                tags.append(word)
    original_tweets[i].append(tags)

#Count the tags Trump liked to use
tags_dictionary = {}
for tweets in original_tweets:
    if len(tweets[4])!=0:
        for tag in tweets[4]:
            if tag in tags_dictionary.keys():
                tags_dictionary[tag] += 1
            else:
                tags_dictionary[tag] = 1
                
#Sort the tags_dictionary according to the count of tags
sorted_temp = sorted((value,key) for (key,value) in tags_dictionary.items())
sorted_temp.reverse()

#Plot all tags that Trump has used in 2019 in his original tweets and their corresponding frequency
sorted_tags = pd.DataFrame(sorted_temp,columns = ['counts','tags'])
print(sorted_tags)    
tags_counts = px.bar(sorted_tags,x='tags',y='counts')    
tags_counts.show()  

#print the top 20 tags Trump has used in 2019
top_ten_tags = px.bar(sorted_tags[0:19],x='tags',y='counts')  
top_ten_tags.show()


# In[7]:


'''The above bar charts show what hashtags Trump liked to use in 2019. Unexpectedly, Trump only used #MAGA for 72 times, 
which is a small amount compared to his original tweets.

According to the first bar chart, Trump tended to use different hashtags among his tweets because most of the hashtags
only appear once in his tweets. 

The second bar chart shows the top 20 most frequently used hashtags by Trump. Unsurprisingly, political campaign hashtags, 
including #MAGA, #KAG2020, #2020, and #KAG are used most frequently. Hashtags related to contemporary news
such as #Dorian and #USMCA were also used frequently. Trump also liked to use abbreviation in hashtags.'''


# In[8]:


#This function is used to calculate the average retweet, average favorite, and frequency of a tag in a specific month.

def adjust_this_month(this_month):
    total_month_retweet = 0
    total_month_favorite = 0
    total_month_count = 0
    for m in range(len(this_month)):
        if(len(this_month[m])==0):
            this_month[m].append([0,0,0])
        elif(len(this_month[m])==1):
            this_month[m][0].append(1)
        elif(len(this_month[m])>1):
            count = 0
            total_retweet = 0
            total_favorite = 0
            for n in this_month[m]:
                count+=1
                total_retweet+=n[0]
                total_favorite+=n[1]
            average_retweet = (total_retweet/count)
            average_favorite = (total_favorite/count)
            this_month[m].clear()
            this_month[m].append([average_retweet,average_favorite,count])
        total_month_retweet+=this_month[m][0][0]
        total_month_favorite+=this_month[m][0][1]
        total_month_count+=this_month[m][0][2]
    average_month_retweet = total_month_retweet/total_month_count
    average_month_favorite = total_month_favorite/total_month_count
    this_month.append(average_month_retweet)    
    this_month.append(average_month_favorite)    
    this_month.append(total_month_count)

#This function is used to sort the array by the value of the given element 
def insertionSort(arr,element): 
    temp = []
    for i in arr:
        temp.append(i)
    for i in range(1, len(temp)): 
  
        key = temp[i]
        j = i-1
        while j >=0 and key[element] > temp[j][element] : 
                temp[j+1] = temp[j] 
                j -= 1
        temp[j+1] = key 
    return temp


# In[9]:


from ipywidgets import interact, interactive, fixed, interact_manual

#Create a big list to store all tags-related information
tag_list = []
for items in sorted_temp:
    tag_list.append(list(items))

for i in range(len(sorted_tags)):
    this_tag = tag_list[i][1]
    
    total_retweet = 0;
    total_favorite = 0;
    retweet_list = []
    favorite_list = []
    month_list = []
    day_list = []
    hour_list = []
    
    all_months = []
    
    #The following loop will compile different information about a hashtag, including total retweet, total favorite,
    #month, day, and hour when the hashtag appears.
    
    for m in range(12):
        all_months.append([])
    for tweets in original_tweets:
        if len(tweets[4])!=0:
            for tag in tweets[4]:
                if tag == this_tag:
                    total_retweet += int(tweets[2])
                    total_favorite+= int(tweets[3])
                    retweet_list.append(int(tweets[2]))
                    favorite_list.append(int(tweets[3]))
                    month_list.append(tweets[1][0])
                    day_list.append(tweets[1][1])
                    hour_list.append(tweets[1][2])
                    break
                    
    this_month = []
    for m in range(31):
        this_month.append([])
        
    #The following while loop is used to distill information about a specific month for the given tag.
    
    loop_index = 0
    while loop_index < len(month_list):
        for j in range(loop_index,len(month_list)):
            if(month_list[j]!=month_list[loop_index]):
                adjust_this_month(this_month)
                
                temp = []
                for n in this_month:
                    temp.append(n)
                all_months[int(month_list[loop_index])-1] = temp.copy()
                this_month.clear()
                loop_index = j
                for m in range(31):
                    this_month.append([])
                break
            else:
                this_day = [retweet_list[j],favorite_list[j]]
                this_month[int(day_list[j])-1].append(this_day)
                
                if(j == len(month_list)-1):
                    adjust_this_month(this_month)
                    temp = []
                    for n in this_month:
                        temp.append(n)
                    all_months[int(month_list[loop_index])-1] = temp.copy()
                    loop_index=len(month_list)
    #Compile the information of the given hashtag in each month into an all_month list.
    
    for k in range(len(all_months)):
        if len(all_months[k])==0:
            for g in range(34):
                if g<=30:
                    all_months[k].append([[0,0,0]])
                else:
                    all_months[k].append(0)
                    
    #Calculate the average retweet and average favorite the hashtag gets 
    
    mean_retweet = total_retweet/tag_list[i][0]
    tag_list[i].append(mean_retweet)
    mean_favorite = total_favorite/tag_list[i][0]
    tag_list[i].append(mean_favorite)
    
    #Find the month, day, and hour when the hashtag is most frequently used
    
    month = most_frequent(month_list)
    day = most_frequent(day_list)
    hour = most_frequent(hour_list)
    tag_list[i].append(month)
    tag_list[i].append(day)
    tag_list[i].append(hour)
    tag_list[i].append(all_months)

tag_df = pd.DataFrame(tag_list,columns = ['Frequency','tag','mean_retweet','mean_favorite','Month','Day','Hour','Others'])

#Sort the hashtag list by number of retweet and favorite.
sort_by_retweet = insertionSort(tag_list,2)
sort_by_favorite = insertionSort(tag_list,3)
sort_by_retweet_df = pd.DataFrame(sort_by_retweet,columns = ['Frequency','tag','mean_retweet','mean_favorite','Month','Day','Hour','Others'])
sort_by_favorite_df = pd.DataFrame(sort_by_favorite,columns = ['Frequency','tag','mean_retweet','mean_favorite','Month','Day','Hour','Others'])

#Plot the ranking of hashtags according to their number of retweet and favorite

mean_retweet_plot = px.bar(sort_by_retweet_df,x='tag',y='mean_retweet')
mean_retweet_plot.show()
top_10_mean_retweet_plot = px.bar(sort_by_retweet_df[0:10],x='tag',y='mean_retweet')
top_10_mean_retweet_plot.show()

mean_favorite_plot = px.bar(sort_by_favorite_df,x='tag',y='mean_favorite')
mean_favorite_plot.show()
top_10_mean_favorite_plot = px.bar(sort_by_favorite_df[0:10],x='tag',y='mean_favorite')
top_10_mean_favorite_plot.show()


# In[10]:


'''
The first two bar charts show the ranking of hashtags by the number of retweet each hashtag gets and the top 10 retweeted tags. 
The second two bar charts show the ranking of hashtags by the number of favorite each hashtag gets and the top 10 favorite tags.
Although the most favorite hashtags are somewhat overlapping with the most retweeted hashtags,t
hey show that the distribution of retweet and favorite of hashtags show different patterns. For example, hashtags related to 
international politics got more retweets than favorite.

They also show that hashtags Trump liked to use are not hashtags people gave favorite and retweet to.
People were not too in favor of Trump's campaign slogans; rather, they liked to give favorite to hashtags related to
domestic polices and international politics. People also liked hashtags related to national events and holidays.

'''


# In[11]:


#Process the tag list data in order to summarize hashtags according to the month they are used

tag_for_month = []
for i in range(len(tag_list)):
    if(len(tag_list) <7):
        break
    tag_name = tag_list[i][1]
    for j in range(len(tag_list[i][7])):
        month_retweet = tag_list[i][7][j][31]
        month_favorite = tag_list[i][7][j][32]
        month_count = tag_list[i][7][j][33]
        tag_for_month.append([j+1,tag_name,month_retweet,month_favorite,month_count])
tag_month_df = pd.DataFrame(tag_for_month,columns = ['month','tag_name','month_retweet','month_favorite','month_count'])
print(tag_month_df)

#Plot the usage of different hashtags throughout the year in an animation

tag_over_year_fav = px.bar(tag_month_df[0:300],x='tag_name',y='month_count',animation_frame = 'month',color = 'month_favorite',range_y = [0,30])
tag_over_year_fav.show()
tag_over_year_ret = px.bar(tag_month_df[0:300],x='tag_name',y='month_count',animation_frame = 'month',color = 'month_retweet',range_y = [0,30])
tag_over_year_ret.show()


# In[12]:


'''
The above animated bar charts show the frequency of most frequently used hashtags in each month in 2019.
The color of the bars show the favorite each hastag gets in each month in 2019.
They show that Trump used few hashtags before June and most of hashtags he used were campaign slogans. After June, he started to
use various hashtags. In addition, Trump used #Dorian most in Semptember and October to discuss the hurricane and used USMAC 
more in December because of the negotiation. Trump seemed indifferent to the impeachment in November as he didn't tweet much
with this tag.

Although Trump used more hashtags after June, he received less favorite and retweet after June.

'''


# In[13]:


from ipywidgets import interact, interactive, fixed, interact_manual

#This function is used to get the average retweet, favorite, and frequency of a given hashtag in a given month
def specific_month(tag,m):
    specific_month = []
    for i in range(31):
        specific_month.append([i+1,tag[7][m-1][i][0][0],tag[7][m-1][i][0][1],tag[7][m-1][i][0][2]])
    specific_month_df = pd.DataFrame(specific_month,columns = ['Day','Average_Retweet','Average_Favorite','Total_count'])
    specific_month_retweet = px.bar(specific_month_df,x='Day',y='Total_count',color='Average_Retweet')
    specific_month_favorite = px.bar(specific_month_df,x='Day',y='Total_count',color='Average_Favorite')
    specific_month_retweet.update_layout(
    title_text = 'Average_retweet and the frequency of this tag in this month.'
    )
    specific_month_favorite.update_layout(
    title_text = 'Average favorite and the frequency of this tag in this month.'
    )
    specific_month_favorite.show()  
    specific_month_retweet.show()    

#This function is used to get the detailed information of a given tag, including the total frequency in 2019,
#the average retweet in 2019, the average favorite in 2019, the date it was usually used, the time it was usually posted,
#the retweet, favorite, and frequency of the given tag in a given month

def tag_info(list_tag,tag_name):
    if tag_name == ' ':
        print('Invalid Input! Default tag will be displayed.')
        tag_name = '#MAGA'
    this_tag_list = []
    for tag in list_tag:
        if tag[1] == tag_name:
            this_tag_list = tag
            break
            
    #Get the basic information about this given tag throughout the year
    print('The tag {} appears in Trump twitters in 2019 for {} time(s).'.format(this_tag_list[1],this_tag_list[0]))
    print('Twitters with this tag have an average retweet of ',this_tag_list[2])
    print('Twitters with this tag have an average favorite of ',this_tag_list[3])
    print('This tag often appears on the date of {}-{}'.format(this_tag_list[4],this_tag_list[5]))
    print('This tag often appears at the time of {}:00'.format(this_tag_list[6]))
    month = []
    for i in range(len(this_tag_list[7])):
        month.append([i+1,this_tag_list[7][i][31],this_tag_list[7][i][32],this_tag_list[7][i][33]])
    month_df = pd.DataFrame(month,columns = ['Month','Average_Retweet','Average_Favorite','Total_count'])
    month_overall_favorite = px.bar(month_df,x='Month',y='Total_count',color = 'Average_Favorite')
    month_overall_retweet = px.bar(month_df,x='Month',y='Total_count',color='Average_Retweet')
    month_overall_retweet.update_layout(
    title_text = 'Average retweet and the frequency of this tag throughout the year.'
    )
    month_overall_favorite.update_layout(
    title_text = 'Average favorite and the frequency of this tag throughout the year.'
    )
    month_overall_favorite.show()
    month_overall_retweet.show()
    print('Drag the tab to display the detailed information about this tag in a given month!')
    interact(specific_month,tag = fixed(this_tag_list),m = (1,12))
    
print('The following is the top 10 tags Trump used most in 2019. Search for any tag to get more information about how Trump used it and how the audience reacted to it!')
print(sorted_tags[0:9])

interact(tag_info,list_tag = fixed(tag_list),tag_name = ['#MAGA','#Dorian','#USMCA','#KAG2020','#2020','#1','#impeachment','KAG','KeepAmericaGreat'])


# In[ ]:





# In[ ]:





# In[ ]:




