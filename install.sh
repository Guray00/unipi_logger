#installing dependecies
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'     # No Color

function print_exit(){
  	echo "";
	echo "";
	printf "Not installing, ${RED}aborting${NC}. Nothing has been changed.";
	echo "Thanks for choosing us.";
	echo "";
}

function something_went_wrong(){
	echo ""
	echo ""
	printf "\n\n${RED}Something went wrong during the installation process. Nothing has been changed, aborting.${NC}"
    echo ""
}

function print_logo(){
  user=$(whoami)
  dir="/home/$user/.unipi_logger"

  echo ""
  echo ""
  printf "${YELLOW}===================================================${NC}\n"
  printf "${YELLOW}  __  __     _      _   __                         ${NC}\n"
  printf "${YELLOW} / / / /__  (_)__  (_) / /  ___  ___ ____ ____ ____${NC}\n"
  printf "${YELLOW}"
  printf '/ /_/ / _ \/ / _ \/ / / /__/ _ \/ _ `/ _ `/ -_) __/'
  printf "${NC}\n"
  printf "${YELLOW}\____/_//_/_/ .__/_/ /____/\___/\_, /\_, /\__/_/   ${NC}\n"
  printf "${YELLOW}           /_/                 /___//___/          ${NC}\n"
  printf "${YELLOW}===================================================${NC}\n"
  echo ""
  echo ""
  printf "Welcome to Unipi Logger installer! An ${YELLOW}utomatic installer${NC} to automate the login form for Unipi's Residences.\n"
  echo "You are installing for user \"$user\" in \"$dir\""
  read -p "Continue with the installation?[y/n] " clone
}


# ============================
# 	START HERE
# ============================
clear
print_logo

user=$(whoami)
dir="/home/$user/.unipi_logger"

if [[ $clone == "y" ]]; then
  	echo "Installing dependencies (python, pip, chromium, git, chromedriver)..."

	if sudo apt-get -qq install python git chromium-browser chromium-chromedriver python-pip -y; then
		printf "\n\n${GREEN}Dependecies installed correctly${NC}\n"
	
	else
		echo ""
		echo ""
		
		printf "${RED}Error with python-pip${NC}. Trying with python3-pip...\n"
		if sudo apt-get -qq install python git chromium-browser chromium-chromedriver python3-pip -y; then
			printf "${GREEN}Dependecies installed correctly${NC}\n"
		else
			something_went_wrong
			exit
		fi
	
		#exit
	fi


  
  echo "Cloning repository in \"$dir\""
  if [[ -d "$dir" ]]; then
    printf "\nThis software is ${GREEN}already installed${NC}, if you continue the folder will be deleted and installed again\n"
	read -p "Do you wanna reinstall?[y/n] " reinstall
	echo ""
	
	if [[ $reinstall == "y" ]]; then
	    sudo rm -R $dir
	else
	    print_exit
        exit
	fi
  fi  
  
  #cloning dir
  cd /home/$user
  git clone https://github.com/Guray00/unipi_logger
  
  # installing python deps
  echo "Installing python dependecies..."
  cd $dir
  if pip install -r requirements.txt; then
	printf "\n\n${GREEN}Python dependecies installed correctly${NC}\n\n"
	# >/dev/null
  else
	if pip install -r requirements.txt --use-feature=2020-resolver; then
		printf "\n\n${GREEN}Python dependecies installed correctly${NC}\n\n"
	else 
		something_went_wrong
		exit
	fi
  fi
# don't want to install  
else
  print_exit
  exit
fi