from __future__ import annotations

import abc
import mmap
import os
import time
from typing import Any, Optional

import numpy as np

from rlay.gym_grpc import gym_rlay_pb2
from rlay.gym_grpc.gym_rlay_pb2 import GymnasiumMessage, ResetArgs, StepReturn
from rlay.utils import encode, wrap_dict


class BaseCommunicator(abc.ABC):
    @abc.abstractmethod
    def send_message(self, msg: gym_rlay_pb2.GymnasiumMessage):
        pass

    @abc.abstractmethod
    def receive_message(self) -> gym_rlay_pb2.GymnasiumMessage | None:
        pass

    @abc.abstractmethod
    def close(self):
        pass


class Communicator(BaseCommunicator):
    def __init__(self, name: str, size: int = 1024, create: bool = True):
        self.name = name
        self.size = size

        filename = f"/tmp/{name}"

        if create:
            if os.path.exists(filename):
                os.remove(filename)
            self.file = open(filename, "wb+")
            self.file.truncate(size)
            self.active_code = 0x01
            self.wait_code = 0x02
        else:
            while not os.path.exists(filename):
                time.sleep(0.001)
            self.file = open(filename, "r+b")
            self.active_code = 0x02
            self.wait_code = 0x01
        self.busy_code = 0x00
        self.map = mmap.mmap(self.file.fileno(), size)
        if create:
            self.map[0] = self.active_code

    def send_message(self, msg: gym_rlay_pb2.GymnasiumMessage):
        serialized_msg = msg.SerializeToString()
        msg_len = len(serialized_msg).to_bytes(4, byteorder="little")
        while self.map[0] != self.active_code:
            pass
        self.map[0] = self.busy_code
        self.map[1 : self.size] = b"\x00" * (self.size - 1)

        self.map[1:5] = msg_len
        self.map[5 : len(serialized_msg) + 5] = serialized_msg
        self.map[0] = self.wait_code

    def receive_message(self) -> gym_rlay_pb2.GymnasiumMessage | None:
        while self.map[0] != self.active_code:
            pass
        msg_len = int.from_bytes(self.map[1:5], byteorder="little")
        serialized_msg = bytes(self.map[5 : 5 + msg_len])
        msg = gym_rlay_pb2.GymnasiumMessage()
        msg.ParseFromString(serialized_msg)
        return msg

    def close(self):
        self.file.close()
        os.remove(f"/tmp/{self.name}")


def create_gymnasium_message(
    step_return: tuple[np.ndarray, float, bool, bool, dict[str, Any]] | None = None,
    reset_return: tuple[np.ndarray, dict[str, Any]] | None = None,
    reset_args: tuple[int, dict[str, Any]] | None = None,
    action: np.ndarray | None = None,
    close: bool | None = None,
) -> GymnasiumMessage:
    message = GymnasiumMessage()

    if step_return is not None:
        obs, reward, terminated, truncated, info = step_return
        obs_data = encode(obs)
        info = wrap_dict(info)

        step_return = StepReturn(
            obs=obs_data,
            reward=reward,
            terminated=terminated,
            truncated=truncated,
            info=info,
        )
        message.step_return.CopyFrom(step_return)

    elif reset_return is not None:
        obs, info = reset_return

        reset_return_ = StepReturn(
            obs=encode(obs),
            reward=0,
            terminated=False,
            truncated=False,
            info=wrap_dict(info),
        )

        message.step_return.CopyFrom(reset_return_)

    elif reset_args is not None:
        seed, options = reset_args
        reset_args = ResetArgs(seed=seed, options=wrap_dict(options))

        message.reset_args.CopyFrom(reset_args)

    elif action is not None:
        action_data = encode(action)

        message.action.CopyFrom(action_data)

    elif close is not None:
        message.close = close

    else:
        raise ValueError("No valid keyword arguments provided.")

    return message
