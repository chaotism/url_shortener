Small project for implementing TinyUrl shortener. Written with fast-api and ddd paradigma.


# Run from root folder
docker-compose  -f docker/docker-compose-dev.yml up

# Template.
This project based on `https://github.com/chaotism/fastapi-purser/`

# Additional docs here
`docs/index.md`

# Plans
## Close plans
add supporting redis as db
add cache for get requests
add mypy to git-commit hooks (need fix issues)
migrate to python 3.11
fix TODOS

## Future Plans
add supporting sql databases
add bloom filter for short url keys
migrate to redirects
