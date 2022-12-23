#!/bin/bash

# TODO : Deal with selection of languages

default_env_user_name="your_username"
default_env_password="your_password"
default_env_url="https://themis.housing.rug.nl/course/rest_of_url"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

function createEnv() {
	echo "Please add your details to the .env file or provide them as command line arguments"
	echo "A .env file has been created, make sure to fill in the details or provide them as command line arguments"
	# create .env file
	echo "USER_NAME_ENV=$default_env_user_name" > .env
	echo "PASSWORD_ENV=$default_env_password" >> .env
	echo "URL_ENV=$default_env_url">> .env
	echo "### !! dont edit below this line, unless you know what you are doing !! ###" >> .env
	echo "FILES_ENV=files" >> .env
	echo "its contents"
	echo "====="
	cat .env
	echo "====="
	exit 1
}

FILES=""
while test $# -gt 0; do
	case "$1" in
		-h|--help)
		echo "Usage: submit [options] [files]"
		echo "Note that all options can also be taken from environment variables."
		echo "Options passed as arguments take precedence over environment variables and **overwrite** them."
		echo "To do that either provide the flag : --create-env or  create a .env file with your details. These details will be used to login to the website, this way you don't have to pass cmd arguments all the time."
		echo "Options:"
		echo "  --create-env				Create a .env file with your details"
		echo "  -l, --url,  --URL			Url / link to submit to"
		echo "  -u, --user, --username		User name"
		echo "  -p, --pass, --password		Password"
		echo "  -h, --help				Display this help message"
		echo "  -v, --version				Display version information"
		exit 0
		;;
		--version)
		echo "Peristeri 2.0"
		echo "see for version 1 https://github.com/Stylo2k/Perist-ri"
		exit 0
		;;
		-l|--url|--URL)
		shift # to skip to the argument aka value of the flag
		URL=$1
		shift
		;;
		-u|--user|--username)
		shift
		USER_NAME=$1
		shift
		;;
		-p|--password|--pass)
		shift
		PASSWORD=$1
		shift
		;;
		--create-env)
		createEnv
		exit 0
		;;
		*)
		FILES="$FILES -F files[]=@$1"
		shift
	esac
done

# check if .env exists
if [ ! -f .env ]; then
	createEnv
fi

{
	source .env
} || {
	printf "\n${RED}Error: .env file is not valid, only command line arguments will be taken into account\n${NC}\n"
}

if [ -z "$USER_NAME" ]; then
	if [ -z "$USER_NAME_ENV" ] || [ "$USER_NAME_ENV" == "$default_env_user_name" ]; then
		echo ""
		echo "Please add your username to the .env file"
		echo "Or use the -u, --user, --USER flag"
		echo ""
		exit 1
	else
		USER_NAME=$USER_NAME_ENV
	fi
elif [ -n "$USER_NAME" ]; then
	echo "USER_NAME_ENV=$USER_NAME" > .env
fi


echo "Continuing as: $USER_NAME"

if [ -z "$PASSWORD" ]; then
	if [ -z "$PASSWORD_ENV" ] || [ "$PASSWORD_ENV" == "$default_env_password" ]; then
		echo ""
		echo "Please add your password to the .env file"
		echo "Or use the -p, --password, --PASSWORD flag"
		echo ""
		exit 1
	else
		PASSWORD=$PASSWORD_ENV
	fi
elif [ -n "$PASSWORD" ]; then
	echo "PASSWORD_ENV=$PASSWORD_ENV" >> .env
fi


if [ -z "$URL" ]; then
	if [ -z "$URL_ENV" ] || [ "$URL_ENV" == "$default_env_url" ]; then
		echo ""
		echo "Please add your url to the .env file"
		echo "Or use the -l, --url, --URL flag"
		echo ""
		exit 1
	else
		URL=$URL_ENV
	fi
elif [ -n "$URL" ]; then
	echo "URL_ENV=$URL_ENV" >> .env
fi

if [ -z "$FILES" ] || [ "$FILES" == "" ]; then
	if [ -z "$FILES_ENV" ] || [ "$FILES_ENV" == "" ]; then
		echo ""
		echo "Please add files to submit e.g. main.c"
		echo ""	
		exit 1
	else
		FILES=$FILES_ENV
	fi
elif [ -n "$FILES" ]; then
	echo "FILES_ENV=\"$FILES\"" >> .env
fi


BASE_URL="https://themis.housing.rug.nl"
# BASE_URL="https://127.0.0.1:8443"

SUBMIT_URL="$URL"

USER_AGENT="Mohammad Al Shakoush, Bash's script (new peresteri)"

COOKIE_FILE=".cookie"

LOGIN_EP="/log/in"

LOGIN="$BASE_URL$LOGIN_EP"

FLAGS="-sk --user-agent \"$USER_AGENT\""

LOGGED_IN=0


function isLoggedIn(){
	# try and do a get request to the login page
	# if it returns 302 then we are logged in
	# if it returns 200 then we are not logged in
	res=$(curl $FLAGS -b $COOKIE_FILE -I $BASE_URL | grep -E "302")

	if [ $? -eq 0 ]; then
		LOGGED_IN=1
	else
		LOGGED_IN=0
	fi
}

function extractCSRF(){
	local flag="-c"
	
	if [ $LOGGED_IN -eq 1 ]; then
		flag="-b"
	fi

	_csrf=$(curl $FLAGS $flag $COOKIE_FILE $1 | grep -E "value=\"(.{10,})\"" | cut -d \" -f6)
	echo $_csrf
}


function login(){
	if [ $LOGGED_IN -eq 1 ]; then
		return
	fi
	curl $FLAGS -b $COOKIE_FILE -X POST -d "_csrf=$1" -d "user=$USER_NAME" -d "password=$PASSWORD" $LOGIN 1> /dev/null
}

function submit(){
	action=$(curl $FLAGS -b $COOKIE_FILE $SUBMIT_URL | grep -E "action=\"(.{10,})\"" | cut -d \" -f2)
	
	redirect=$(curl $FLAGS -b $COOKIE_FILE -X POST $BASE_URL$action $FILES | cut -d ' ' -f4)

	judgeUrl=$(echo $redirect | sed 's/submission/judge/')

	submissionPage=$(curl $FLAGS -b $COOKIE_FILE -X POST "$BASE_URL$judgeUrl" -d "_csrf=$_csrf"| cut -d ' ' -f4)

	printf "\n${GREEN}You can view your submission at $BASE_URL$submissionPage\n${NC}"
}

isLoggedIn $@

# extract csrf from the login page
_csrf=$(extractCSRF $LOGIN)

# login with the extracted csrf
login $_csrf

echo "Submitting to $SUBMIT_URL"

submit
