# type: ignore
from __future__ import annotations
from typing import Dict, Any
import random
import string
import requests
from os import getenv

USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")


class AttendeceTools:
    def __init__(self) -> None:
        self.token: str = ''

    def __post_init__(self) -> None:
        pass

    def update_tok(self) -> None:
        print('entered\n')
        rand_str: str = ''.join(random.choices(string.ascii_lowercase, k=3))
        sess_token: str = f"ggpmgfj8dssskkp2q2h6db{rand_str}0"
        url: str = "http://103.203.175.90:94/attendance/attendanceLogin.php"
        headers: Dict[str, str] = {
            "Cache-Control": "max-age=0",
            "Origin": "http://103.203.175.90:94",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Sec-GPC": "1",
            "Accept-Language": "en-US,en",
            "Referer": "http://103.203.175.90:94/attendance/attendanceLogin.php",
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": f"PHPSESSID={sess_token}",
            "Connection": "keep-alive"
        }

        payload: str = f'username={USERNAME}&password={PASSWORD}&captcha='

        response: requests.Response = requests.post(url, headers=headers,
                                                    data=payload, allow_redirects=False)

        self.token = sess_token


class DataStore:
    def __init__(self):
        self.sections = {
            "cse": {"a": "", "b": "", "c": "", "d": ""},
            "aids": {"a": "", "b": ""},
            "mech": {"a": ""},
            "ece": {"a": "", "b": "", "c": "", "d": ""},
            "eee": {"a": "", "b": ""},
            "civ": {"-": ""},
            "it": {"-": ""},
            "cse_ds": {"-": ""},
            "cse_aiml": {"-": ""},
        }
        self.branches = {
            "5": "CSE",
            "23": "AIDS",
            "7": "MECH",
            "4": "ECE",
            "2": "EEE",
            "11": "CIV",
            "22": "IT",
            "32": "CSE_DS",
            "33": "CSE_AIML",
        }
