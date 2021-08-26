from json import dumps
from . import errors
import requests
from requests.auth import HTTPBasicAuth

from python_iugu.client.iclient import IClient
from python_iugu.utils import to_dict
from python_iugu.version import __version__
from typing import Dict, Any, Generic, TypeVar
import os

T = TypeVar("T")


class _Client(IClient):
    _URL = "https://api.iugu.com/v1"

    def __init__(self, token: str) -> None:
        self._token = token

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str) -> None:
        """
        it allows to change the token in runtime.
        Ex.: (prod to test)
        :param token:
        :return:
        """
        self._token = token

    @staticmethod
    def headers() -> Dict[str, str]:
        return {
            "User-Agent": "Async Iugu Python Api %s" % __version__,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def __validation(self, response, msg=None):
        """
        Validates if data returned by API contains errors json. The API returns
        by default a json with errors as field {errors: XXX}

            => http://iugu.com/referencias/api#erros
        """

        results = response

        try:
            err = results["errors"]
        except:
            err = None

        if err:
            raise errors.IuguGeneralException(value=err)
        else:
            return results

    def __reload_conn(self):
        """
        Wrapper to keep TCP connection ESTABLISHED. Rather the connection go to
        CLOSE_WAIT and raise errors CannotSendRequest or the server reply with
        empty and it raise BadStatusLine
        """
        self.__conn = HTTPSConnection(config.API_HOSTNAME)  # reload
        self.__conn.timeout = 10

    def __request(self, method: str, suffix: str, obj: Generic[T]) -> Dict[str, Any]:

        url = f"{self._URL}/{suffix}"
        headers = self.headers()

        body = dumps(to_dict(obj))

        response = requests.request(
            method=method,
            url=url,
            data=body,
            headers=headers,
            auth=HTTPBasicAuth(username=self.token, password=""),
        )

        return response.json()

    def get(self, suffix: str, obj: Generic[T] = None) -> Dict[str, Any]:
        response = self.__request("GET", suffix, obj)
        return self.__validation(response)

    def post(self, suffix: str, obj: Generic[T] = None) -> Dict[str, Any]:
        response = self.__request("POST", suffix, obj)
        return self.__validation(response)

    def put(self, suffix: str, obj: Generic[T] = None) -> Dict[str, Any]:
        response = self.__request("PUT", suffix, obj)
        return self.__validation(response)

    def delete(self, suffix: str, obj: Generic[T] = None) -> Dict[str, Any]:
        response = self.__request("DELETE", suffix, obj)
        return self.__validation(response)


__default_api__ = None


def default_api():
    global __default_api__
    if __default_api__ is None:
        try:
            token = os.environ["IUGU_API_TOKEN"]
        except KeyError:
            raise NotImplementedError
        __default_api__ = _Client(token=token)
    return __default_api__


def config(token: str):
    global __default_api__
    __default_api__ = _Client(token)
    return __default_api__
