#!/bin/bash

cd /home/nekoyoukan/projects/Home-plus || exit

code .

source .venv/bin/activate

streamlit run app.py