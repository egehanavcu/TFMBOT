# TFMBot

TFMBot is a bot written in Python in order to make the socket connection between TFM server and Python client. It allows you to send messages with TCP connection.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TFMBot.

```bash
pip install pysocks
pip install asyncio
pip install aiohttp
```

## Config Details
* Split the string, using comma, followed by a space, if you want to use more than one account. For example:
```bash
usernames = User1, User2, User3
```

* If you specify multiple accounts, you will only be able to use one password. All accounts' passwords must be same.
* Proxy needs to be set as false if not used.
