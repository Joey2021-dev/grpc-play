package main

import (
    "flag"
    "fmt"
    gopro "gopro"
    "golang.org/x/net/context"
    grpc "google.golang.org/grpc"
)

var (
    addr = flag.String("host", "127.0.0.1:8088", "")

    cli gopro.HelloClient
)

func main() {
    conn, err := grpc.Dial(*addr,grpc.WithInsecure())
    if err != nil {
        fmt.Println("failed to connect server")
        return
    }
    cli = gopro.NewHelloClient(conn)
    res, err := cli.Helloworld(context.Background(), &gopro.Request{Name: "world"})
    if err != nil {
        fmt.Println("get grpc call failed: %v", err)
        return
    }
    fmt.Println(res.Result)
}
