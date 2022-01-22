# mlops103-localgpuforgithubaction

## Pre-reqs:

1) First you need to Get out of following runtime env dependency hell... 
docker
nvidia drivers (sorry if you are on AMD RX GPUs as I'm not sure AMD's rocm has gone mainstream or not..)
nvidia-docker
nvidia-container-toolkit

you can test this out by running 
dpkg -l | grep -i nvidia (on ubuntu)
docker run --gpus all dvcorg/cml-py3 nvidia-smi

2) Start your self-hosted runner
docker run --name myrunner -d --gpus all iterativeai/cml:0-dvc2-base1-gpu  runner   --repo=$my_repo_url --token=$my_repo_token  --labels="local,runner"  --idle-timeout=1800
