#!/bin/bash

# Help function
function printHelp {
    printf "Typical usage: /bin/bash install_webserver.sh\n"
    printf "OPTIONS:\n"
    printf "  -h : Print help\n"
    printf "  -f : Fresh install\n"
    printf "  -s : Only install webserver files\n"
}

# Exit on the first error
set -e

# Verify the user is running as root or sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or sudo."
    exit 1
fi

# Read the command line args
while getopts 'hfs' option; do
    case "${option}" in
        h) printHelp; exit 0 ;;
        f) FRESH_INSTALLATION=true ;;
        s) FRESH_INSTALLATION=false ;;
    esac
done
if [ -z "$FRESH_INSTALLATION" ]; then
    printf  "ERROR!: The installer must be called with either the -f or -s flag.\n"
    printHelp
    exit 1;
fi

# Potentially skip installing packages
if [ "$FRESH_INSTALLATION" = true ]; then
    # Install Apache2
    printf "Installing Apache2.."
    apt-get install apache2 -y 2>&1 > /dev/null
    printf ".Done!\n"

    # Install PHP
    printf "Installing PHP.."
    apt-get install php -y 2>&1 > /dev/null
    printf ".Done!\n"

    # Install MySQL and PHP-MySQL
    printf "Installing MySQL and PHP-MySQL.."
    apt-get install mariadb-server php-mysql -y 2>&1 > /dev/null
    service apache2 restart 2>&1 > /dev/null
    printf ".Done!\n"

    # Run Secure Installation for MySQL
    printf "Running secure installation for MySQL..\n"
    mysql_secure_installation
    printf ".Done!\n"

    # Enable PHP MySQLi extension
    printf "Enabling MySQLi PHP extension.."
    phpenmod mysqli 2>&1 > /dev/null
    service apache2 restart 2>&1 > /dev/null
    printf ".Done!\n"
fi

# Copy over the files in this directory to /var/www/html
printf "Copying webserver files into /var/www/html.."
rm -rf /var/www/html/*
cp -r * /var/www/html
printf ".Done!\n"

# Clean up extra files
printf "Cleaning Up.."
rm -rf /var/www/html/install_webserver.sh
printf ".Done!\n"

printf "Webserver Installation complete!\n"

