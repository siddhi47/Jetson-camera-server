sudo apt update
sudo apt upgrade -y

echo "Installing python 3.9"
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.9 -y

echo "Installing dependencies for python 3.9"
sudo apt-get install python3.9-distutils -y

echo "Installing additional python 3.9 dependencies"
sudo apt-get install python-dev python-pip python3-dev python3.9-dev python3-pip -y

echo "Installing Dependencies for dlib"
sudo apt-get install build-essential cmake -y
sudo apt install virtualenv -y

echo "Installing unzip"
sudo apt install unzip -y

echo "Installing dependencies for python-opencv"
sudo apt-get install libgl1

echo "Creating virtual environment using python 3.9"
virtualenv venv --python=python3.9
source venv/bin/activate


echo "Installing python requirements."
pip install -r requirements.txt
