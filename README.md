usage:

```bash
# exec into container
make docker-up # takes 20min
docker exec -it main bash
python3 -c 'import sys; assert sys.version_info >= (3, 13); assert not sys._is_gil_enabled(); print("it works!")'

# run tests

# wipe docker images
make docker-clean
```
