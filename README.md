# [Installing OpenCV](https://pimylifeup.com/raspberry-pi-opencv/)
1) Install the required libraries
	1) sudo apt update
	2) sudo apt upgrade
	3) sudo apt install cmake build-essential pkg-config git
	4) sudo apt install libjpeg-dev libtiff-dev ilbjasper-dev libpng-dev libwebp-dev libopenexr-dev
	5)  sudo apt install livavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394-22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
	6) sudo apt install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
	7) sudo apt install libatlas-base-dev liblapacke-dev gfortran
	8) sudo apt install libhdf5-dev libhdf5-103
	9) sudo apt install python3-dev python3-pip python3-numpy
2) Allow more memory in the swapfile
	1) Edit /etc/dphys-swapfile and update this line CONF_SWAPSIZE=100 to CONF_SWAPSIZE=2048
	2) sudo systemctl restart dphys-swapfile.service
3) Clone the OpenCV git repositories
	1) git clone https://github.com/opencv/opencv.git
	2) git clone https://github.com/opencv/opencv_contrib.git
4) Build the OpenCV source code
	1) cd opencv
	2) mkdir build
	3) cd build
	4) cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D ENABLE_NEON=ON -D ENABLE_VFPV3=ON -D BUILD_TESTS=OFF -D INSTALL_PYTHON_EXAMPLES=OFF -D OPENCV_ENABLE_NONFREE=ON -D CMAKE_SHARED_LINKER_FLAGS=-latomic -D BUILD_EXAMPLES=OFF ..
	5) make -j 3
	6) sudo make install
	7) sudo ldconfig
5) Return the swapfile to its original size
	1) Edit /etc/dphys-swapfile and update this line CONF_SWAPSIZE=2048 to CONF_SWAPSIZE=100
	2) sudo systemctl restart dphys-swapfile.service
