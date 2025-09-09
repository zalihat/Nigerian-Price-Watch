#!/bin/bash
set -e

# Clean up old builds
rm -rf package build.zip

# Install dependencies to package/
pip install --platform manylinux2014_x86_64 --only-binary=:all: --target ./package -r requirements.txt

# Zip dependencies
cd package
zip -r9 ../build.zip .
cd ..

# Add your lambda function files
zip -g build.zip lambda_function.py clean_data.py

echo "✅ build.zip created successfully!"
