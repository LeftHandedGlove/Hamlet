#!/bin/bash

# Fail quickly to prevent issues
set -e

# Useful variables
DATE=$(date +'%h-%d-%Y_%H-%M-%S')
# Get the location of this install script, it should be the top level of the code directory
REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Run as sudo
if [ $EUID -ne 0 ]; then
    echo "Must run as sudo"
    exit 1
fi

echo "Installing the Hamlet Sensors Monitor."

# Create install dir
echo "Creating the installation directory"
INSTALL_DIR="/opt/hamlet/sensors_monitor"
rm -rf $INSTALL_DIR
mkdir -p $INSTALL_DIR

# Copy files into install directory
echo "Copying files into the installation directory"
cd $REPO_DIR
cp -r * $INSTALL_DIR

# Register the service
echo "Registering the hamlet_sensors_monitor service"
cd $INSTALL_DIR
systemctl daemon-reload
systemctl stop hamlet_sensors_monitor > /dev/null || exit 0
systemctl disable hamlet_sensors_monitor > /dev/null || exit 0
cp hamlet_sensors_monitor.service /etc/systemd/system
systemctl start hamlet_sensors_monitor > /dev/null
systemctl enable hamlet_sensors_monitor > /dev/null
systemctl daemon-reload

echo "Installation Complete!"
