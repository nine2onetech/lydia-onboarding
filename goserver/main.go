package main

import (
	"context"
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"

	hwpb "goserver/protogen"
)

type helloWorldServer struct {
	hwpb.UnimplementedHelloWorldServer
}

func (s *helloWorldServer) SayHello(_ context.Context, req *hwpb.Greetings) (*hwpb.BackAtYou, error) {
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

func main() {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", 9000))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	hwpb.RegisterHelloWorldServer(s, &helloWorldServer{})
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
