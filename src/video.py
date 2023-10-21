from googleapiclient.discovery import build

import os

API_KEY = os.getenv('YT_API_KEY')
service = build('youtube', 'v3', developerKey=API_KEY)


class Video:
    """
    Класс для видео
    """

    def __init__(self, id_video: str):
        """
        Инициализация класса Видео
        """
        try:
            self.id_video = id_video
            self.url_video = f'https://www.youtube.com/watch?v={id_video}'
            response = service.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                         id=id_video).execute()
            self.video_title = response['items'][0]['snippet']['title']
            self.count_view = response['items'][0]['statistics']['viewCount']
            self.like_counts = response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.__video_id = None
            self.video_url = None
            self.video_title = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    """
    Класс для плейлиста
    """

    def __init__(self, id_video, id_playlist):
        """
        Инициализация для класса плейлиста
        """
        super().__init__(id_video)
        self.id_playlist = id_playlist
