import os
import subprocess
import sys

import coloredlogs
import verboselogs
from colorama import Fore, Style
from openpyn import __basefilepath__, root

credentials_file_path = __basefilepath__ + "credentials"

logger = verboselogs.VerboseLogger(__name__)


def check_credentials():
    return os.path.exists(credentials_file_path)


def save_credentials():
    if root.verify_running_as_root() is False:
        logger.error("\nPlease run as 'sudo openpyn --init' the first time. \
Root access is needed to store credentials in " + "'" + credentials_file_path + "'" + ".")
        sys.exit()
    else:
        logger.verbose("Storing credentials in " + "'" + credentials_file_path + "'" + " with openvpn \
compatible 'auth-user-pass' file format")

        username = input("Enter your username for NordVPN, i.e youremail@yourmail.com: ")
        password = input("Enter the password for NordVPN: ")
        try:
            with open(credentials_file_path, 'w') as creds:
                creds.write(username + "\n")
                creds.write(password + "\n")
            creds.close()
            # Change file permission to 600
            subprocess.check_call(["sudo", "chmod", "600", credentials_file_path])

            logger.verbose("Awesome, the credentials have been saved in " + "'" + credentials_file_path + "'")
        except (IOError, OSError):
            logger.error("IOError while creating 'credentials' file.")
    return
