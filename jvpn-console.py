#!/usr/bin/env python
import requests
import subprocess
import os
import getpass

# configuration
HOST = "remote.macys.net"

## prepare required variables
# remote url for auth (login and logout)
LOGIN_URL = "https://{}/dana-na/auth/url_12/login.cgi".format(HOST)
LOGOUT_URL = "https://{}/dana-na/auth/logout.cgi".format(HOST)
VERIFY_CERT = False  # my company use self signed cert.

# ncui location
PROG = os.path.expanduser("~/.juniper_networks/network_connect/ncui")
# cert location
CERT_FILE = os.path.expanduser("~/remote.macys.net.net_ssl.crt")


def get_cred():
    """Get credentials from user.

    :return: (username, lan_password, pin_rsa)"""

    # get auth info from user
    username = raw_input('input username: ')
    lan_password = getpass.getpass(prompt='input password: ')
    pin_rsa = getpass.getpass(prompt='input pin and rsa key: ')

    return (username, lan_password, pin_rsa)


def auth():
    """Authenticate user.

    :return: session."""

    # params required for auth
    #TODO: automate tz_offset calculation
    tz_offset = "240"  # this works in Moscow/GMT+4 timezone
    realm = "FDS Mac Users"

    # get data from user
    username, lan_password, pin_rsa = get_cred()

    auth_data = {
        'username': username,
        'password': lan_password,
        'password#2': pin_rsa,
        'realm': realm,
        'tz_offset': tz_offset
    }

    # send auth request to get DSID cookie
    session = requests.Session()
    session.post(LOGIN_URL, data=auth_data, verify=VERIFY_CERT)

    return session


def logout(session):
    """Logout from session.

    :param session: session to log out from"""

    print("logging out")
    session.get(LOGOUT_URL, verify=VERIFY_CERT)


def get_dsid(session):
    """Get dsid from session.

    :param session: session to get DSID cookie.
    :return: dsid."""

    return session.cookies['DSID']


def start_vpn(dsid):
    """Start vpn channel.

    :param dsid: DSID cookie from session,
    :return: exit code of ncui execution."""

    # construct command line
    pass_opt = "-p ''"  # required for not asking password
    command = "{prog} -h {host} -c DSID={dsid} -f {cert_file} {pwd}".format(
        prog=PROG,
        host=HOST,
        dsid=dsid,
        cert_file=CERT_FILE,
        pwd=pass_opt)

    # execute ncui to create tunnel
    exit_code = subprocess.call(command, shell=True)
    return exit_code


# authenticate client
session = auth()

# get dsid
dsid = get_dsid(session)

# start vpn and logout at the end
try:
    start_vpn(dsid)
except Exception as exception:
    print("something wrong happened executing ncui")
    print exception
finally:
    # logout at the end to avoid problems on next login.
    logout(session)