import os

import dotenv
import requests
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

v = '5.130'

dotenv.load_dotenv()

vk_token = settings.VK_TOKEN
vk_api_url = "https://api.vk.com/method/"

tg_token = settings.TG_TOKEN
tg_api_url = f"https://api.telegram.org/bot{tg_token}/"


class VkMethods:
    __slots__ = '_method'

    def __init__(self, method='') -> None:
        self._method = method

    def __getattr__(self, method: str) -> object:
        return VkMethods(method=method if self._method == '' else f'{self._method}.{method}')

    def __call__(self, **kwargs) -> dict:
        """
        :param method: Метод выполняемый в вк апи
        :param kwargs: Аргументы для этого метода
        :return: https://vk.com/dev/methods
        """
        kwargs.update({"v": v, "access_token": vk_token})
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=Retry(connect=2, backoff_factor=0.5))
        session.mount("https://", adapter)
        if self._method == "messages.send":
            kwargs["random_id"] = 0
            if len(kwargs['message']) > 3500:
                first_message = kwargs['message'][:len(kwargs['message']) // 2]
                second_message = kwargs['message'][len(kwargs['message']) // 2:]
                kwargs['message'] = first_message
                session.get(vk_api_url + self._method, params=kwargs)
                kwargs['message'] = second_message
                rw = session.get(vk_api_url + self._method, params=kwargs)
                return rw.json()
        rw = session.get(vk_api_url + self._method, params=kwargs)
        try:
            if rw.json().get('error'):
                print(rw.json())
                match rw.json()["error"]["error_code"]:
                    case 15 | 901 | 7 | 10 | 100:
                        ...
                    case _:
                        print('error:', rw.json())
        except Exception as e:
            print(e)
        return rw.json()


class TgMethods:
    def __init__(self, method=None) -> None:
        self._method = method

    def __getattr__(self, method: str):
        return TgMethods(method=method)

    def __call__(self, *args, **kwargs):

        if self._method == "sendMessage":
            if len(kwargs["text"]) > 3500:
                first_message = kwargs['text'][:len(kwargs['text']) // 2]
                second_message = kwargs['text'][len(kwargs['text']) // 2:]
                kwargs['text'] = first_message
                requests.get(tg_api_url + self._method, params=kwargs)
                kwargs['text'] = second_message
                rw = requests.get(tg_api_url + self._method, params=kwargs)
                return rw.json()

        return requests.get(tg_api_url + self._method, params=kwargs).json()
