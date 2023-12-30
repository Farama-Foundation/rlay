#!bash
protoc -I./protos/ --python_out=./rlay/ --pyi_out=./rlay/ --rust_out ./rlay-rs/src/ ./protos/gym_grpc/gym_rlay.proto
