from socket import socket
from urllib.request import Request, urlopen
from urllib.parse import quote
import socks
import threading
import time
import random
import base64
import hashlib
import ctypes
import configparser
import sys
import re
import codecs
import asyncio
import aiohttp
import struct

class ByteArray:
    def __init__(self, b=b''):
        self.position = 0
        self.bytes = b

    def writeByte(self, value):
        self.bytes += struct.pack('!b', int(value))
        return self

    def writeUnsignedByte(self, value):
        self.bytes += struct.pack('!B', int(value))
        return self

    def writeShort(self, value):
        self.bytes += struct.pack('!h', int(value))
        return self

    def writeUnsignedShort(self, value):
        self.bytes += struct.pack('!H', int(value))
        return self

    def writeInt(self, value):
        self.bytes += struct.pack('!i', int(value))
        return self

    def writeUnsignedInt(self, value):
        self.bytes += struct.pack('!I', int(value))
        return self

    def writeBool(self, value):
        self.bytes += struct.pack('!?', int(value))
        return self

    def writeUTF(self, value):
        size = len(value.encode())
        self.writeShort(size)
        self.write(value.encode())
        return self

    def writeUTFBytes(self, value, size):
        valueData = str(struct.pack('!b', 0)) * int(size)
        for data in valueData:
            if len(value) < int(size):
                value = value + struct.pack('!b', 0)

        self.write(value)
        return self

    def writeBytes(self, value):
        self.bytes += value
        return self

    def write(self, value):
        self.bytes += value

    def readByte(self):
        value = struct.unpack('!b', self.bytes[self.position:self.position + 1])[0]
        self.position += 1
        return value

    def readUnsignedByte(self):
        value = struct.unpack('!B', self.bytes[self.position:self.position + 1])[0]
        self.position += 1
        return value

    def readShort(self):
        value = struct.unpack('!h', self.bytes[self.position:self.position + 2])[0]
        self.position += 2
        return value

    def readUnsignedShort(self):
        value = struct.unpack('!H', self.bytes[self.position:self.position + 2])[0]
        self.position += 2
        return value

    def readInt(self):
        value = struct.unpack('!i', self.bytes[self.position:self.position + 4])[0]
        self.position += 4
        return value

    def readUnsignedInt(self):
        value = struct.unpack('!I', self.bytes[self.position:self.position + 4])[0]
        self.position += 4
        return value

    def readUTF(self):
        size = struct.unpack('!h', self.bytes[self.position:self.position + 2])[0]
        value = self.bytes[self.position + 2:self.position + 2 + size]
        self.position += size + 2
        return value

    def readUnsignedUTF(self):
        size = struct.unpack('!H', self.bytes[self.position:self.position + 2])[0]
        value = self.bytes[self.position + 2:self.position + 2 + size]
        self.position += size + 2
        return value

    def readBool(self):
        value = struct.unpack('!?', self.bytes[self.position:self.position + 1])[0]
        self.position += 1
        if value == 1:
            return True
        return False

    def readUTFBytes(self, size):
        value = self.bytes[self.position:self.position + int(size)]
        self.position += int(size)
        return value

    def toByteArray(self):
        return self.bytes[self.position:len(self.bytes)]

    def getLength(self):
        return len(self.bytes)

    def bytesAvailable(self):
        return len(self.bytes) - self.position

def m8(n):
    return ctypes.c_byte(n & 255).value


def m32(n):
    return ctypes.c_int(n & 4294967295).value


def n32(n):
    return n & 4294967295


def mls(a, b):
    return m32(a << b)


def rshift(val, n):
    if val >= 0:
        return val >> n
    return val + 4294967296 >> n

def cryptPass(password):
    return base64.b64encode(hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode() + b'\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0').digest()).decode('utf-8')

