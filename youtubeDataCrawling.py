import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from tqdm import tqdm

API_KEY = "AIzaSyDyYNe8iFLOG2ZApQt9e4OiNgcF-bnzXRU"
YOUTUBE_SERVICE_NAME = "youtube"
YOUTUBE_VERSION = "v3"

youtube = build(YOUTUBE_SERVICE_NAME, YOUTUBE_VERSION,
                developerKey=API_KEY)

#채널 id를 통하여 upload태그에 접근 / playlist_id를 얻어옴
res = youtube.channels().list(id='UCDqaUIUSJP5EVMEI178Zfag',
                              part='contentDetails').execute()
playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

#video를 담을 리스트 생성
videos = []

#채널의 모든 동영상을 얻어와야 하므로 page_token을 이용
next_page_token = None


res = youtube.playlistItems().list(playlistId=playlist_id,
                                       part='snippet').execute()
#채널의 전체 동영상수
max_size = res['pageInfo']['totalResults']

DEBUG = False
#로딩바를 보여주기 위하여 tqdm 라이브러리 사용
if DEBUG :
    pbar = tqdm(total=max_size, desc = 'youtube로부터 data를 받고 있습니다')

#모든 동영상을 받을때 까지 반복문 실행
while DEBUG : 
    res = youtube.playlistItems().list(playlistId=playlist_id,
                                       part='snippet',
                                       maxResults=50,
                                       pageToken=next_page_token).execute()
    
    #videos리스트에 item 저장
    videos += res['items']

    #로딩바 update
    pbar.update(50)

    #다음 페이지가 없으면 반복문 중단
    next_page_token = res.get('nextPageToken')
    if next_page_token is None:
        break
    


res = youtube.playlistItems().list(playlistId=playlist_id,
                                       part='snippet',
                                       maxResults=5,
                                       pageToken=next_page_token).execute()
        
videos += res['items']
i = 0
for video in videos:
    i += 1
    print(video['snippet']['title'] + " " +str(i))


