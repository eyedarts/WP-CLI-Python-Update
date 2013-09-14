WP-CLI-Python-Update
====================

Update multiple local and remote instances of WordPress using WP-CLI, Python, and Fabric.

Install Fabric
--------------

```
$ virtualenv --no-site-packages [directory for script]
$ cd [directory for script]
$ source bin/activate
(directory for script)$ pip install fabric
```


Edit hosts in wp_sites_local.txt
-------------------------------
For hosts on your local machine, add lines like these to this file:

```
/home/user/path/to/WordPress/instance
/home/user/path/to/WordPress/instance2
/home/user/path/to/WordPress/instance3
```

Edit hosts in ssh_sites.txt
--------------------------
For hosts on a remote machine, add lines like these to this file:

```
user@domain.com,/home/user/path/to/WordPress/instance
user@domain2.com,/home/user/path/to/WordPress/instance2
user@domain3.com,/home/user/path/to/WordPress/instance3
```

Run the Script
--------------

```
(directory for script)$ python wp_update.py
```
You will be asked to enter passwords where they're needed.
