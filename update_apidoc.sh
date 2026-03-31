#! /bin/bash

source .env

# TODO: add api gateway endpoint id to the openapi.yaml URL

npx @scalar/cli auth login --token $SCALAR_AUTH
npx @scalar/cli registry publish ./swagger/openapi.yaml --namespace pilotworks --private --force

echo "https://registry.scalar.com/@pilotworks/apis/address-cleansing-demo"
