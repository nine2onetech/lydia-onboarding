// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.5.1
// - protoc             v5.28.3
// source: helloworld.proto

package protogen

import (
	context "context"

	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.64.0 or later.
const _ = grpc.SupportPackageIsVersion9

const (
	HelloWorld_SayHello_FullMethodName       = "/HelloWorld/SayHello"
	HelloWorld_SayHelloStream_FullMethodName = "/HelloWorld/SayHelloStream"
)

// HelloWorldClient is the client API for HelloWorld service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type HelloWorldClient interface {
	// Say Hello to World! The World will respond
	SayHello(ctx context.Context, in *Greetings, opts ...grpc.CallOption) (*BackAtYou, error)
	// Say Hello to World! The World will respond but slowly..
	SayHelloStream(ctx context.Context, in *Greetings, opts ...grpc.CallOption) (grpc.ServerStreamingClient[BackAtYou], error)
}

type helloWorldClient struct {
	cc grpc.ClientConnInterface
}

func NewHelloWorldClient(cc grpc.ClientConnInterface) HelloWorldClient {
	return &helloWorldClient{cc}
}

func (c *helloWorldClient) SayHello(ctx context.Context, in *Greetings, opts ...grpc.CallOption) (*BackAtYou, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(BackAtYou)
	err := c.cc.Invoke(ctx, HelloWorld_SayHello_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *helloWorldClient) SayHelloStream(ctx context.Context, in *Greetings, opts ...grpc.CallOption) (grpc.ServerStreamingClient[BackAtYou], error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	stream, err := c.cc.NewStream(ctx, &HelloWorld_ServiceDesc.Streams[0], HelloWorld_SayHelloStream_FullMethodName, cOpts...)
	if err != nil {
		return nil, err
	}
	x := &grpc.GenericClientStream[Greetings, BackAtYou]{ClientStream: stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

// This type alias is provided for backwards compatibility with existing code that references the prior non-generic stream type by name.
type HelloWorld_SayHelloStreamClient = grpc.ServerStreamingClient[BackAtYou]

// HelloWorldServer is the server API for HelloWorld service.
// All implementations must embed UnimplementedHelloWorldServer
// for forward compatibility.
type HelloWorldServer interface {
	// Say Hello to World! The World will respond
	SayHello(context.Context, *Greetings) (*BackAtYou, error)
	// Say Hello to World! The World will respond but slowly..
	SayHelloStream(*Greetings, grpc.ServerStreamingServer[BackAtYou]) error
	mustEmbedUnimplementedHelloWorldServer()
}

// UnimplementedHelloWorldServer must be embedded to have
// forward compatible implementations.
//
// NOTE: this should be embedded by value instead of pointer to avoid a nil
// pointer dereference when methods are called.
type UnimplementedHelloWorldServer struct{}

func (UnimplementedHelloWorldServer) SayHello(context.Context, *Greetings) (*BackAtYou, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SayHello not implemented")
}
func (UnimplementedHelloWorldServer) SayHelloStream(*Greetings, grpc.ServerStreamingServer[BackAtYou]) error {
	return status.Errorf(codes.Unimplemented, "method SayHelloStream not implemented")
}
func (UnimplementedHelloWorldServer) mustEmbedUnimplementedHelloWorldServer() {}
func (UnimplementedHelloWorldServer) testEmbeddedByValue()                    {}

// UnsafeHelloWorldServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to HelloWorldServer will
// result in compilation errors.
type UnsafeHelloWorldServer interface {
	mustEmbedUnimplementedHelloWorldServer()
}

func RegisterHelloWorldServer(s grpc.ServiceRegistrar, srv HelloWorldServer) {
	// If the following call pancis, it indicates UnimplementedHelloWorldServer was
	// embedded by pointer and is nil.  This will cause panics if an
	// unimplemented method is ever invoked, so we test this at initialization
	// time to prevent it from happening at runtime later due to I/O.
	if t, ok := srv.(interface{ testEmbeddedByValue() }); ok {
		t.testEmbeddedByValue()
	}
	s.RegisterService(&HelloWorld_ServiceDesc, srv)
}

func _HelloWorld_SayHello_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Greetings)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(HelloWorldServer).SayHello(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: HelloWorld_SayHello_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(HelloWorldServer).SayHello(ctx, req.(*Greetings))
	}
	return interceptor(ctx, in, info, handler)
}

func _HelloWorld_SayHelloStream_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(Greetings)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(HelloWorldServer).SayHelloStream(m, &grpc.GenericServerStream[Greetings, BackAtYou]{ServerStream: stream})
}

// This type alias is provided for backwards compatibility with existing code that references the prior non-generic stream type by name.
type HelloWorld_SayHelloStreamServer = grpc.ServerStreamingServer[BackAtYou]

// HelloWorld_ServiceDesc is the grpc.ServiceDesc for HelloWorld service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var HelloWorld_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "HelloWorld",
	HandlerType: (*HelloWorldServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "SayHello",
			Handler:    _HelloWorld_SayHello_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "SayHelloStream",
			Handler:       _HelloWorld_SayHelloStream_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "helloworld.proto",
}
