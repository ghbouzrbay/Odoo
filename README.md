# How to Install Odoo 16 on Ubuntu 22.04

Odoo is a suite of open source Business applications. It was formerly known as OpenERP, and it offers so many modules to use, like Point of Sale (POS), Inventory, CRM, Website, Live Chat, e-Commerce, Billing, Accounting, Warehouse, etc. Odoo 16 was released on October 12, 2022. The performance of Odoo 16 is amazing; it is much faster than Odoo 15, which is already fast. These are some of the improved features in Odoo 16:

Opening an invoice is 3.7 times faster.
There are 2.4 times fewer SQL queries.
eCommerce pages load 3.9 times faster.
Reduced the number of HTTP requests, hence the lower latency
The features do not end here. The developers at Odoo are still planning on offering new features in the future. This tutorial will show you how to install Odoo 16 on Ubuntu 22.04.


## Table of Contents
Prerequisites

+ Step 1. Update The System
+ Step 2. Add System User
+ Step 3. Install Dependencies
+ Step 4. Install PostgreSQL
+ Step 5. Install Wkhtmltopdf
+ Step 6. Install Odoo
+ Step 7. Create Odoo Systemd Unit file
+ Step 8. Configure Reverse Proxy


## Prerequisites

+ An Ubuntu 22.04 VPS.
+ At least 2GB of RAM.
+ SSH root access or a system user with sudo privileges

### Step 1. Update The System
First of all, let us log in to our Ubuntu 22.04 VPS through SSH:

```
ssh master@IP_Address -p Port_number
```

Replace “master” with a user that has sudo privileges or root if necessary. Additionally, replace “IP_Address” and “Port_Number” with your server’s IP address and SSH port number. Next, let’s make sure that we’re on Ubuntu 22.04. You can verify it with this command:

```
$ lsb_release -a
```

You should get an output like this:

```
No LSB modules are available.
Distributor ID: Ubuntu
Description: Ubuntu 22.04.1 LTS
Release: 22.04
Codename: jammy
```

Then, execute this command below to make sure that all installed packages on the server are updated to their latest available versions:

```
$ sudo apt update
```

### Step 2. Add System User

We will install an Odoo 16 instance under a system user account. So, we need to create a new system account. This command below is used to create a user called “odoo16”.

```
$ sudo useradd -m -d /opt/odoo16 -U -r -s /bin/bash odoo16
```

### Step 3. Install Dependencies

Since Odoo is built on Python, we need to install some dependencies to proceed with installing Odoo 16 on our Ubuntu 22.04 system. We can install them by running this command below.

```
$ sudo apt install build-essential wget git python3-pip python3-dev python3-venv python3-wheel libfreetype6-dev libxml2-dev libzip-dev libsasl2-dev python3-setuptools libjpeg-dev zlib1g-dev libpq-dev libxslt1-dev libldap2-dev libtiff5-dev libopenjp2-7-dev
```

### Step 4. Install PostgreSQL

Odoo only supports PostgreSQL to store its data. Let’s execute the command below to install the PostgreSQL server on our Ubuntu 22.04 server.

```
$ sudo apt install postgresql
```

After the installation is finished, we can add a new postgresql user for our Odoo 16; run this command:

```
$ sudo su - postgres -c "createuser -s odoo16"
```

### Step 5. Install Wkhtmltopdf

For printing-related purposes, Odoo 16 requires a wkhtmltopdf version higher than 0.12.2. Wkhtmltopdf is an open-source command line tool to render HTML data into PDF format using Qt webkit. To install wkhtmltopdf on your Ubuntu 22.04 server, follow the steps below.

```
$ sudo apt install wkhtmltopdf
```

Once installed, you can check its version by running this command

```
$ wkhtmltopdf --version
```

You will see an output like this:

wkhtmltopdf 0.12.6

### Step 6. Install Odoo

In Ubuntu 22.04, we can install Odoo from the default Ubuntu repository, but this will install Odoo version 14. In this article, we will install Odoo 16 under a python virtual environment. We created a system user earlier in this article; let’s switch to system user ‘odoo16’ and then install Odoo under that username.

```
$ sudo su - odoo16
```

The command above should bring you to /opt/odoo16 and log you in as user ‘odoo16’. Now, download Odoo from Github.

```
$ git clone https://www.github.com/odoo/odoo --depth 1 --branch 16.0 odoo16
```  
OR 
```
$ git clone https://github.com/ghbouzrbay/Odoo/odoo16
```

Execute the following command to create a new python virtual environment.

```
$ python3 -m venv odoo16-venv
```

The virtual environment is now installed; it is time to activate it by running this command.

```
$ source odoo16-venv/bin/activate
```

Once executed, your shell prompt would look like this:

```(odoo16-venv) odoo16@ubuntu22:~$```

Next, let’s install Odoo

```
(odoo16-venv) odoo16@ubuntu22:~$ pip3 install wheel
(odoo16-venv) odoo16@ubuntu22:~$ pip3 install -r odoo16/requirements.txt
```

Once Odoo installation is completed, we can create a new directory to store our custom Odoo add-ons.

```
(odoo16-venv) odoo16@ubuntu22:~$ deactivate
$ mkdir /opt/odoo16/odoo16/custom-addons
```

Now, exit from user ‘odoo16’ and create the Odoo configuration file.

```
$ exit
$ sudo nano /etc/odoo16.conf
Paste the following contents into the file.
```

```
[options]
admin_passwd = m0d1fyth15
db_host = False
db_port = False
db_user = odoo16
db_password = False
addons_path = /opt/odoo16/odoo16/addons,/opt/odoo16/odoo16/custom-addons
xmlrpc_port = 8069
```

Make sure to modify the value of the m0d1fyth15 key above and use a stronger password. This is your Odoo master password; you need it to create or delete databases.

### Step 7. Create Odoo Systemd Unit file

In this step, we will create a systemd unit file. It is required to start/stop/restart Odoo.

```
$ sudo nano /etc/systemd/system/odoo16.service
```

Paste the following content into the systemd unit file above.

```
[Unit]
Description=Odoo16
Requires=postgresql.service
After=network.target postgresql.service

[Service]
Type=simple
SyslogIdentifier=odoo16
PermissionsStartOnly=true
User=odoo16
Group=odoo16
ExecStart=/opt/odoo16/odoo16-venv/bin/python3 /opt/odoo16/odoo16/odoo-bin -c /etc/odoo16.conf
StandardOutput=journal+console

[Install]
WantedBy=multi-user.target
```

That’s it. We can now reload systemd and run Odoo.

```
$ sudo systemctl daemon-reload
$ sudo systemctl start odoo16
```

Check if Odoo is starting by running this command:

```
$ sudo systemctl status odoo16
```
