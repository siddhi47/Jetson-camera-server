# export cuda variables 

export PATH=${PATH}:/usr/local/cuda/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64
source .bashrc

# setting up tensorflow
echo "#####################################################"
echo "SETTING UP TENSORFLOW"
sudo apt-get purge libreoffice* -y
sudo apt-get clean -y
sudo apt-get update && sudo apt-get upgrade -y
sudo apt install curl -y
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran -y
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python3
sudo apt-get -y install python3-pip cmake libpython3-dev python3-numpy

sudo pip3 install virtualenv virtualenvwrapper
echo "# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh" >> $HOME/.bashrc
source $HOME/.bashrc
mkvirtualenv tensorflow --python=python3
workon tensorflow
pip3 install -U --no-deps numpy==1.19.4 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig
H5PY_SETUP_REQUIRES=0 pip3 install -U --no-build-isolation h5py==3.1.0
pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 tensorflow

echo "TENSORFLOW SETUP COMPLETED"

echo "#####################################################"

if [ $BUILD_OPENCV = true ] ; then
    echo "#####################################################"
    echo "BUILDING OPENCV WITH GPU SUPPORT"
    sudo apt purge libopencv libopencv-dev libopencv-python libopencv-samples -y
    cd ~/git
    git clone https://github.com/mdegans/nano_build_opencv.git
    cd nano_build_opencv
    ./build_opencv.sh

    sudo cp /usr/local/lib/python3.6/dist-packages/cv2/python-3.6/cv2.cpython-36m-aarch64-linux-gnu.so /usr/lib/python3.6/lib-dynload
    echo "FINISHED BUILDING OPENCV WITH GPU SUPPORT"
    echo "#####################################################"
else
    pip3 install opencv-python~=4.4
fi

# Configuring TRT

echo "CONFIGURING JETSON-INFERENCE AND UTILS FOR TENSORFLOW TRT"
cd ~/git
git clone --recursive https://github.com/dusty-nv/jetson-inference.git
cd jetson-inference
mkdir build 
cd build
cmake ../ -DBUILD_INTERACTIVE:BOOL=NO
make
sudo make install
sudo ldconfig

cp /usr/lib/python3.6/dist-packages/jetson_inference_python.so ~/.virtualenvs/tensorflow/lib/python3.6/site-packages/jetson_inference_python.so
cp /usr/lib/python3.6/dist-packages/jetson_utils_python.so ~/.virtualenvs/tensorflow/lib/python3.6/site-packages/jetson_utils_python.so
cp -r /usr/lib/python3.6/dist-packages/jetson/ /home/siddhi/.virtualenvs/tensorflow/lib/python3.6/site-packages/jetson/
echo "FINISHED CONFIGURATION FOR JETSON INFERENCE AND UTILS"

echo "Copying the TRT libraries to tensorflow venv"
cp -r /usr/lib/python3.6/dist-packages/tensorrt/  /home/siddhi/.virtualenvs/tensorflow/lib/python3.6/site-packages/

echo "INSTALLING PYTHON DEPENDENCIES"
sudo apt-get install libgeos-dev -y
pip3 install bottle imutils matplotlib scipy pyyaml shapely waitress easydict tensorflow-hub decorator
echo "FINISHED INSTALLING PYTHON DEPENDENCIES"


echo "Setting up pycuda"
cd ~/git/mlpipeline/*/setup/
./install_pycuda.sh

echo "Copying pycuda to tensorflow venv"

cp -r /usr/local/lib/python3.6/dist-packages/pycuda-2019.1.2-py3.6-linux-aarch64.egg/pycuda/  /home/siddhi/.virtualenvs/tensorflow/lib/python3.6/site-packages/
echo "Installing yolo plugin"
cd ~/git/mlpipeline/*/plugins/
make
i
