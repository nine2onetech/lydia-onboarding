# gRPC 통신 구현하기

1. [proto 파일의 관리](#1-proto-파일의-관리)
2. [실행하기](#2-실행하기)
### 1. proto 파일의 관리
* 모든 proto 파일은 `./protos` 디렉토리에 위치해야하며 Makefile 의 명령어를 이용하여 stub 파일을 생성합니다.

**go stub 파일 생성**
```bash
make protogen-go
```
**python stub 파일 생성**
```bash
make protogen-python
```
**go & python stub 파일 생성**
```bash
make protogen-all
```

### 2. 실행하기
**go 서버 실행**
```bash
make run-go
```
**python 클라이언트 실행**
```bash
make run-python
```
**web 클라이언트 실행**
```bash
make run-web
```
