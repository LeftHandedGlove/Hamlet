cd /home/hamlet/

apt update
apt upgrade

apt install cmake build-essential pkg-config git
apt install libjpeg-dev libtiff-dev ilbjasper-dev libpng-dev libwebp-dev libopenexr-dev
apt install livavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394-22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
apt install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
apt install libatlas-base-dev liblapacke-dev gfortran
apt install libhdf5-dev libhdf5-103
apt install python3-dev python3-pip python3-numpy

sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
systemctl restart dphys-swapfile.service

git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git

cd opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=/home/hamlet/opencv_contrib/modules \
      -D ENABLE_NEON=ON \
      -D ENABLE_VFPV3=ON \
      -D BUILD_TESTS=OFF \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
      -D BUILD_EXAMPLES=OFF ..
make -j 3
make install
ldconfig

sed -i 's/CONF_SWAPSIZE=2048/CONF_SWAPSIZE=100/' /etc/dphys-swapfile
systemctl restart dphys-swapfile.service
