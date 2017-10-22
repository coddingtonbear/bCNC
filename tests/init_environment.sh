#!/usr/bin/env bash
set -x
set -e

MAIN_DIR=$(pwd)

echo "Installing GRBL Simulator"
# GRBL 0.9; later versions are not supported by the simulator
git clone https://github.com/grbl/grbl.git
cd grbl/grbl
git checkout 3ce1a9d637f05e28462a36cb8b166386aab94afc

git clone https://github.com/grbl/grbl-sim.git
cd grbl-sim
git checkout ff1e887d1fd68cfa3dedc50d78ee928c8358d6ba
make new

echo "Starting GRBL Simulator at /tmp/ttyFAKE"
./simport.sh &
cd $MAIN_DIR

echo "Installing bCNC Requirements"
pip install imageio==2.2.0
pip install pyserial==3.4
cp tests/travis_bcnc_config.ini ~/.bCNC

echo "Installing Sikulix"
wget https://launchpad.net/sikuli/sikulix/1.1.1/+download/sikulixsetup-1.1.1.jar
java -jar sikulixsetup-1.1.1.jar options 1.1

echo "Installing Test Requirements"
pip install pyscreenshot==0.4.2
pip install pytest==3.2.3
