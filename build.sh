#python -m grpc_tools.protoc -I./rlay/protos/ --python_out=./rlay/ --pyi_out=./rlay/ --csharp_out=./rlay/ ./rlay/protos/gym_grpc/gym.proto
#protoc -I./rlay/protos/ --python_out=./rlay/ --pyi_out=./rlay/ --csharp_out=./rlayEnv/Assets/ ./rlay/protos/gym_grpc/gym.proto

protoc -I./protos/ --python_out=./rlay/ --pyi_out=./rlay/ --rust_out ./rlay-rs/src/ ./protos/gym_grpc/gym_rlay.proto

#python -m grpc_tools.protoc -I./rlay/protos/ --python_out=./rlay/ --pyi_out=./rlay/ --grpc_python_out=./rlay/ ./rlay/protos/gym_grpc/gym.proto
#protoc -I./rlay/protos/ --python_out=./rlay/ ./rlay/protos/gym_grpc/gym.proto

