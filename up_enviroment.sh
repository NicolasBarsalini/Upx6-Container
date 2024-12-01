#!/bin/bash

echo "Ennabling ENVIROMENT..."
cd ~/venv_para_podman_compose/
source venv/bin/activate

cd ~/zenohd_pu/
podman-compose up -d
echo "Enviroment ennabled..."
