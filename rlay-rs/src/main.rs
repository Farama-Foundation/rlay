extern crate libc;
extern crate memmap;
extern crate protobuf;

use std::io::Write;
use protobuf::{Message, MessageField};

mod gym_rlay;
mod backends;
mod core;
mod gym_environment;

use gym_rlay::*;
// use backends::{ClientBackend, ServerBackend};



struct CartPoleEnv {
    state: Vec<f32>,
    step_count: i32,
}

struct NumpyArray {
    data: Vec<f32>,
    shape: Vec<i32>,
    dtype: String,
}
fn ndarray_to_protobuf(dtype: &str, shape: Vec<i32>, data: Vec<f32>) -> NDArray {
    let mut ndarray_proto = NDArray::new();
    ndarray_proto.set_shape(shape);
    ndarray_proto.set_dtype(String::from(dtype));
    ndarray_proto.set_data_float32(data);
    ndarray_proto
}

fn protobuf_to_ndarray(message: NDArray) -> (String, Vec<i32>, Vec<f32>) {
    let dtype = message.get_dtype().to_string();
    let shape = message.get_shape().to_vec();
    let data = match message.data {
        Some(NDArray_oneof_data::data_float32(data)) => data,
        _ => panic!("Unsupported data type"),
    };
    (dtype, shape, data)
}

impl NumpyArray {
    fn new(data: Vec<f32>, shape: Vec<i32>, dtype: String) -> NumpyArray {
        NumpyArray { data, shape, dtype }
    }

    fn from_vec(data: Vec<f32>) -> NumpyArray {
        NumpyArray { data, shape: vec![data.len() as i32], dtype: "float32".to_string() }
    }
}

fn main() {
    let mut mem_server = MemServer::new();


    mem_server.run();
}
