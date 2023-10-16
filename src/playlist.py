import datetime
import isodate

from src.channel import APIMixin


# answer = APIMixin.get_service().playlistItems().list(playlistId='PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC',
#                                                      part='snippet').execute()
#
# print(answer)

class PlayList(APIMixin):

    def __init__(self, playlist_id: str) -> None:
        """
        Инициализация класса вместе с классом миксином из класса chanel
        """
        self.__playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'
        super().get_service()
        self.playlist = PlayList.get_service().playlists().list(id=self.__playlist_id, part='snippet', ).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                           part='snippet, contentDetails',
                                                                           maxResults=50, ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

    @property
    def playlist_id(self):
        return self.__playlist_id

    @property
    def total_duration(self):
        """
        Метод показывающий продолжительность видео
        """
        add_time = datetime.timedelta(minutes=0)
        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(self.video_ids)).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            add_time += duration

        return add_time

    def show_best_video(self):
        """
        Метод возвращающий лучший ролик по лайкам
        """
        like: int = 0
        for video_id in self.video_ids:
            video_response = PlayList.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                  id=video_id).execute()
            like_count: int = int(video_response['items'][0]['statistics']['likeCount'])

            if like < like_count:
                url_video = f'https://youtu.be/{video_id}'
                like = like_count

        return url_video
