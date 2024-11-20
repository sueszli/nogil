usage:

```bash
# compile cpython
make docker-up # takes 20min
docker compose exec main python3 -c 'import sys; assert sys.version_info >= (3, 13); assert not sys._is_gil_enabled(); print("it works!")'

# get dependencies
docker compose exec main apt update
docker compose exec main apt install -y build-essential apt-utils curl libssl-dev openssl
docker compose exec main sh -c 'curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh'
docker compose exec main /root/.cargo/bin/cargo --version
docker compose exec main /root/.cargo/bin/cargo install --locked hyperfine
docker compose exec main /root/.cargo/bin/hyperfine --version

# wipe docker images
make docker-clean
```
