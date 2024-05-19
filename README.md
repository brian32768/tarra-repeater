## Provisioning a vagrant machine

This sets up a new machine from scratch to be a complete asterisk based phone server.
It was a year long project that I embarked upon but ultimately abandoned. I pushed
it to this github repo and I'm about to fork it to turn it into a ham radio
SVXlink repeater system. Small change LOL.



### What to do

cd to folder containing the machine

possibly
vagrant up

then
vagrant provision

## Provisioning a real hardware machine

Tell me everything you know about a host:
ansible -i inventory bellman.wildsong.biz -m setup

Run everything; careful you don't whack production machines!
ansible-playbook -i inventory setup.yml

Just run one role: 
ansible-playbook -i inventory roles/apache2/tasks/install.yml 


Some packages that could go in as part of Debian --

mysql server -- then I could insert a password in preseed.cfg
phpmyadmin
postfix

1. PXEboot server installs base Debian on target.
2. Ansible does provisioning

### PXEboot server

DHCP server

Set up the options to point at the PXEboot server and ask for pxelinux.0
Mikrotik router was not able to serve options, so I use either OpenWRT or Linux.

TFTP server

Install tftpd-hpa package.
Unpack Debian's netboot.tar.gz file in /srv/tftp/
Copy the files in tftp to /srv/tftp

Web server

Set the web server to respond to the hostname 'autoserver'.
Copy the tree d-i to the web server, perhaps at /var/www/?
Test with a browser: When you request http://autoserver/d-i/jessie/preseed.cfg you should get the file.

The preseed.cfg file has some custom presets in it. These include
  Selecting the US keyboard setting
  Use a proxy on local server. 192.168.1.2:8000
  Sets an ntp server, probably should not. 192.168.1.1
  Set root password with plaintext password.
  Create bwilson account with MD5 password.
  preseed/late_command
    Put an ssh key in for bwilson
    Allow bwilson to have sudo access, to facilitate ansible 'become' feature.

## Ansible provisioning

With vagrant, it's just "vagrant provision", voila!

With real hardware, add the machine to the inventory file ansible_hosts in the appropriate group

To use ansible directly, I have added ansible.cfg here and pointed it at ansible.hosts

Double check the boot config on the target, you don't want to re-install Debian!
Boot target (from the hard drive!)

Remove an old host key if you are rebuilding the same machine, for example

        ssh-keygen -f "/home/bwilson/.ssh/known_hosts" -R 192.168.1.232

Now try running
 
        ansible-playbook -i pbx vastra-setup.yml

or to run one particular role, try

        ansible-playbook -i pbx roles/nginx/tasks/install.yml

I need to figure out a clean way to avoid password prompts.

To update bellman

ansible-playbook -i inventory setup.yml
