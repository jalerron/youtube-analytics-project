import json
import os

from googleapiclient.discovery import build

API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    @classmethod
    def get_service(cls):
        """
        Создает объект для работы с YouTube API
        """
        service = build('youtube', 'v3', developerKey=API_KEY)
        return service

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        self.request = self.get_service().channels().list(
            id=self.__channel_id, part='snippet,contentDetails,statistics').execute()

        self.title = self.request['items'][0]['snippet']['title']
        self.description = self.request['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{channel_id}'
        self.subscriber_count = int(self.request['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.request['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.request['items'][0]['statistics']['viewCount'])

    @property
    def channel_id(self):
        return self.__channel_id

    def __str__(self):
        """
        Читабельный вывод класса
        """
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """
        Метод сложения для подписчиков каналов
        """
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """
        Разница между подписчиками каналов
        """
        return self.subscriber_count - other.subscriber_count

    def __eq__(self, other):
        """
        Равенство кол-ва подписчиков каналов
        """
        return self.subscriber_count == other.subscriber_count

    def __ne__(self, other):
        """
        Неравенство кол-ва подписчиков каналов
        """
        return self.subscriber_count != other.subscriber_count

    def __lt__(self, other):
        """
        Оператор меньше для подписчиков каналов
        """
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """
        Оператор меньше или равно для подписчиков каналов
        """
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        """
        Оператор больше для подписчиков каналов
        """
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """
        Оператор больше или равно для подписчиков каналов
        """
        return self.subscriber_count >= other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        # api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,contentDetails,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    # def get_channel_info(self) -> None:
    #     request = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
    #     title = request['items'][0]['snippet']['title']
    #     description = request['items'][0]['snippet']['description']
    #     customUrl = request['items'][0]['snippet']['customUrl']
    #     print(description)
    #     print(customUrl)

    def to_json(self, filename: str):
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

# moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
# print(moscowpython.title)
