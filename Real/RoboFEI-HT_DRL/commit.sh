#!/bin/bash

LightBlue='\e[1;34m'
LightRed='\e[1;31m'
NC='\e[0m' # No Color
#font colors:
#Black				0;30		Dark Gray			1;30
#Blue					0;34		Light Blue		1;34
#Green				0;32		Light Green		1;32
#Cyan					0;36		Light Cyan		1;36
#Red					0;31		Light Red			1;31
#Purple				0;35		Light Purple	1;35
#Brown/Orange	0;33		Yellow				1;33
#Light Gray		0;37		White					1;37

clear
git config --global --unset-all user.name
git config --global --unset-all user.email

git config --unset-all user.name
git config --unset-all user.email

echo -e "${LightBlue}Insira seu nome: ${NC}"
read name

echo -e "${LightBlue}Insira seu email do git: ${NC}"
read email

git config --global user.name "${name}"
git config --global user.email "${email}"

git cola
git reset --hard
echo -e "${LightRed}Certifique se está conectado a internet e logado, precione enter para continuar${NC}"
read a

git pull -f --all
echo -e "${LightRed}Certifique se foi realizado corretamente o pull, precione enter para continuar${NC}"
read a

git push -f --all
echo -e "${LightRed}Certifique se foi realizado corretamente o push, precione enter para continuar${NC}"
read a

git config --global --unset-all user.name
git config --global --unset-all user.email
