import json

import grpc
import redis
from aiohttp import web
import socketio

from protogen import bike_pb2_grpc, bike_pb2
from google.protobuf import empty_pb2
from google.protobuf.json_format import MessageToDict


def get_redis_client():
    return redis.Redis(host="localhost", port=6379, decode_responses=True)


# Socket.IO 서버 생성
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


# 연결 이벤트 핸들러
@sio.event
def connect(sid, environ):
    print("클라이언트가 연결되었습니다:", sid)


# 메시지 이벤트 핸들러
@sio.event
def message(sid, data):
    print("클라이언트로부터 메시지 수신:", data)


@sio.event
async def stn_list(sid, data):
    print("클라이언트가 대여소 목록을 요청했습니다.")
    r = get_redis_client()
    key = "stn_list"
    if not r.exists(key):
        print("Cache miss")
        with grpc.insecure_channel("localhost:9000") as channel:
            # Bike Service
            bike_stub = bike_pb2_grpc.BikeStub(channel)
            res: bike_pb2.StationList = bike_stub.GetStationList(empty_pb2.Empty())
        data = res
        # redis 에 캐시 저장
        encoded = json.dumps(MessageToDict(data), ensure_ascii=False).encode("utf-8")
        await r.set(key, encoded)
    else:
        # redis 에 이미 캐시가 있으면 캐시에서 응답
        print("Cache hit")
        data = r.get(key)
    await sio.emit("stn_list", data, room=sid)


# 실행할 때 웹 소켓 서버 시작
if __name__ == "__main__":
    web.run_app(app)
