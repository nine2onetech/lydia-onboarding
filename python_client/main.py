import asyncio
import logging
import json
import threading
from datetime import datetime

import grpc
from redis.asyncio import Redis
import socketio
from aiohttp import web, ClientSession
from protogen import bike_pb2_grpc, bike_pb2
from google.protobuf import empty_pb2
from google.protobuf.json_format import MessageToDict

# constants
GRPC_SERVER_HOST = "localhost:9000"
REQUEST_INTERVAL = 120  # 2분마다 요청

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S")
logger = logging.getLogger(__name__)


# Redis client
class RedisClient(object):
    def __init__(self):
        self.client = Redis(host="localhost", port=6379, decode_responses=True)

    def __new__(cls):
        # Singleton
        if not hasattr(cls, "instance"):
            cls.instance = super(RedisClient, cls).__new__(cls)
            logger.debug("RedisClient 객체 생성")
        else:
            logger.debug("RedisClient 객체 재사용")
        return cls.instance


def get_redis_client() -> Redis:
    """Redis 클라이언트 생성"""
    return RedisClient().client


# Socket.IO 서버 생성
sio = socketio.AsyncServer(async_mode="aiohttp", logger=False, engineio_logger=False, cors_allowed_origins="*")


# 연결 이벤트 핸들러
@sio.event
async def connect(sid, environ):
    logger.info("클라이언트가 연결되었습니다: " + sid)


# 메시지 이벤트 핸들러
@sio.event
async def message(sid, data):
    # 클라이언트로부터 메시지 수신 (테스트용)
    logger.debug("클라이언트로부터 메시지 수신: " + data)
    await sio.emit("message", "Received: " + data)


@sio.event
async def stn_list(sid, data):
    """대여소 목록 요청 이벤트 핸들러"""
    logger.info("클라이언트가 대여소 목록을 요청했습니다.")
    r = get_redis_client()
    key = "stn_list"
    if not await r.exists(key):
        logger.debug("Cache miss")
        with grpc.insecure_channel(GRPC_SERVER_HOST) as channel:
            # Bike Service
            bike_stub = bike_pb2_grpc.BikeStub(channel)
            # 대여소 현황을 미리 가져와, parkedBikeCnt 를 추가할 수 있도록 함
            await __get_real_time_station_status(bike_stub, socketio_emit=False)
            res: bike_pb2.StationList = bike_stub.GetStationList(empty_pb2.Empty())

        data = []
        for station in res.stations:
            d = MessageToDict(station)
            if await r.exists(station.stn_id):
                d["parkedBikeCnt"] = await r.get(station.stn_id)
            data.append(d)

        # redis 에 캐시 저장
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        await r.set(key, encoded)
        logger.debug("Cache set")
    else:
        # redis 에 이미 캐시가 있으면 캐시에서 응답
        logger.debug("Cache hit")
        data = json.loads(await r.get(key))
    await sio.emit("stn_list", data)


@sio.event
async def feed(sid, data):
    """실시간 피드 새로고침을 위한 이벤트 핸들러"""
    with grpc.insecure_channel(GRPC_SERVER_HOST) as channel:
        stub = bike_pb2_grpc.BikeStub(channel)
        await __get_real_time_station_status(stub, socketio_emit=True)


async def __get_real_time_station_status(stub, socketio_emit: bool = True):
    response_stream = stub.GetRealTimeStationStatus(empty_pb2.Empty())
    r = get_redis_client()
    for response in response_stream:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key = response.stn_id
        value = response.parked_bike_cnt
        stn_name = response.stn_name

        # Redis에서 이전 값 가져오기 + 없으면 설정하기
        previous_value = await r.getset(key, value)

        # 값이 변경되었을 때만 업데이트 및 Socket.IO로 알림
        if previous_value is None:
            logger.debug(f"[REDIS] {key}: {value}")
        else:
            prv_int = int(previous_value)
            if prv_int == value:
                pass
            elif prv_int > value:
                msg = f"{key} 대여소의 자전거가 {prv_int - value} 대 빠졌습니다."
                logger.debug(f"[REDIS] {key}: {prv_int} -> {value}")
                if socketio_emit:
                    await sio.start_background_task(
                        sio.emit,
                        "bike_rent",
                        dict(message=msg, timestamp=timestamp, parked_bike_cnt=value, stn_id=response.stn_id),
                    )
            else:
                msg = f"{stn_name} 대여소에 자전거가 {value - prv_int} 대 들어왔습니다."
                logger.debug(f"[REDIS] {key}: {prv_int} -> {value}")
                if socketio_emit:
                    await sio.start_background_task(
                        sio.emit,
                        "bike_return",
                        dict(message=msg, timestamp=timestamp, parked_bike_cnt=value, stn_id=response.stn_id),
                    )


async def fetch_and_notify_bike_rent_status():
    """지속적으로 gRPC 스트림 데이터를 가져오는 함수"""
    async with ClientSession() as _:
        with grpc.insecure_channel(GRPC_SERVER_HOST) as channel:
            stub = bike_pb2_grpc.BikeStub(channel)
            while True:
                try:
                    await __get_real_time_station_status(stub, socketio_emit=True)
                except grpc.RpcError as e:
                    print("gRPC error:", e)
                await asyncio.sleep(REQUEST_INTERVAL)  # 오류 발생 시에도 대기 후 재시도


def start_background_event_loop():
    """서브 스레드에서 독립적인 이벤트 루프 생성 및 실행"""
    loop = asyncio.new_event_loop()  # 서브 스레드에서 새 이벤트 루프 생성
    asyncio.set_event_loop(loop)  # 현재 스레드의 이벤트 루프 설정
    loop.run_until_complete(fetch_and_notify_bike_rent_status())


if __name__ == "__main__":
    # 서버 시작 전에 백그라운드 스레드를 시작
    thread = threading.Thread(target=start_background_event_loop)
    thread.start()

    # aiohttp 웹 서버 실행
    app = web.Application(logger=logger)
    sio.attach(app)
    web.run_app(app, handle_signals=True, shutdown_timeout=5)
