# GRPC 实现 golang 调用 python

[![Support Python Version](https://img.shields.io/badge/Python-2.7.5-brightgreen.svg)](https://www.python.org/)
[![Support Go Version](https://img.shields.io/badge/Go-1.12.6-blue.svg)](https://www.python.org/)
[![Support Protobuf Version](https://img.shields.io/badge/Protoc-3.9.1-blueviolet.svg)](https://www.python.org/)

---

## 简介

grpc 是谷歌开源的实现远程调用的系统，允许客户端对远程服务函数方法的调用，连接不同语言实现的服务，轻松解耦系统各模块。[grpc](https://doc.oschina.net/grpc?t=58008)

## 实现

### 环境安装

- python

```
pip install grpcio
pip install protobuf
pip install grpcio-tools
```

- [golang](https://www.cnblogs.com/leisurelylicht/p/Go-an-zhuanggRPC.html)

```
git clone https://github.com/grpc/grpc-go.git $GOPATH/src/google.golang.org/grpc 
git clone https://github.com/golang/net.git $GOPATH/src/golang.org/x/net 
git clone https://github.com/golang/text.git $GOPATH/src/golang.org/x/text 
go get -u github.com/golang/protobuf/{proto,protoc-gen-go} 
git clone https://github.com/google/go-genproto.git $GOPATH/src/google.golang.org/genproto 

cd $GOPATH/src/ 
go install google.golang.org/grpc
```
安装完会在 GOBIN 下生成 protoc-gen-go 可执行文件，拷贝到 PATH 下，如 /usr/local/bin 。

还需要安装 proto，[download](https://github.com/protocolbuffers/protobuf/releases)

最新版本为 protoc-3.9.1-linux-x86_64.zip

解压后：

```
tree protoc-3.9.1
protoc-3.9.1
├── bin
│   └── protoc
└── readme.txt

1 directory, 2 files
```

再将 bin/protoc 拷贝到 /usr/local/bin 下面就可以了。

### proto 配置文件

proto 文件是配置客户端和服务端通信协议，主要是对 API 接口的描述。

```
syntax = "proto3";
package test;

service Greeter {
    rpc Helloword(request) returns (response) {}
}

message request {
   string name = 1;
}

message response {
   string result = 1;
```

- syntax 是版本，推荐使用 proto3，语法简单清晰。

- package 是配置文件的名，用于包的导入

- service 定义服务

- rpc Helloword() 配置要调用的服务端函数（方法）

- request 入参

- response 返回值

- message request 定义入参数据格式

- message response 定义返回值数据格式

### 生成代码文件

根据不同语言生成对应的 grpc 代码文件

- python

```
python -m grpc_tools.protoc -I . --python_out=./pypro --grpc_python_out=./pypro ./test.proto
```

- golang 

```
protoc -I . --go_out=plugins=grpc:./gopro ./test.proto
```
gopro 拷贝到 $GOPATH/src 下。

### 服务端实现（python）

```
class Greeter(test_pb2_grpc.GreeterServicer):

    def Helloworld(self, request, context):
        #print dir(request)
        result = "hello" + ' ' + request.Name
        print result
        return test_pb2.Response(Result=result)
```

### 客户端实现（golang）

```
cli = gopro.NewGreeterClient(conn)
    res, err := cli.Helloworld(context.Background(), &gopro.Request{Name: "gzy"})
    if err != nil {
        fmt.Println("get grpc call failed: %v", err)
        return
    }
    fmt.Println(res.Result)
```

具体代码详见 [gRPC-play](https://github.com/guanzydev/grpc-play)

### 测试

启动服务：

```
python server.py
```

客户端访问：

```
go run client.go
hello world
```
