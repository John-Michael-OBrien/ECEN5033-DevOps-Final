# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

$baseprovision = <<-SCRIPT
     apt-get update
	 sed -e "s/^\(\s*net.ipv4.ip_forward\s*=\s*\)0/\11/g" -i.bak /etc/sysctl.conf
SCRIPT

# Provisioning script for the administration computer which makes
# auth keys, copies the public key into the shared folder for the clients
# to import. And installs ansible.
$admprovision = <<-SCRIPT
     echo Generating Identity
     sudo -u vagrant ssh-keygen -N "" -q -t rsa -f /home/vagrant/.ssh/id_rsa
	 cp /home/vagrant/.ssh/id_rsa ~/.ssh/id_rsa
     echo "Exporting Administrator Public Key..."
     cp /home/vagrant/.ssh/id_rsa.pub /vagrant/adm_id_rsa.pub

	 echo "Installing Ansible Repo..."
     apt-get install software-properties-common
     apt-add-repository ppa:ansible/ansible

	 echo "Installing Google Cloud SDK Repo..."
	 export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
	 echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
	 curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
	 
	 echo "Updating Apt..."
     apt-get update

	 echo "Installing Ansible Resources..."
	 apt-get install -y ansible
 	 apt-get install -y python-pip

	 echo "Installing Google Cloud SDK..."
	 apt-get install -y google-cloud-sdk
	 
	 cd ~
	 git clone https://github.com/kubernetes-incubator/kubespray.git
	 cd kubespray
	 pip install -r requirements.txt
	 cp -r /vagrant/jmcluster inventory/jmcluster
	 
SCRIPT

# Import the public key from the administrator into our authorized_keys.
$workerprovision = <<-SCRIPT
echo "Importing Administrator Public Key..."
sudo -u vagrant cat  /vagrant/adm_id_rsa.pub >> /home/vagrant/.ssh/authorized_keys 
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.provision "shell", inline: $baseprovision 
  
  config.vm.define "master" do |master|
     master.vm.network "private_network", ip: "10.10.77.2", netmask: "24"
	 master.vm.hostname = "kubely-master"
     master.vm.provider "virtualbox" do |vb|
       vb.memory = "2048"
     end
     master.vm.provision "shell", inline: $admprovision
  end

  config.vm.define "worker1" do |worker|
     worker.vm.network "private_network", ip: "10.10.77.3", netmask: "24"
	 worker.vm.hostname = "kubely-worker1"
     worker.vm.provider "virtualbox" do |vb|
       vb.memory = "2048"
     end
     worker.vm.provision "shell", inline: $workerprovision
  end 
  
  config.vm.define "worker2" do |worker|
     worker.vm.network "private_network", ip: "10.10.77.4", netmask: "24"
	 worker.vm.hostname = "kubely-worker2"
     worker.vm.provider "virtualbox" do |vb|
       vb.memory = "2048"
     end
     worker.vm.provision "shell", inline: $workerprovision
  end 
  config.vm.define "worker3" do |worker|
     worker.vm.network "private_network", ip: "10.10.77.5", netmask: "24"
	 worker.vm.hostname = "kubely-worker3"
     worker.vm.provider "virtualbox" do |vb|
       vb.memory = "2048"
     end
     worker.vm.provision "shell", inline: $workerprovision
  end 
  config.vm.provision "shell", inline: <<-SHELL
  SHELL
end
