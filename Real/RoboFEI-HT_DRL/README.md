[![Build Status](https://travis-ci.com/thiagohomem/RoboFEI-HT_Debug.svg?token=BM6ZpSsKHNz3RkbM8yxT&branch=master)](https://travis-ci.com/thiagohomem/RoboFEI-HT_Debug)
#RoboFEI-HT: Artificial Intelligence and Simulator

## AI: Deep Reinforcement Learning for Humanoid Robots



### Setup

1. compile the code of the robot running *./setup.sh*


### Setup

1. Once the AI is compiled, run *./start_simulator.sh* for running the simulator and the AI

### Run

Para executar o DRL e preciso executar o programa do controle de da pasta *AI/build/Control*:

./control


E preciso executar o programa que le a camera e salva a imagem na memoria compartilhada dentro da pasta *AI/DRL*:

python readCam.py


E executar o programa que executa a rede ja treinada dentro da pasta *AI/DRL/examples:

python duel_dqn_goalkeeper.py


Para visualizar a imagem da camera sera necessario executar o *readCam.py* pelo ssh

ssh -X fei@192.168.1.102

## OS and dependencies for AI and Simulator

This program was tested in Ubuntu 14.04 LTS 64 bits

* Main Dependencies:
    * cmake
    * g++
    * python 2.7 
    * python-pygame
    * python-numpy
    * python-opencv
    * screen

## Communication dependency
Install Construct:

sudo pip install construct==2.5.3
    
## License

GNU GENERAL PUBLIC LICENSE.
Version 3, 29 June 2007
   
