import grpc
from concurrent import futures
from pypro import test_pb2, test_pb2_grpc

class Hello(test_pb2_grpc.HelloServicer):

    def Helloworld(self, request, context):
        #print dir(request)
        result = "hello" + ' ' + request.Name
        print result
        return test_pb2.Response(Result=result)

def server():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_HelloServicer_to_server(Hello(), server)
    server.add_insecure_port('[::]:8088')
    server.start() 
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)

if __name__=='__main__':
    server()
