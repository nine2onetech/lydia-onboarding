PROTO_DIR=protos
GO_ROOT=goserver
PYTHON_ROOT=python_client
WEB_ROOT=web-client
GO_OUT=protogen
PY_OUT=protogen
PROTO_FILE ?= service.proto
PROTO_NAME := $(shell echo $(PROTO_FILE) | cut -d'.' -f1)

.PHONY: run

protogen-all: protogen-go protogen-python

protogen-go:
	protoc -I=$(PROTO_DIR) --proto_path=$(PROTO_DIR) --go_out=$(GO_ROOT) --go-grpc_out=$(GO_ROOT) $(PROTO_DIR)/$(PROTO_FILE)

protogen-python:
	cd $(PYTHON_ROOT) &&  \
	uv run python3 -m grpc_tools.protoc -I=../$(PROTO_DIR) --proto_path=../$(PROTO_DIR) --python_out=$(PY_OUT) --pyi_out=$(PY_OUT) --grpc_python_out=$(PY_OUT) ../$(PROTO_DIR)/$(PROTO_FILE) && \
	sed -i '' 's/^import $(PROTO_NAME)_pb2 as $(PROTO_NAME)__pb2/from protogen import $(PROTO_NAME)_pb2 as $(PROTO_NAME)__pb2/' $(PY_OUT)/$(PROTO_NAME)_pb2_grpc.py

protogen-clean:
	rm -rf $(GO_ROOT)/$(GO_OUT)/*
	rm -rf $(PYTHON_ROOT)/$(PY_OUT)/*

run-go:
	cd $(GO_ROOT) && \
	go run main.go

run-python:
	cd $(PYTHON_ROOT) && \
	uv run main.py

grpc-client-test:
	cd $(PYTHON_ROOT) && \
	uv run grpc_test.py

run-web:
	cd $(WEB_ROOT) && \
	yarn dev --port 9898
