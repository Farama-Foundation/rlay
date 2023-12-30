from __future__ import annotations

import gymnasium as gym

from rlay.core import Communicator, create_gymnasium_message
from rlay.gym_grpc import gym_rlay_pb2
from rlay.gym_grpc.gym_rlay_pb2 import GymnasiumMessage
from rlay.utils import decode, unwrap_dict, encode, wrap_dict


class ClientBackend:
    def __init__(self, env_id: str, port: int = 5005):
        self.env = gym.make(env_id)
        self.env.reset()

        # self.communicator = Communicator("rlay_client", "rlay_server", "rlay_lock", port=port, create=False)
        self.communicator = Communicator("rlay", create=False)

        self.communicator.send_message(gym_rlay_pb2.GymnasiumMessage(status=True))
        handshake = self.communicator.receive_message()  # handshake

        print(f"Backend client listening on port {port}")

    def run(self):
        # Optional setup code goes here

        # When setup is done, request a reset.

        self.communicator.send_message(gym_rlay_pb2.GymnasiumMessage(request=True))

        msg = self.communicator.receive_message()
        assert msg.HasField("reset_args"), "Environment must be reset before using."

        seed = msg.reset_args.seed if msg.reset_args.seed != -1 else None
        options = unwrap_dict(msg.reset_args.options)

        obs, info = self.env.reset(seed=seed, options=options)
        reward, terminated, truncated = 0.0, False, False

        while True:
            # Execute whatever logic. When we need a decision, send the current step return and get the decision
            msg = create_gymnasium_message(
                step_return=(obs, reward, terminated, truncated, info)
            )
            self.communicator.send_message(msg)  # 1
            response = self.communicator.receive_message()  # 2

            if response.HasField("action"):
                # If we got an action, execute it
                action = decode(response.action)
                if action.size == 1:
                    action = action[0]
                obs, reward, terminated, truncated, info = self.env.step(action)

            elif response.HasField("reset_args"):
                seed = (
                    response.reset_args.seed if response.reset_args.seed != -1 else None
                )
                options = unwrap_dict(response.reset_args.options)
                obs, info = self.env.reset(seed=seed, options=options)
                reward, terminated, truncated = 0.0, False, False

            elif response.HasField("close"):
                self.env.close()
                return
            elif response.HasField("status"):
                continue
            else:
                # Send a dummy message to request a decision
                raise ValueError("Received an invalid message")


class ServerBackend:
    def __init__(self, env_id: str, port: int = 50051, env_kwargs: dict = {}):
        self.env = gym.make(env_id, **env_kwargs)
        self.env.reset()

        self.communicator = Communicator("rlay", create=True)

        print("Waiting for handshake")
        self.communicator.send_message(gym_rlay_pb2.GymnasiumMessage(request=True))
        self.communicator.receive_message()  # handshake
        self.communicator.send_message(gym_rlay_pb2.GymnasiumMessage(request=True))

        print(f"Backend server listening on port {port}")

    def process_reset(self, msg: GymnasiumMessage):
        msg = msg.reset_args
        seed = msg.seed if msg.seed != -1 else None
        options = unwrap_dict(msg.options)
        obs, info = self.env.reset(seed=seed, options=options)
        response = create_gymnasium_message(reset_return=(obs, info))
        self.communicator.send_message(response)

    def process_close(self, msg: GymnasiumMessage):
        self.env.close()
        self.communicator.close()

    def process_step(self, msg: GymnasiumMessage):
        action = decode(msg.action)
        if action.size == 1:
            action = action[0]
        obs, reward, terminated, truncated, info = self.env.step(action)
        step_return = gym_rlay_pb2.StepReturn(
            obs=encode(obs),
            reward=reward,
            terminated=terminated,
            truncated=truncated,
            info=wrap_dict(info),
        )
        response = gym_rlay_pb2.GymnasiumMessage(step_return=step_return)
        self.communicator.send_message(response)

    def run(self):
        while True:
            msg = self.communicator.receive_message()

            if msg.HasField("action"):
                self.process_step(msg)
            elif msg.HasField("reset_args"):
                self.process_reset(msg)
            elif msg.HasField("close"):
                self.process_close(msg)
                break
