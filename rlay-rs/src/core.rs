use std::fs::{File, OpenOptions};
use std::io::{Error, ErrorKind, Read, Write};
use std::os::unix::io::AsRawFd;
use std::path::Path;
use std::time::Duration;
use std::thread;
use memmap::{Mmap, MmapMut};

use protobuf::{Message};
use crate::gym_rlay::{GymnasiumMessage, StepReturn, ResetArgs};

pub struct Communicator {
    name: String,
    size: usize,
    file: File,
    map: MmapMut,
    active_code: u8,
    wait_code: u8,
    busy_code: u8,
}

impl Communicator {
    pub fn new(name: &str, size: usize, create: bool) -> Result<Communicator, Error> {
        let filename = format!("/tmp/{}", name);
        let mut file;
        let active_code;
        let wait_code;

        if create {
            if Path::new(&filename).exists() {
                std::fs::remove_file(&filename)?;
            }
            file = OpenOptions::new().read(true).write(true).create_new(true).open(&filename)?;
            file.set_len(size as u64)?;
            active_code = 0x01;
            wait_code = 0x02;
        } else {
            while !Path::new(&filename).exists() {
                thread::sleep(Duration::from_millis(1));
            }
            file = OpenOptions::new().read(true).write(true).open(&filename)?;
            active_code = 0x02;
            wait_code = 0x01;
        }

        let mut map = unsafe { MmapMut::map_mut(&file)? };
        if create {
            map[0] = active_code;
        }

        Ok(Communicator {
            name: name.to_string(),
            size,
            file,
            map,
            active_code,
            wait_code,
            busy_code: 0x00,
        })
    }

    pub fn send_message(&mut self, msg: &GymnasiumMessage) -> Result<(), Error> {
        let serialized_msg = msg.write_to_bytes()?;
        let msg_len = serialized_msg.len();
        if msg_len + 5 > self.size {
            return Err(Error::new(ErrorKind::Other, "Message is too long"));
        }

        while self.map[0] != self.active_code {
            thread::sleep(Duration::from_millis(1));
        }
        self.map[0] = self.busy_code;
        self.map[1..self.size].fill(0);

        self.map[1..5].copy_from_slice(&(msg_len as u32).to_le_bytes());
        self.map[5..5 + msg_len].copy_from_slice(&serialized_msg);
        self.map[0] = self.wait_code;

        Ok(())
    }

    pub fn receive_message(&mut self) -> Result<GymnasiumMessage, Error> {
        while self.map[0] != self.active_code {
            thread::sleep(Duration::from_millis(1));
        }

        let msg_len = u32::from_le_bytes([self.map[1], self.map[2], self.map[3], self.map[4]]) as usize;
        let mut msg = GymnasiumMessage::new();
        msg.merge_from_bytes(&self.map[5..5 + msg_len])?;

        Ok(msg)
    }

    pub fn close(self) -> Result<(), Error> {
        std::fs::remove_file(format!("/tmp/{}", self.name))
    }
}


