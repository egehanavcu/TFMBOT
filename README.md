# TFMBot

TFMBot is a Python-based bot designed to establish a socket connection between the TFM server and Python client. It enables users to send messages via TCP connection.

## Installation

To install TFMBot, use the package manager pip, which can be found at https://pip.pypa.io/en/stable/.

```
pip install pysocks
pip install asyncio
pip install aiohttp
```

## Configuration Details
* To connect to the game, you need to have an API key.
* If you want to use more than one account, separate the usernames with a comma followed by a space. For example: `usernames = User1, User2, User3`. **Note that if you specify multiple accounts, you will only be able to use one password, which must be the same for all accounts.**
* If you are not using a proxy, set it to false.
