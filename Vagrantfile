# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. 
# Do not change it unless you know what you're doing.

Vagrant.configure("2") do |config|
    config.vm.box = "bento/ubuntu-20.04"
    config.vm.define "vetiot" do |vetiot|
        vetiot.vm.hostname = "vetiot"
  
        vetiot.vm.network "private_network", ip: "192.168.56.10"
        vetiot.vm.network "forwarded_port", guest: 8080, host: 8080
  
      # Share an additional folder to the guest VM. The first argument is
      # the path on the host to the actual folder. The second argument is
      # the path on the guest to mount the folder. And the optional third
      # argument is a set of non-required options.
        vetiot.vm.synced_folder "./vetiot", "/home/vagrant/vetiot"
        vetiot.vm.synced_folder ".", "/vagrant", disabled: true
        vetiot.vm.provision "shell", inline: <<~SHELL
          export DEBIAN_FRONTEND=noninteractive
          apt-get update
          apt-get upgrade -y
          apt-get install -y python3.9 python3.9-venv
          apt-get install -y unzip
          SHELL
        vetiot.vm.provision "file", source: "./bootstrap.sh", destination: "/tmp/bootstrap.sh"
        vetiot.vm.provision "shell", inline: "/bin/bash --login /tmp/bootstrap.sh"
    end
end
  
  
  
