from __future__ import annotations

import gymnasium as gym
import numpy as np

from rlay.core import Communicator, create_gymnasium_message
from rlay.gym_grpc import gym_rlay_pb2
from rlay.utils import wrap_dict, decode, unwrap_dict


class ServerEnv(gym.Env):
    def __init__(self, port: int = 5005):
        self.port = port
        self.communicator = Communicator("rlay", create=True)

        self.communicator.send_message(gym_rlay_pb2.GymnasiumMessage(status=True))
        handshake = self.communicator.receive_message()
        self.communicator.send_message(gym_rlay_pb2.GymnasiumMessage(status=True))


    def reset(self, seed=None, options=None):
        # print("Resetting environment")
        seed = seed if seed is not None else -1
        options = wrap_dict(options) if options else {}

        reset_args = create_gymnasium_message(reset_args=(seed, options))


        old_msg = self.communicator.receive_message()  # 1

        # obs = decode(msg.step_return.obs)
        # reward = msg.step_return.reward
        # terminated = msg.step_return.terminated
        # truncated = msg.step_return.truncated
        # info = unwrap_dict(msg.step_return.info)


        self.communicator.send_message(reset_args)  # 2

        msg = self.communicator.receive_message()  # 1
        obs = decode(msg.step_return.obs)
        info = unwrap_dict(msg.step_return.info)

        self.communicator.send_message(gym_rlay_pb2.GymnasiumMessage(status=True))  # 2

        return obs, info

    def step(self, action: np.ndarray | int):
        action_msg = create_gymnasium_message(action=action)

        msg = self.communicator.receive_message()  # 1

        obs = decode(msg.step_return.obs)
        reward = msg.step_return.reward
        terminated = msg.step_return.terminated
        truncated = msg.step_return.truncated
        info = unwrap_dict(msg.step_return.info)

        self.communicator.send_message(action_msg)  # 2

        return obs, reward, terminated, truncated, info

    def close(self):
        self.communicator.close()


class ClientEnv:  # (gym.Env)
    def __init__(self, port: int = 50051):
        self.port = port
        self.communicator = Communicator("rlay", create=False)


        self.communicator.receive_message()
        self.communicator.send_message(gym_rlay_pb2.GymnasiumMessage(status=True))
        self.communicator.receive_message()
        print(f"Environment starting on port {port}")



    def reset(self, seed=None, options=None):
        seed = seed if seed is not None else -1
        options = wrap_dict(options) if options else {}

        reset_msg = create_gymnasium_message(reset_args=(seed, options))
        self.communicator.send_message(reset_msg)


        response = self.communicator.receive_message()

        if response.HasField("step_return"):
            obs = decode(response.step_return.obs)
            info = unwrap_dict(response.step_return.info)
            return obs, info

    def step(self, action: np.ndarray | int):
        """Send an action to the server and receive a response."""
        if isinstance(action, int):
            action = np.array([action], dtype=int)
        action_msg = create_gymnasium_message(action=action)

        self.communicator.send_message(action_msg)
        response = self.communicator.receive_message()

        if response.HasField("step_return"):
            obs = decode(response.step_return.obs)
            reward = response.step_return.reward
            terminated = response.step_return.terminated
            truncated = response.step_return.truncated
            info = unwrap_dict(response.step_return.info)
            return obs, reward, terminated, truncated, info

    def close(self):
        close_msg = gym_rlay_pb2.GymnasiumMessage(close=True)
        self.communicator.send_message(close_msg)
