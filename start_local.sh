#! /bin/bash

# poetry export -f requirements.txt --output requirements.txt --without-hashes
# cp requirements.txt src/addrgen/requirements.txt
# cp requirements.txt src/cleansing/requirements.txt
# mv requirements.txt src/auth/requirements.txt

# # poetry run python prepare_sam_template.py
# # poetry run sam build --use-container
# # poetry run sam local start-api

# # rm src/addrgen/requirements.txt
# # rm src/cleansing/requirements.txt
# # rm src/auth/requirements.txt
# # rm ./template.yaml

# SAM is conflict to devcontainer, two options: 1. move all testing to AWS, 2. Use localstack to mock AWS environment