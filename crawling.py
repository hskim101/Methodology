import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import requests
import json

def set_video(channelId, maxCount):  
  	#먼저 search 함수를 통해 해당 channelId의 조회 수(viewCount)가 높은 영상을 파라미터로 받아 준 maxCount만큼 조회한다.
    # search_response = youtube.search().list(
    #     order = 'viewCount',
    #     part = 'snippet',
    #     channelId = channelId,
    #     maxResults = maxCount,
    # ).execute()
    
    search_response = youtube.search().list(
        order = 'viewCount',
        part = 'snippet',
        q = channelId,
        maxResults = maxCount,
    ).execute()
    
    
    video_ids = []
    for i in range(len(search_response['items'])):
        video_ids.append((search_response['items'][i]['id']['videoId'])) #videoId의 리스트를 만들어 둔다 (videoId로 조회할 수 있게)
  
  	#추출할 정보의 list들과 그 모든 정보를 key-value로 저장할 딕셔너리 변수를 하나 생성한다.
    channel_video_id = []
    channel_video_title = []
    channel_rating_view = []
    channel_rating_comments = []
    channel_rating_good = []
    channel_published_date = []
    channel_description = []
    data_dicts = { }
    
    # 영상이름, 조회수 , 좋아요수 등 정보 등 추출
    for k in range(len(search_response['items'])):
        video_ids_lists = youtube.videos().list(
            part='snippet, statistics',
            id=video_ids[k],
        ).execute()
        
        #print(video_ids_lists)
    
        str_video_id = video_ids_lists['items'][0]['id']
        str_video_title = video_ids_lists['items'][0]['snippet'].get('title')
        str_view_count = video_ids_lists['items'][0]['statistics'].get('viewCount')
        if str_view_count is None:
            str_view_count = "0"
        str_comment_count = video_ids_lists['items'][0]['statistics']['commentCount']
        if str_comment_count is None:
            str_comment_count = "0"
        str_like_count = video_ids_lists['items'][0]['statistics'].get('likeCount')
        if str_like_count is None:
            str_like_count = "0"
        str_published_date = str(video_ids_lists['items'][0]['snippet'].get('publishedAt'))
        str_description = video_ids_lists['items'][0]['snippet'].get('description')

        # 비디오 ID 
        channel_video_id.append(str_video_id)
        # 비디오 제목 
        channel_video_title.append(str_video_title)
        # 조회수 
        channel_rating_view.append(str_view_count)
        # 댓글수 
        channel_rating_comments.append(str_comment_count)
        # 좋아요 
        channel_rating_good.append(str_like_count)
        # 게시일 
        channel_published_date.append(str_published_date)
        # 설명
        channel_description.append(str_description)

    data_dicts['id'] = channel_video_id
    data_dicts['title'] = channel_video_title
    data_dicts['viewCount'] = channel_rating_view
    data_dicts['commentCount'] = channel_rating_comments
    data_dicts['likeCount'] = channel_rating_good
    data_dicts['publishedDate'] = channel_published_date
    data_dicts['description'] = channel_description
    
    return data_dicts     
# YouTube Data API 인증 정보
# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# 인증 흐름 시작
API_KEY = 'AIzaSyDbi2_9deOsHM6XkA4zGLKoV4o9_fWKWxs'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_SERVICE_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_SERVICE_VERSION, developerKey = API_KEY)
youtuber = set_video('UCg-p3lQIqmhh7gHpyaOmOiQ',  50) 


with open('./englishman.json','w') as f:
    json.dump(youtuber, f, indent=4, ensure_ascii=False)