class Bot:
    def __init__(self):
        self.id = None
        self.closed = False
        self.proxyIP = "127.0.0.1"
        self.apiURL = ""
        self.proxyPort = None
        self.dropInfo = None

        self.connection = None
        self.reader = None
        self.writer = None

        self.foot = 0
        self.swfInfo = {}
        self.dkeys = []
        self.enterRoomTimer = None
        self.language = None

        self.login = None
        self.username = None
        self.password = password
        self.useTime = 0
        self.roomListOpenCount = 0
        self.limit = 0
        self.firstMessage = False
        self.rooms = []
        self.enteringRoom = None
        self.bulle = None
        self.blockedNames = []

        self.lastMessage = ""
        self.messages = []
        self.connectedPlatform = False
        self.firstRoom = True
        self.isWaitBot = False
        self.sentMods = False
        self.isBanned = False
        self.sendingMessagesTo = []

    async def start(self, id, username, password, language, message, apikey):
        self.id = id
        try:
            if len(proxies) == len(usernames):
                if proxies[self.id] is not None:
                    self.proxyIP = proxies[self.id].split(":")[0]
                    self.proxyPort = proxies[self.id].split(":")[1]
            else:
                if proxies[-1] is not None:
                    self.proxyIP = proxies[-1].split(":")[0]
                    self.proxyPort = proxies[-1].split(":")[1]
        except IndexError:
            pass

        self.dropInfo = [self.id, username, password, language, message, apikey]
        self.language = {'en': 0, 'fr': 1, 'ru': 2, 'br': 3, 'es': 4, 'cn': 5, 'tr': 6, 'no': 7, 'pl': 8, 'hu': 9, 'nl': 10, 'ro': 11, 'id': 12, 'de': 13, 'e2': 14, 'ar': 15, 'ph': 16, 'lt': 17, 'jp': 18, 'fi': 20, 'cz': 21, 'hr': 23, 'bg': 24, 'lv': 25, 'he': 26, 'it': 27, 'pt': 28, 'et': 29}[language]
        self.login = username
        if '@' in username:
            self.username = username.split('@')[0].capitalize()
        elif '#' in username:
            self.username = username.split('#')[0].capitalize()
        else:
            self.username = username.capitalize()
        self.messages = message.split('|')
        try:
            self.swfInfo = await self.getSWFInfo(username, password, language, message, apikey)
            self.dkeys = self.swfInfo['dkeys']
            self.connection = socks.socksocket()
            if self.proxyPort is not None:
                self.connection.set_proxy(socks.HTTP, self.proxyIP, int(self.proxyPort))
            self.connection.connect((self.swfInfo["ip"], 6112))
            try:
                self.reader, self.writer = await asyncio.open_connection(loop=loop, sock=self.connection)
            except Exception:
                await asyncio.sleep(30)
                await Bot().start(self.dropInfo[0], self.dropInfo[1], self.dropInfo[2], self.dropInfo[3], self.dropInfo[4], self.dropInfo[5])
                return
            print("[%s] [%s] Connected succesfully." % (self.username, str(self.proxyIP)))
            p = ByteArray()
            p.writeByte(28)
            p.writeByte(1)
            p.writeShort(int(self.swfInfo["cv"][0].split('.')[1]))
            p.writeUTF(self.swfInfo["cv"][1])
            p.writeUTF('ActiveX')
            p.writeUTF('x')
            p.writeInt(6125)
            p.writeUTF('')
            p.writeUTF('7d776cc1ac82a95a05faf75a55f047a11832c0f218e8ecc651abf416029ff36f')
            p.writeUTF('A=t&SA=t&SV=t&EV=t&MP3=t&AE=t&VE=t&ACC=t&PR=t&SP=f&SB=f&DEB=f&V=WIN 27,0,0,130&M=Adobe Windows&R=1920x1080&COL=color&AR=1.0&OS=Windows 10&ARCH=x86&L=tr&IME=t&PR32=t&PR64=t&PT=ActiveX&AVD=f&LFD=f&WD=f&TLS=t&ML=5.1&DP=72')
            p.writeInt(0)
            p.writeInt(892)
            p.writeShort(0)
            await self.sendData(p)
            try:
                ckeyRespond = await self.reader.read(21)
                user_foot = ByteArray(ckeyRespond[4:9])
                print("[%s] %s onlines!" % (self.username, str(user_foot.readInt())))
                self.foot = user_foot.readByte()
            except Exception:
                print('[%s] Wrong ckey, trying again!' % (self.username))
                await asyncio.sleep(5)
                await Bot().start(self.dropInfo[0], self.dropInfo[1], self.dropInfo[2], self.dropInfo[3], self.dropInfo[4], self.dropInfo[5])
                return
            try:
                asyncio.ensure_future(self.ping())
            except Exception:
                pass
            try:
                asyncio.ensure_future(self.ping2())
            except Exception:
                pass

            self.loginPass = ByteArray(ckeyRespond[-4:]).readInt()
            for code in self.swfInfo['pass']:
                self.loginPass = self.loginPass ^ code

            await self.loginPlayer()
            await self.listen()
        except Exception:
            print("[%s] Error while connecting %s:%s to game. Trying again." % (self.username, self.proxyIP, self.proxyPort))
            await asyncio.sleep(3)
            await Bot().start(self.dropInfo[0], self.dropInfo[1], self.dropInfo[2], self.dropInfo[3], self.dropInfo[4], self.dropInfo[5])
            return

    async def getSWFInfo(self, username, password, language, message, code):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.apiURL + code + '/' + quote(username, safe='') + '/' + quote(password, safe='') + '/' + quote(language, safe='') + '/' + quote(message.encode('ascii', 'ignore').decode('utf-8'))) as resp:
                    response = await resp.json()
                    return response
            return json.loads(urlopen(Request(self.apiURL + code + '/' + quote(username, safe='') + '/' + quote(password, safe='') + '/' + quote(language, safe='') + '/' + quote(message.encode('ascii', 'ignore').decode('utf-8'), safe=''), headers={'User-Agent': 'Mozilla/5.0'})).read().decode())
        except Exception:
            await asyncio.sleep(5)
            await Bot().start(self.dropInfo[0], self.dropInfo[1], self.dropInfo[2], self.dropInfo[3], self.dropInfo[4], self.dropInfo[5])
            return

    async def sendData(self, data):
        try:
            if not self.closed:
                p = ByteArray()
                p.writeByte(1 if data.getLength() <= 255 else 2)
                if data.getLength() <= 255:
                    p.writeUnsignedByte(data.getLength())
                else:
                    p.writeUnsignedShort(data.getLength())
                p.writeByte(self.foot)
                p.write(data.toByteArray())
                self.writer.write(p.toByteArray())
                self.foot = (self.foot + 1) % 100
        except Exception:
            await Bot().start(self.dropInfo[0], self.dropInfo[1], self.dropInfo[2], self.dropInfo[3], self.dropInfo[4], self.dropInfo[5])
            return

    async def ping(self):
        if not self.closed:
            p = ByteArray()
            p.writeByte(26)
            p.writeByte(26)
            await self.sendData(p)
            await self.sendData(p)
            await asyncio.sleep(20)
            await self.ping()

    async def ping2(self):
        if not self.closed:
            p = ByteArray()
            p.writeByte(8)
            p.writeByte(30)
            p.writeByte(20)
            await self.sendData(p)
            await asyncio.sleep(10)
            await self.ping2()

    async def loginPlayer(self):
        p = ByteArray()
        p.writeByte(8)
        p.writeByte(2)
        p.writeByte(self.language)
        p.writeByte(0)
        await self.sendData(p)

        p = ByteArray()
        p.writeByte(28)
        p.writeByte(17)
        p.writeUTF('tr')
        p.writeUTF('Windows 10')
        p.writeUTF('WIN 27,0,0,130')
        p.writeByte(0)
        await self.sendData(p)

        p = ByteArray()
        p.writeUTF(self.login)
        p.writeUTF(cryptPass(self.password))
        p.writeUTF('http://www.transformice.com/ChargeurTransformice.swf')
        p.writeUTF(random.choice(["vanilla", "defilante", "racing", "#deathmatch", "bootcamp"]) + str(random.randint(1, 20)))
        p.writeInt(m32(self.loginPass))
        p.writeByte(0)
        p.writeUTF('')
        p2 = ByteArray()
        p2.writeByte(26)
        p2.writeByte(8)
        p2.write((await self.cyrptdec(p)).toByteArray())
        await self.sendData(p2)

    async def cyrptdec(self, param1):
        var_16 = ByteArray()
        _loc6_ = 0
        _loc7_ = 0
        while 8 > param1.getLength():
            param1.writeByte(0)
            await asyncio.sleep(0)

        _loc3_ = param1.getLength() % 4
        if _loc3_:
            _loc6_ = -_loc3_ + 4
            _loc7_ = 0
            while _loc7_ < _loc6_:
                param1.writeByte(0)
                _loc7_ += 1
                await asyncio.sleep(0)

        param1.position = 0
        _loc4_ = param1.getLength() / 4
        _loc5_ = {}
        for a in range(0, int(_loc4_)):
            _loc5_[a] = 0
            await asyncio.sleep(0)

        _loc7_ = 0
        while _loc7_ < _loc4_:
            _loc5_[_loc7_] = param1.readInt()
            _loc7_ += 1
            await asyncio.sleep(0)

        await self.method_2219(_loc5_, 'identification')
        var_16.writeShort(_loc4_)
        _loc7_ = 0
        while _loc7_ < _loc4_:
            var_16.writeInt(m32(_loc5_[_loc7_]))
            _loc7_ += 1
            await asyncio.sleep(0)

        return var_16

    async def method_2219(self, param1, param2):
        _loc12_ = 0
        _loc3_ = await self.method_948(param2)
        if 2 > len(param1):
            param1.push(0)
        _loc4_ = len(param1)
        _loc5_ = param1[_loc4_ - 1]
        _loc6_ = param1[0]
        _loc7_ = m32(2654435769)
        _loc8_ = int(int(6 + 52 / _loc4_))
        _loc9_ = int(_loc8_)
        _loc10_ = _loc8_
        _loc11_ = 0
        while _loc10_ > 0:
            _loc11_ = _loc11_ + _loc7_
            _loc9_ = _loc11_ >> 2 & 3
            _loc12_ = 0
            await asyncio.sleep(0)
            while _loc12_ < _loc4_:
                _loc6_ = param1[(_loc12_ + 1) % _loc4_]
                _loc8_ = (rshift(_loc5_, 5) ^ mls(_loc6_, 2)) + (rshift(_loc6_, 3) ^ mls(_loc5_, 4)) ^ (_loc11_ ^ _loc6_) + (_loc3_[_loc12_ & 3 ^ _loc9_] ^ _loc5_)
                _loc5_ = param1[_loc12_] = m32(param1[_loc12_] + _loc8_)
                _loc12_ += 1
                await asyncio.sleep(0)

            _loc10_ -= 1
            await asyncio.sleep(0)

        return param1

    async def method_948(self, param1):
        var_1618 = self.dkeys
        _loc3_ = 0
        _loc4_ = len(var_1618)
        _loc5_ = len(param1)
        _loc6_ = 5381
        while _loc3_ < _loc4_:
            await asyncio.sleep(0)
            _loc6_ = m32(int(mls(_loc6_, 5) + _loc6_ + var_1618[_loc3_] + ord(param1[_loc3_ % _loc5_])))
            _loc3_ += 1

        _loc3_ = 0
        _loc2_ = {}
        while _loc3_ < _loc4_:
            await asyncio.sleep(0)
            _loc6_ = _loc6_ ^ mls(_loc6_, 13)
            _loc6_ = _loc6_ ^ _loc6_ >> 17
            _loc6_ = _loc6_ ^ mls(_loc6_, 5)
            _loc2_[_loc3_] = _loc6_
            _loc3_ += 1

        return _loc2_

    async def cyrypt(self, cmddtec, a):
        bytea = ByteArray()
        bytea.write(a)
        _loc2_ = await self.method_948('msg')
        _loc3_ = bytea
        var_16 = ByteArray()
        _loc4_ = len(_loc2_)
        while _loc3_.bytesAvailable():
            await asyncio.sleep(0)
            cmddtec = (1 + cmddtec) % _loc4_
            kh = _loc3_.readByte()
            i = kh ^ _loc2_[cmddtec]
            var_16.writeByte(m8(i))

        return var_16.toByteArray()

    async def listen(self):
        while True:
            await asyncio.sleep(0)
            if not self.closed:
                try:
                    recv = ByteArray(await self.reader.read(10000))
                    if recv.bytesAvailable():
                        position = recv.position
                        lenlen = recv.readByte()
                        length = 0
                        if lenlen == 1:
                            length = recv.readUnsignedByte()
                        elif lenlen == 2:
                            length = recv.readUnsignedShort()
                        if recv.bytesAvailable() >= length:
                            read = ByteArray(recv.bytes[lenlen + 1:length + lenlen + 1])
                            recv.bytes = recv.bytes[length + lenlen + 1:]
                            position = 0
                            try:
                                token1, token2 = read.readByte(), read.readByte()
                                if token1 == 1:
                                    if token2 == 1:
                                        read.readShort()
                                        oldtoken1, oldtoken2 = read.readByte(), read.readByte()
                                        if oldtoken1 == 26 and (oldtoken2 == 17 or oldtoken2 == 18):
                                            hours, reason = read.toByteArray()[1:].split(b'\x01')
                                            print('[' + self.username + '] Banned for ' + str(int(int(hours.decode()) / 3600000)) + ' hour(s). Reason : ' + reason.decode())
                                            self.isBanned = True
                                            return

                                if token1 == 26:
                                    if token2 == 12:
                                        resultType = read.readByte()
                                        if resultType == 1:
                                            print(self.username + ' is already connected!')
                                            await asyncio.sleep(30)
                                            await Bot().start(self.dropInfo[0], self.dropInfo[1], self.dropInfo[2], self.dropInfo[3], self.dropInfo[4], self.dropInfo[5])
                                            return
                                        elif resultType == 2:
                                            print('[%s] Wrong password!' % self.username)
                                        else:
                                            print('[%s] Something went wrong while logging in.' % self.username)
                                    elif token2 == 35:
                                        splits = read.toByteArray().split(b'mjj')
                                        h = ByteArray(splits[len(splits) - 1])
                                        strtype = h.readUTF().decode()
                                        while h.bytesAvailable():
                                            h.readByte()
                                            lang = h.readByte()
                                            roomName = h.readUTF().decode()
                                            players = h.readShort()
                                            if lang == self.language and players != 0:
                                                if not roomName.startswith('#madchess'):
                                                    if not roomName in self.rooms:
                                                        self.rooms.append(roomName)
                                            (h.readByte(), h.readByte())

                                        self.roomListOpenCount += 1
                                        # if self.roomListOpenCount == 9:
                                        #     self.roomListOpenCount = 0
                                        #     print("All rooms: " + ", ".join(self.rooms))
                                        #     asyncio.ensure_future(self.roomTour())

                                elif token1 == 28:
                                    if token2 == 5:
                                        read.readShort()
                                        messages = read.readUTF().decode().split("\n")
                                        if not messages[0] == "\x00)<ROSE>$PasAutoriseParlerSurServeur</ROSE>\x00":
                                            self.sentMods = True
                                            del messages[0]
                                            self.blockedNames = []
                                            for message in messages:
                                                self.blockedNames.extend(re.findall('<BV>(.*?)</BV>', message[5:]))
                                            print("[" + self.username + "] [Info] [Mods Online] " + ", ".join(self.blockedNames))
                                            asyncio.ensure_future(self.roomTour())
                                        else:
                                            print("[%s] You can't speak at this server." % self.username)

                                elif token1 == 60:
                                    if token2 == 3:
                                        if not self.connectedPlatform:
                                            self.connectedPlatform = True
                                            print("[%s] Logged in." % self.username)
                                            asyncio.ensure_future(self.sendRoomList())
                                        else:
                                            protocole = read.readShort()
                                            if protocole == 66:
                                                pmFrom = read.readUTF().decode()
                                                language = read.readInt()-1
                                                languages = {0: 'en', 1: 'fr', 2: 'ru', 3: 'br', 4: 'es', 5: 'cn', 6: 'tr', 7: 'no', 8: 'pl', 9: 'hu', 10: 'nl', 11: 'ro', 12: 'id', 13: 'de', 14: 'e2', 15: 'ar', 16: 'ph', 17: 'lt', 18: 'jp', 20: 'fi', 21: 'cz', 23: 'hr', 24: 'bg', 25: 'lv', 26: 'he', 27: 'it', 28: 'pt', 29: 'et'}
                                                if pmFrom.split('#')[0] != self.username.lower():
                                                    read.readUTF().decode()
                                                    print('[%s] > [%s] [%s] %s' % (self.username, languages[language], pmFrom.capitalize(), read.readUTF().decode()))
                            except struct.error:
                                pass
                except (ConnectionAbortedError, ConnectionResetError):
                    pass
            else:
                break
    
    async def sendRoomList(self):
        self.rooms = []
        self.roomListOpenCount = 0
        roomList = [1, 1, 3, 8, 9, 11, 2, 10, 18, 16]
        printedMessage = {1 : False, 3 : False, 8 : False, 9 : False, 11 : False, 2 : False, 10 : False, 18 : False, 16 : False}
        for id, type in enumerate(roomList):
            while not self.roomListOpenCount == id:
                roomType = {1 : "normal", 3 : "vanilla", 8 : "survivor", 9 : "racing", 11 : "music", 2 : "bootcamp", 10 : "defilante", 18 : "module", 16 : "village"}
                if not printedMessage[type]:
                    print('[%s] [Room List] %s rooms are parsed.' % (self.username, roomType[type].capitalize()))
                printedMessage[type] = True
                p = ByteArray()
                p.writeByte(26)
                p.writeByte(35)
                p.writeByte(type)
                await self.sendData(p)
                await asyncio.sleep(0.8)
        self.sentMods = False
        while not self.sentMods:
            await self.sendCommand('mod')
            await asyncio.sleep(0.8)

    async def sendCommand(self, command):
        if not self.closed:
            p = ByteArray()
            p.writeUTF(command)
            p2 = ByteArray()
            p2.writeByte(6)
            p2.writeByte(26)
            p2.write(await self.cyrypt(self.foot, p.toByteArray()))
            p2.writeByte(0)
            await self.sendData(p2)

    async def roomTour(self):
        print("[" + self.username + "] [Info] [All Rooms] " + ", ".join(self.rooms))
        for room in self.rooms:
            if not self.isBanned:
                print("[%s] [Status] [Room] %s" % (self.username, room))
                await self.enterRoom(room)
                await asyncio.sleep(1)

                message = random.choice(self.messages)
                if len(self.messages) >= 2:
                    while message == self.lastMessage:
                        await asyncio.sleep(0)
                        message = random.choice(self.messages)
                self.lastMessage = message
                await self.sendMessage(self.lastMessage + " #" + str(random.randint(1000, 9999)))
        if not self.isBanned:
            await self.sendRoomList()

    async def enterRoom(self, roomName):
        if not self.closed:
            p = ByteArray()
            p.writeByte(5)
            p.writeByte(38)
            p.writeByte(-1)
            p.writeUTF(roomName)
            p.writeByte(0)
            await self.sendData(p)

    async def sendMessage(self, message, hey=False):
        if not self.closed:
            if hey:
                message += ' #' + ('').join((random.choice(string.hexdigits) for _ in range(1)))
            p = ByteArray()
            p.writeUTF(message)
            p2 = ByteArray()
            p2.writeByte(6)
            p2.writeByte(6)
            p2.write(await self.cyrypt(self.foot, p.toByteArray()))
            await self.sendData(p2)


config = configparser.ConfigParser()
config.read_file(codecs.open("./config.txt", "r", "utf8"))

usernames = config.get("Bot", "usernames").split(", ")
password = config.get("Bot", "password")
language = config.get("Bot", "language")
keyword = config.get("Bot", "keyword")
message = config.get("Bot", "message").replace("pvpismi", keyword)
proxies = config.get("Bot", "proxies").split(", ")
apikey = config.get("Bot", "apikey")

if proxies[0] == "false":
    proxies = []

threads = []

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*[Bot().start(id, username, password, language, message, apikey) for id, username in enumerate(usernames)]))
loop.close()
