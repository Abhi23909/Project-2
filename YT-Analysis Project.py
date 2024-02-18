#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns


# In[ ]:


pip install --upgrade google-api-python-client


# In[ ]:


api_key ='AIzaSyC1S5h34y_usF9e1bY-a708sgK_qCxh1kA'
channel_ids=['UCmi3mz9bvyPnnXEmROrYnRw',
             'UC8tjqXag737a3B9dHd_nU2w',
             'UCMIFfKxfDFWmioZ_Gl6GZrg'
            ]
youtube= build('youtube', 'v3', developerKey=api_key)


# In[ ]:


def get_channel_stats(youtube, channel_ids):
    all_data=[]
    request = youtube.channels().list(
        part='snippet, contentDetails, statistics',
        id=','.join(channel_ids))
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(Channel_name=response['items'][i]['snippet']['title'],
                    Subscribers =response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'], 
                    Total_videos=response['items'][i]['statistics']['videoCount'],
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    
    return all_data


# In[ ]:


channel_statistics=get_channel_stats(youtube, channel_ids)


# In[ ]:


channel_data = pd.DataFrame(channel_statistics)


# In[ ]:


channel_data


# In[ ]:


playlist_id = channel_data.loc[channel_data['Channel_name']=='DJ Rash Official','playlist_id'].iloc[0]


# In[ ]:


playlist_id


# In[ ]:


channel_data['Subscribers']= pd.to_numeric(channel_data['Subscribers'])
channel_data['Views']= pd.to_numeric(channel_data['Views'])
channel_data['Total_videos']= pd.to_numeric(channel_data['Total_videos'])
channel_data.dtypes


# In[ ]:


sns.set(rc={'figure.figsize':(10,8)})
ax = sns.barplot(x='Channel_name', y='Subscribers', data=channel_data)


# In[ ]:


ax = sns.barplot(x='Channel_name', y='Views', data=channel_data)


# In[ ]:


ax = sns.barplot(x='Channel_name', y='Total_videos', data=channel_data)


# In[ ]:





# In[ ]:


def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50)
    response = request.execute()
    
    video_ids = []
    
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                      part='contentDetails',
                      playlistId=playlist_id,
                      maxResults=50,
                      pageToken=next_page_token)
            response = request.execute()
            
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
        
    return video_ids


# In[ ]:


video_ids=get_video_ids(youtube, playlist_id)


# In[ ]:


video_ids


# In[176]:


def get_video_details(youtube, video_ids):
    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id= ','.join(video_ids[i:i+50])
        )
        response = request.execute()
        for video in response['items']:
            video_stats=dict(Title=video['snippet']['title'],
                             Published_date=video['snippet']['publishedAt'],    
                             Views=video['statistics']['viewCount'],
                             Likes=video['statistics']['likeCount'],
                             Comments=video['statistics']['commentCount']
                            )
            all_video_stats.append(video_stats)
   
    return all_video_stats


# In[179]:


video_details=get_video_details(youtube, video_ids)


# In[180]:


video_data=pd.DataFrame(video_details)


# In[181]:


video_data['Published_date'] = pd.to_dateframe(video_date['Published_date']).dt.date
video_data['Views'] =pd.to_numeric(video_data['Views'])
video_data['Likes'] =pd.to_numeric(video_data['Likes'])
video_data['Comments'] =pd.to_numeric(video_data['Comments'])
video_data['Views'] =pd.to_numeric(video_data['Views'])
video_data


# In[185]:


top10_videos = video_data.sort_values(by='Views',ascending=False).head(10)


# In[186]:


top10_videos


# In[189]:


top10_videos['Views'] = top10_videos['Views'].astype(int)
ax1 = sns.barplot(x='Views', y='Title', data=top10_videos)


# In[190]:


video_data


# In[193]:


video_data['Month']=pd.to_datetime(video_data['Published_date']).dt.strftime('%b')


# In[195]:


video_data


# In[196]:


videos_per_month = video_data.groupby('Month', as_index=False).size()


# In[197]:


videos_per_month


# In[202]:


sort_order =['Jan','Feb','Mar','Apr','May','Jun',
             'Jul','Aug','Sept','Oct','Nov','Dec']


# In[206]:


videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories=sort_order, ordered=True)


# In[207]:


videos_per_month=videos_per_month.sort_index()


# In[208]:


ax2= sns.barplot(x='Month',y='size',data=videos_per_month)


# In[ ]:




