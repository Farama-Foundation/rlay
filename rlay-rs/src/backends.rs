use std::collections::HashMap;
use std::any::Any;
use std::error::Error;

use protobuf::Message;
use crate::gym_rlay::{GymnasiumMessage, StepReturn, ResetArgs, NDArray};
use crate::core::Communicator;
use crate::gym_environment::GymEnvironment;

pub struct ClientBackend {
    env: Box<dyn GymEnvironment>,
    communicator: Communicator,
}

impl ClientBackend {
    pub fn new(env_id: &str, port: u16) -> Result<ClientBackend, Box<dyn Error>> {
        let mut env = GymEnvironment::make(env_id)?;
        env.reset(None, HashMap::new())?;

        let mut communicator = Communicator::new("rlay", 1024, false)?;

        let message = GymnasiumMessage {
            status: Some(true),
            ..Default::default()
        };
        communicator.send_message(&message)?;

        communicator.receive_message()?;

        println!("Backend client listening on port {}", port);

        Ok(ClientBackend {
            env,
            communicator,
        })
    }

    pub fn run(&mut self) -> Result<(), Box<dyn Error>> {
        let message = GymnasiumMessage {
            request: Some(true),
            ..Default::default()
        };
        self.communicator.send_message(&message)?;

        let msg = self.communicator.receive_message()?;

        if let Some(reset_args) = msg.reset_args {
            let seed = if reset_args.seed != -1 { Some(reset_args.seed) } else { None };
            let options = unwrap_dict(&reset_args.options)?;

            let (obs, info) = self.env.reset(seed, options)?;
            let (mut reward, mut terminated, mut truncated) = (0.0, false, false);

            loop {
                let step_return = StepReturn {
                    obs: obs.clone(),
                    reward,
                    terminated,
                    truncated,
                    info: info.clone(),
                    ..Default::default()
                };
                let msg = GymnasiumMessage {
                    step_return: Some(step_return),
                    ..Default::default()
                };
                self.communicator.send_message(&msg)?;

                let response = self.communicator.receive_message()?;

                if let Some(action) = response.action {
                    let action = decode(&action)?;
                    let single_action = if action.len() == 1 { action[0] } else { 0.0 };
                    let (obs, reward, terminated, truncated, info) = self.env.step(vec![single_action])?;
                } else if let Some(reset_args) = response.reset_args {
                    let seed = if reset_args.seed != -1 { Some(reset_args.seed) } else { None };
                    let options = unwrap_dict(&reset_args.options)?;
                    let (obs, info) = self.env.reset(seed, options)?;
                    reward = 0.0;
                    terminated = false;
                    truncated = false;
                } else if response.close.unwrap_or(false) {
                    self.env.close()?;
                    return Ok(());
                } else if response.status.is_some() {
                    continue;
                } else {
                    return Err(From::from("Received an invalid message"));
                }
            }
        } else {
            Err(From::from("Environment must be reset before using."))
        }
    }
}

pub fn encode(array: &Vec<f32>) -> NDArray {
    NDArray {
        shape: vec![array.len() as i32],
        data: array.clone(),
        dtype: "float".to_string(),
        ..Default::default()
    }
}

pub fn decode(msg: &NDArray) -> Result<Vec<f32>, Box<dyn Error>> {
    Ok(msg.data.clone())
}

pub fn unwrap_dict(d: &HashMap<String, Value>) -> Result<HashMap<String, String>, Box<dyn Error>> {
    let mut new_dict = HashMap::new();
    for (k, v) in d.iter() {
        new_dict.insert(k.clone(), v.clone());
    }
    Ok(new_dict)
}
