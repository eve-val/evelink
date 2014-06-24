# -*- mode: ruby -*-
# vi: set ft=ruby :

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
