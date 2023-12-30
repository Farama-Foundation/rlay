# RLay

RLay (pronounced like "relay") is a tool that enables building [Gymnasium](https://github.com/Farama-Foundation/Gymnasium) environments with ~any language or software toolkit.

The main inspiration is interfacing with games built in powerful engines like Unity and Unreal.
Adding a client or a server in the environment code will expose it for interaction with the standard
Gymnasium API.

There are two possible paradigms -- the environment runs either as a server, or as a client.

ClientEnv has a relatively intuitive interpretation. The server maintains an instance of the environment,
and calls its methods according to the MemServer calls. The user (or the RL algorithm) calls the methods of `ClientEnv`,
which in turn calls the MemServer methods on the server.

ServerEnv works the other way around. It expects that the user creates a server which implements a policy,
and the environment lives in a client which can query that policy. When the client queries the server, it sends an observation,
and receives the following observation.


In summary, in ClientEnv:
- The underlying environment logic lives on the server
- The `Env` instance exists in the client
- The algorithmic logic is in the client

In ServerEnv:
- The underlying environment logic is in the client
- The `Env` instance exists on the server
- The algorithmic logic is on the server


The `ServerEnv` implementation is inspired by ML-Agents, but we generally recommend using `ClientEnv`.

## Protocol

ClientBackend - ServerEnv:
- Handshake -- server sends a message, client sends a message
- Server sends a message to hand over control
# TODO: finish this
