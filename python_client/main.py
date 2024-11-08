import json
import threading
import time

import grpc
import redis
import socketio

from protogen import bike_pb2_grpc, bike_pb2
from google.protobuf import empty_pb2
from google.protobuf.json_format import MessageToDict


def get_redis_client() -> redis.Redis:
    return redis.Redis(host="localhost", port=6379, decode_responses=True)


# Socket.IO 서버 생성
sio = socketio.Server(logger=True, engineio_logger=True, async_mode="threading")
app = socketio.WSGIApp(sio)


# 연결 이벤트 핸들러
@sio.event
def connect(sid, environ):
    print("클라이언트가 연결되었습니다:", sid)


# 메시지 이벤트 핸들러
@sio.event
def message(sid, data):
    print("클라이언트로부터 메시지 수신:", data)
    sio.emit("bike_return", "Return")


@sio.event
def stn_list(sid, data):
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
        r.set(key, encoded)
    else:
        # redis 에 이미 캐시가 있으면 캐시에서 응답
        print("Cache hit")
        data = r.get(key)
    sio.emit("stn_list", data, room=sid)


# gRPC 데이터를 가져오는 함수
def fetch_and_notify():
    # gRPC 채널과 스텁 초기화
    r = get_redis_client()
    with grpc.insecure_channel("localhost:9000") as channel:
        stub = bike_pb2_grpc.BikeStub(channel)

        while True:
            # gRPC 서버 스트리밍 호출
            try:
                response_stream = stub.GetRealTimeStationStatus(empty_pb2.Empty())
                for response in response_stream:
                    key = response.stn_name
                    value = response.parked_bike_cnt

                    # Redis에서 이전 값 가져오기 + 없으면 설정하기
                    previous_value = r.getset(key, value)

                    # 값이 변경되었을 때만 업데이트 및 Socket.IO로 알림
                    if previous_value is None:
                        print(f"[REDIS] {key}: {value}")
                    else:
                        prv_int = int(previous_value)
                        if prv_int == value:
                            pass
                        if prv_int > value:
                            print(f"{key} 대여소의 자전거가 {prv_int - value} 대 빠졌습니다.")
                            print(f"[REDIS] {key}: {prv_int} -> {value}")
                            sio.start_background_task(
                                sio.emit, "bike_rent", MessageToDict(response)
                            )  # 웹 클라이언트에 알림 전송
                        elif prv_int < value:
                            print(f"{key} 대여소에 자전거가 {value - prv_int} 대 들어왔습니다.")
                            print(f"[REDIS] {key}: {prv_int} -> {value}")
                            sio.start_background_task(
                                sio.emit, "bike_return", MessageToDict(response)
                            )  # 웹 클라이언트에 알림 전송

                # 1분 대기 후 다시 요청
                time.sleep(120)

            except grpc.RpcError as e:
                print("gRPC error:", e)
                time.sleep(120)  # 오류 발생 시에도 1분 대기 후 재시도


# gRPC 데이터 수신을 위한 스레드 시작
grpc_thread = threading.Thread(target=fetch_and_notify, daemon=True)
grpc_thread.start()

# 실행할 때 웹 소켓 서버 시작
if __name__ == "__main__":
    # TODO: gunicorn 을 사용하도록 변경
    # gunicorn --workers 1 --threads 2 --bind 127.0.0.1:8000 main:app
    # eventlet.wsgi.server(eventlet.listen(("", 8000)), app)
    pass
