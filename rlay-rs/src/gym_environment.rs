use std::collections::HashMap;
use std::error::Error;

pub trait GymEnvironment {
    fn reset(&mut self, seed: Option<i32>, options: HashMap<String, String>) -> Result<(Vec<f32>, HashMap<String, String>), dyn Error>;
    fn step(&mut self, action: Vec<f32>) -> Result<(Vec<f32>, f32, bool, bool, HashMap<String, String>), dyn Error>;
    fn close(&mut self) -> Result<(), dyn Error>;
}
