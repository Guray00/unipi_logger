#installing dependecies
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'     # No Color

function print_exit(){
	echo "";
	printf "Not installing, ${RED}aborting${NC}. Nothing has been changed.";
	echo "Thanks for choosing us.";
	echo "";
}

function something_went_wrong(){
	echo ""
	printf "\n\n${RED}Something went wrong during the installation process. Nothing has been changed, aborting.${NC}"
    echo ""
}

function program_is_working(){
	printf "\n${GREEN}Working${NC}, but if you were already logged could be a ${GREEN}false positive${NC}.\n"
	printf "If the script wont work in future, consider to ${GREEN}reinstall (safer)${NC} or change user and pw in the configuration\n\n"

	printf "\nYou should add to the crontab file (crontab -e) the line:\n\n"
	printf "*/2 * * * * python ~/.unipi_logger/logger.py -u $1 -pw $2 >/dev/null 2>&1\n\n"
}

function python_dependencies_installed(){
	printf "\n${GREEN}Python dependecies installed correctly${NC}\n"
}

function dependencies_installed(){
	printf "\n${GREEN}Dependecies installed correctly${NC}\n"
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
  echo ""
  printf "${YELLOW}===================================================${NC}\n"
  echo ""
  echo ""
  printf "Welcome to Unipi Logger installer! An ${YELLOW} installer${NC} to automate login form for Unipi's Residences.\n"
  echo "You are installing for user \"$user\" in \"$dir\""
  read -p "Continue with the installation?[y/n] " clone
}

function cron_check(){
	crontab -l | grep -q 'unipi_logger' && return true || return false
}

function script_check(){
	user=$(whoami)
  	dir="/home/$user/.unipi_logger"
	  
  	read -p "Insert your username (Alice): " usr
	read -p "Insert your password: " pw

	python $dir/logger.py -u $usr -pw $pw --log debug --force >/dev/null 2>&1
	ret=$?

	if [ $ret == 254 ]; then
		echo "Wrong input"
		script_check

	elif [ $ret == 1 ]; then
			python3 $dir/logger.py -u $usr -pw $pw --log debug --force
			ret=$?

			if [ $ret == 254 ]; then
			echo "Wrong input"
			script_check

			elif [ $ret -ne 0 ];then
				echo "Script not working"
				something_went_wrong

			else
				program_is_working $usr $pw
			fi


	elif [ $ret -ne 0 ];then
				echo "Script not working"
				something_went_wrong

	else
		program_is_working $usr $pw
	fi
}


function debian_deps(){
	if sudo apt-get -qq install python git chromium-browser chromium-chromedriver python-pip -y; then
		dependencies_installed
	
	else
		echo ""
		
		printf "${RED}Error with python-pip${NC}. Trying with python3-pip...\n"
		if sudo apt-get -qq install python git chromium-browser chromium-chromedriver python3-pip -y; then
			dependencies_installed
		else
			something_went_wrong
			exit
		fi
	
		#exit
	fi
}

function arch_deps(){
	if sudo pacman -Syu --quiet --noconfirm python git python-pip; then
		yay -Syu --noconfirm --quiet chromedriver
		dependencies_installed
	
	else
		echo ""
		
		printf "${RED}Error with python-pip${NC}. Trying with python3-pip...\n"
		if sudo pacman -Syu --quiet --noconfirm python git chromium-browser chromium-chromedriver python3-pip; then
			yay -Syu --noconfirm --quiet chromedriver
			dependencies_installed
		else
			something_went_wrong
			exit
		fi
	
		#exit
	fi
}

# ============================
# 	START HERE
# ============================

#probe os here
apt -v >>.log 2>&1
if [ $? -eq 0 ]
then
	DISTRO=DEBIAN
fi
pacman -V >>.log 2>&1
if [ $? -eq 0 ]
then
	DISTRO=ARCH
fi

echo "Detected system type: " $DISTRO

clear
print_logo

user=$(whoami)
dir="/home/$user/.unipi_logger"

if [[ $clone == "y" ]]; then
  	echo "Installing dependencies (python, pip, chromium, git, chromedriver)..."

	if [[ $DISTRO == "DEBIAN" ]]; then 
		debian_deps
	
	elif [[ $DISTRO == "ARCH" ]]; then 
		arch_deps
	

	else
		echo "NOT RECOGNIZED QUITTING"
		exit
	fi

	#cloning dir
	if ! git clone https://github.com/Guray00/unipi_logger $dir 2>/dev/null && [ -d "${dir}" ] ; then
		echo "Clone failed because the folder ${dir} exists, no problem."
	fi
	
	# installing python deps
	echo ""
	echo "Installing python dependecies..."
	cd $dir
	if pip install -r $dir/requirements.txt; then
		python_dependencies_installed

	else
		if pip install -r $dir/requirements.txt --use-feature=2020-resolver; then
			python_dependencies_installed
		
		else 
			something_went_wrong
			exit
		fi
  fi

  #checking if the script works
  script_check

  #cron check
  x=cron_check

# don't want to install  
else
  print_exit
  exit
fi
