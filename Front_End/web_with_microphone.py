import asyncio
import json
import logging
import websockets
import time
import database
import os

#from Microphone import Phone
import argparse

copy from tuochao
parser = argparse.ArgumentParser()

parser.add_argument("-d", "--device", type = int, default = 8, help="decice index of microphone")
parser.add_argument("-r", "--rate", type = int, default = 48000, help="sampling rate of microphone")
parser.add_argument("-c", "--channel", type = int, default = 6, help="the number of channels")
parser.add_argument("-w", "--width", type = int, default = 2, help="the size of a single data (Bytes)")
parser.add_argument("-l", "--length", type = int, default = 1024, help="The lenght of chunk")

args = parser.parse_args()
RESPEAKER_RATE = args.rate
RESPEAKER_CHANNELS = args.channel
RESPEAKER_WIDTH = args.width # run getDeviceInfo.py to get index
RESPEAKER_INDEX = args.device  # refer to input device id
CHUNK = args.length
RECORD_SECONDS = 5


microphone = Phone(RESPEAKER_RATE, RESPEAKER_CHANNELS,RESPEAKER_WIDTH,RESPEAKER_INDEX,CHUNK, 1)
# copy from tuochao


logging.basicConfig()

STATE = {"value": 0}

USERS = set()

def writedata(nowtime,data):
    f = open('.\\keyboard_data\\'+str(nowtime)+'.txt', "a")
    f.write(str(data['input'])+'\n'+str(data['time']))
    f.close()

def newfile(nowtime):
    f = open('.\\keyboard_data\\'+ str(nowtime) +'.txt', 'w')
    f.close()

def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def sentence_event():
    sentence = database.package_give_sentence(sentences,rare_dict)
    return json.dumps({"type":"txt","count":sentence})

async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        microphone.begin()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_sentence():
    if USERS:
        message = sentence_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    global nowtime
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            microphone.end()
            microphone.save_file(nowtime+'.wav')
            writedata(nowtime,data)
            await notify_sentence()

            print(data)
            print(time.time())
            # await notify_state()
    finally:
        await unregister(websocket)

sentences = database.get_sentences()
rare_dict = database.generate_rare_dict(sentences)
nowtime = int(time.time())
print(nowtime)
newfile(nowtime)
print('文字数据库加载完成')

start_server = websockets.serve(counter, "localhost", 6789)

microphone.begin()
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()