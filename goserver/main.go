package main

import (
	"context"
	"fmt"
	"goserver/api"
	bpb "goserver/protogen/bike"
	hwpb "goserver/protogen/helloworld"
	"log"
	"net"

	"google.golang.org/protobuf/types/known/emptypb"

	"google.golang.org/grpc"
)

// HelloWorld Service

type helloWorldServer struct {
	hwpb.UnimplementedHelloWorldServer
}

func (s *helloWorldServer) SayHello(_ context.Context, req *hwpb.Greetings) (*hwpb.BackAtYou, error) {
	// context.Context는 gRPC 메서드에서 요청의 생명 주기를 관리하고 제어함
	fmt.Println("Received:", req.GetBody())
	fmt.Println("From:", req.GetName())
	response := fmt.Sprintf("Hello %s!", req.GetName())
	return &hwpb.BackAtYou{Response: response}, nil
}

func (s *helloWorldServer) SayHelloStream(req *hwpb.Greetings, stream hwpb.HelloWorld_SayHelloStreamServer) error {
	fmt.Println("Received:", req.GetBody())
	fmt.Println("From:", req.GetName())
	response := fmt.Sprintf("Hello %s!", req.GetName())
	for _, char := range response {
		if err := stream.Send(&hwpb.BackAtYou{Response: string(char)}); err != nil {
			return err
		}
	}
	return nil
}

// Bike Service
type bikeServer struct {
	bpb.UnimplementedBikeServer
}

func (s *bikeServer) GetStationList(_ context.Context, _ *emptypb.Empty) (*bpb.StationList, error) {
	totalCount, stations, _ := api.GetBikeStns()
	stationPb := api.StationsToStationPbList(stations)
	return &bpb.StationList{Count: int32(totalCount), Stations: stationPb}, nil
}

func (s *bikeServer) GetRealTimeStationStatus(_ *emptypb.Empty, stream bpb.Bike_GetRealTimeStationStatusServer) error {
	statuses, err := api.GetBikeStnStatus()
	if err != nil {
		log.Println("Error:", err)
		return err
	}
	for _, status := range statuses {
		if err := stream.Send(api.StationStatusToStationStatusPb(status)); err != nil {
			log.Println(err)
			continue
		}
	}
	return nil
}

func main() {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", 9000))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	hwpb.RegisterHelloWorldServer(s, &helloWorldServer{})
	bpb.RegisterBikeServer(s, &bikeServer{})

	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
