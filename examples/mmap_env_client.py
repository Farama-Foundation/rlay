from rlay import ClientBackend

def run_mmap_env_client():
    server = ClientBackend("CartPole-v1")
    server.run()

if __name__ == "__main__":

    run_mmap_env_client()
