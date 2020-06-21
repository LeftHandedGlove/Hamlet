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

printf "Installing the Hamlet Database Manager.\n"

# Create install dir
printf "Creating the installation directory.."
INSTALL_DIR="/opt/hamlet/database-manager"
rm -rf $INSTALL_DIR
mkdir -p $INSTALL_DIR
printf ".Done!\n"

# Copy files into install directory
printf "Copying files into the installation directory.."
cd $REPO_DIR
cp -r * $INSTALL_DIR
printf ".Done!\n"

# Register the service
printf "Registering the hamlet-db-manager service.."
cd $INSTALL_DIR
systemctl stop hamlet-db-manager 2>&1 /dev/null || exit 0
systemctl disable hamlet-db-manager 2>&1 /dev/null || exit 0
cp hamlet-db-manager.service /etc/systemd/system
systemctl start hamlet-db-manager 2>&1 /dev/null
systemctl enable hamlet-db-manager 2>&1 /dev/null
printf ".Done!\n"

printf "Installation Complete!\n"
