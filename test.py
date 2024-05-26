import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import requests
import json

import pandas as pd



def get_youtube_vedio_search_list(channelID, max_data_num, keyword):   
    df = pd.DataFrame(columns = ['video_id', 'title', 'rating_view', 'rating_comments', 'rating_good', 'published_date', 'description'])
    # start_time='2024-06-01T00:00:00Z'
    start_time='2023-04-01T00:00:00Z'
    page_token = ''
    part = 8
    while(len(df)<max_data_num):
    	##API 호출	
        # search_response = youtube.search().list(
        #     maxResults = 50,       #한 번에 가져오는 데이터 수
        #     part = 'snippet',   
        #     channelId = channelID,		
        #     pageToken = page_token,
        #     publishedBefore = start_time,
        #     publishedAfter = calculate_next_publish_time(start_time)
        # ).execute()
        search_response = youtube.search().list(
            maxResults = 50,       #한 번에 가져오는 데이터 수
            part = 'snippet',   
            q = keyword,
            order='relevance',		
            pageToken = page_token,
            publishedBefore = start_time,
            publishedAfter = calculate_next_publish_time(start_time)
        ).execute()
        # print(keyword)
        ##불러온 데이터 저장
        for item in search_response['items']:
            new_data = {'video_id':'not-yet', 'title':'not-yet', 'rating_view':-1, 'rating_comments':-1, 'rating_good':-1, 'published_date':'not-yet', 'description':'not-yet'}
            if 'videoId' in item['id'].keys():
                new_data['video_id'] = item['id']['videoId']
            new_data['title'] = item['snippet']['title']
            new_data['published_date'] = item['snippet']['publishTime']
            new_data['description'] = item['snippet']['description']
            df.loc[len(df)] = new_data

        for index in range(len(df)):
        #API로 정보 불러오기
            response = youtube.videos().list(
                part = 'statistics',
                id = df.loc[index, 'video_id']  #앞서 수집한 video_id
            ).execute()
            #불러온 결과에 조회수 정보가 있는지 확인하고
            #있으면 해당 내용을, 없으면 -2를 넣는다.
            if (response['pageInfo']['totalResults'] > 0):
                if('viewCount' in response['items'][0]['statistics']):
                    df.loc[index, 'rating_view'] = response['items'][0]['statistics']['viewCount']
                if('commentCount' in response['items'][0]['statistics']):
                    df.loc[index, 'rating_comments'] = response['items'][0]['statistics']['commentCount']
                if('likeCount' in response['items'][0]['statistics']):
                    df.loc[index, 'rating_good'] = response['items'][0]['statistics']['likeCount']
                    
            else:
                df.loc[index, 'rating_view'] = -2
                df.loc[index, 'rating_comments'] = -2
                df.loc[index, 'rating_good'] = -2
    

            
            ###다음 페이지 토큰 찾기
        if ('nextPageToken' in search_response):
            print('nextPage')
            page_token = search_response['nextPageToken']
            
        else:
            print('count : ', len(df))
            start_time = calculate_next_publish_time(start_time)
            page_token=''
            df.to_csv("/home/lafesta/Desktop/Methodology/dataset/spicynoodle/" + f'{keyword}'+ f'{part}'+".csv", header=True, index=False)
            part+=1
            df = pd.DataFrame(columns = ['video_id', 'title', 'rating_view', 'rating_comments', 'rating_good', 'published_date', 'description'])


    return df

def calculate_next_publish_time(time):
    if(time[5:7]=='01'):
        return '%04d-12-01T00:00:00Z'%(int(time[:4])-1)
    else:
        return time[:5]+'%02d-01T00:00:00Z'%(int(time[5:7])-1)

# AIzaSyDBDXT_GeVoS-cMwuYm-DdxMI4GdQy1DUE

API_KEY = 'AIzaSyDBDXT_GeVoS-cMwuYm-DdxMI4GdQy1DUE'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_SERVICE_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_SERVICE_VERSION, developerKey = API_KEY)
keywords = ['불닭', '불닭 챌린지', 'fire noodle challenge', 'fire noodle', 'korean spicy noodle', '불닭볶음면', '핵붉닭', 'nuclear fire noodle', 'noodle challenge']
youtuber = get_youtube_vedio_search_list('UCg-p3lQIqmhh7gHpyaOmOiQ', 10000, '불닭') 
