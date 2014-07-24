# -*- mode: ruby -*-
# vi: set ft=ruby :

#
# this Vagrantfile creates a simple ubuntu 14.04 box and installs python 2&3 
# and the evelink requirements for both versions.
#
# you can run the tests with the commands nosetests-2.7 and nosetests-3.4
#

$script = <<SCRIPT
echo I am provisioning...
apt-get update -y
apt-get install -y python-pip python3-pip
pip install -r /vagrant/requirements_py2.txt
pip3 install -r /vagrant/requirements_py3.txt
date > /etc/vagrant_provisioned_at
SCRIPT

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "phusion/ubuntu-14.04-amd64"

  config.vm.provision "shell", inline: $script

end
