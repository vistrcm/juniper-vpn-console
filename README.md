juniper-vpn-console
===================

juniper-vpn-console is a simple script created to provide ability to start juniper vpn client without starting browser.

For now this script can be used only if two form auth enabled (username+password together with PIN+SecureID).

Requirements
------------

Before executing this script, you'll need to convert the ncui.so library into an executable and obtain the SSL certificate from your login webpage following the instructions on ["Juniper VPN, 64-bit Linux .. an unsolved mystery?"](http://makefile.com/.plan/2009/10/juniper-vpn-64-bit-linux-an-unsolved-mystery/).

Thanks to [Scott](http://makefile.com/.plan/author/Scott/) for this post. And for Ivan Onushkin who found this post.

Also [requests](http://docs.python-requests.org/en/latest/) python lib required for this script.


Usage
-----

Just start script

```
$ python jvpn-console.py
```

Enter username, password and PIN+SecureID.

If you don't want to enter username and password every time you can create ~/.jvpn-consolerc file

```
[hostname]
username = username
password = pass
pin = 12345
```

and you will be asked only for rsa key.
