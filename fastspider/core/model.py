import datetime
import json
from typing import Dict

from requests.cookies import cookiejar_from_dict

from fastspider.core.utils import compact_json_dumps
import hashlib

class Request:
    def __init__(self, url: str, method: str, cookies: Dict = None, headers: Dict = None, body=None, proxy=None,
                 meta=None):
        """
        :param url: The request url
        :param method: HTTP method
        :param headers: dictionary of headers
        :param body: HTTP message body
        """
        self.url: str = url
        self.method: str = method  # 'GET','HEAD', 'POST', 'PUT','DELETE','OPTIONS', 'PATCH', etc
        self.cookies = cookies
        self.headers = headers  # 'Accept-Encoding', 'Accept','Content-Length','User-Agent', etc
        self.body = body
        self.proxy = proxy
        self.meta = meta

    def serialize(self):
        if not self.method:
            raise
        d = {
            'url': self.url,
            'method': self.method.upper(),
            'cookies': self.cookies,
            'headers': self.headers,
            'proxy': self.proxy,
            'meta': self.meta,
        }
        return compact_json_dumps(d)

    def deserialize(self,data:str):
        dic = json.loads(data)


class Response:
    def __init__(self):
        self.url = None
        self.status_code = None
        self.headers = {}
        self.history = []
        self.reason = None

        self.cookies = cookiejar_from_dict({})
        self.request = None
        self.elapsed = datetime.timedelta(0)
        self.encoding = None

    def __repr__(self):
        return f'<Response [{self.url}][{self.status_code}]>'


class Task:
    def __init__(self):
        self._request: Request = None
        self._response: Response = None

    def task_id(self):
        if not self._request:
            raise Exception("Should set request first")
        return hashlib.md5(self._request.url.encode())

    def set_request(self,request:Request):
        self._request = request


    def set_response(self,response:Response):
        self._response = response