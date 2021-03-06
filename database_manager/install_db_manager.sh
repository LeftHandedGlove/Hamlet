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

echo "Installing the Hamlet Database Manager."

# Create install dir
echo "Creating the installation directory"
INSTALL_DIR="/opt/hamlet/database-manager"
rm -rf $INSTALL_DIR
mkdir -p $INSTALL_DIR

# Copy files into install directory
echo "Copying files into the installation directory"
cd $REPO_DIR
cp -r * $INSTALL_DIR

# Register the service
echo "Registering the hamlet_db_manager service"
cd $INSTALL_DIR
systemctl daemon-reload
systemctl stop hamlet_db_manager > /dev/null || exit 0
systemctl disable hamlet_db_manager > /dev/null || exit 0
cp hamlet_db_manager.service /etc/systemd/system
systemctl start hamlet_db_manager > /dev/null
systemctl enable hamlet_db_manager > /dev/null
systemctl daemon-reload

echo "Installation Complete!"
