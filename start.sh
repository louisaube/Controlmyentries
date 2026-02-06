#!/bin/bash
cd frontend && npx vite build 2>&1 && cd ..
rm -rf static && cp -r frontend/dist static
python -m api.main
