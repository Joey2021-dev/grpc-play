import grpc
from pypro import test_pb2, test_pb2_grpc

def run():
    conn = grpc.insecure_channel('localhost:50051')
    stub = test_pb2_grpc.GreeterStub(conn)
    res = stub.Sayhello(test_pb2.Request(Name='gzy'))
    print("Greeter client received:" + res.Result)

if __name__=='__main__':
    run()
