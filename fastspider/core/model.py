import base64
import hashlib
import json
from typing import Dict

import chardet

from fastspider.core.utils import compact_json_dumps


class Request:
    def __init__(self, url: str, method: str, cookies: Dict = None, headers: Dict = None, body=None, proxy=None,
                 meta: Dict = None):
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
        self.meta = meta or {}

    def serialize(self):
        if not self.method:
            raise
        d = {
            'url': self.url,
            'method': self.method.upper(),
            'cookies': self.cookies,
            'body': self.body,
            'headers': self.headers,
            'proxy': self.proxy,
            'meta': self.meta,
        }
        return compact_json_dumps(d)

    @classmethod
    def deserialize(cls, data: str):
        dic = json.loads(data)
        url = dic['url']
        method = dic['method']
        cookies = dic['cookies']
        headers = dic['headers']
        body = dic['body']
        proxy = dic['proxy']
        meta = dic.get('meta')
        return cls(url, method, cookies, headers, body=body, proxy=proxy, meta=meta)


class Response:
    def __init__(self, url: str, status_code: int, content: bytes = None, headers: Dict = None, cookies: Dict = None,
                 history: list = None, reason: str = None):
        self.url = url
        self.status_code = status_code
        self.content: bytes = content
        self.headers = headers or {}
        self.history = history or []
        self.reason = reason
        self.cookies = cookies
        self.elapsed = None

    def __repr__(self):
        return f'<Response [{self.url}][{self.status_code}]>'

    def serialize(self):
        if self.content:
            content = base64.b64encode(self.content)
            content = content.decode()
        else:
            content = None
        d = {
            'url': self.url,
            'status_code': self.status_code,
            'content': content,
            'cookies': self.cookies,
            'headers': dict(self.headers),
            'history': self.history,
        }
        return compact_json_dumps(d)

    @classmethod
    def deserialize(cls, data: str):
        dic = json.loads(data)
        url = dic['url']
        status_code = dic['status_code']
        content = dic['content']
        if content:
            content = base64.b64decode(content.encode())
        cookies = dic['cookies']
        headers = dic['headers']
        history = dic.get('history')

        return cls(url, status_code, content, cookies, headers, history)

    def text(self, encoding='utf8', use_chardet=False, errors='replace'):
        """

        :param encoding:
        :param use_chardet: Use chardet to auto detect the encoding of content
        :param errors: two mode: replace or strict
        :return:
        """
        if use_chardet:
            encoding = chardet.detect(self.content)['encoding']
        return self.content.decode(encoding, errors=errors)


class Task:
    def __init__(self):
        self._request: Request = None
        self._response: Response = None

    def task_id(self):
        if not self._request:
            raise Exception("Should set request first")
        return hashlib.md5(self._request.url.encode())

    def set_request(self, request: Request):
        self._request = request

    def set_response(self, response: Response):
        self._response = response
