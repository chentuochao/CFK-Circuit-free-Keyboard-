import asyncio
import json
import logging
import websockets
import time
import database
from multiprocessing import Queue, Process

logging.basicConfig()

STATE = {"value": 0}
WS_QUEUE = None
USERS = set()
sentences = []
rare_dict = []

def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def sentence_event():
    global sentences
    global rare_dict
    sentence = database.package_give_sentence(sentences,rare_dict)
    return json.dumps({"type":"txt","count":sentence})

async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
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
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            await notify_sentence()
            print(data)
            print(time.time())
            # await notify_state()

    finally:
        await unregister(websocket)

def ws_process_main(queue):
    sentences = database.get_sentences()
    rare_dict = database.generate_rare_dict(sentences)
    print('文字数据库加载完成')
    global WS_QUEUE
    WS_QUEUE = queue
    start_server = websockets.serve(counter, 'localhost', 6789)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    # loop.create_task(ws_wait_queue_and_publish_thread_main())
    loop.run_forever()



if __name__ == '__main__':
    WS_QUEUE = Queue(5)
    ws_process = Process(target=ws_process_main, args=(WS_QUEUE,))
    ws_process.start()


    try:
        M = initialM()
        queue = Queue(5)
        nowtime = newfile()
        read_process = Process(target=read, args=(queue,))
        read_process.start()
        try:
            while True:
                try:
                    a = queue.get(True,10)
                    break
                except QueueEmpty:
                    print("QueueEmpty, waiting for read process")
            get_process = Process(target =monitor, args=(queue,M,nowtime))
            get_process.start()
            try:
                read_process.join()
                get_process.join()
            finally:
                get_process.terminate()
        finally:
            read_process.terminate()
    finally:
        ws_process.terminate()