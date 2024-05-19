# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "vastra-preseed"
  config.vm.network "public_network"

# What kind of host is this?

 # Deployed machine: web | postgis

  config.vm.define "web"
  # Disable the shared folder
  #config.vm.synced_folder(".", nil, :disabled => true, :id => "vagrant-root")

 # Development machine: dev | pbxdev
  
  #config.vm.define "dev"
  # Share source folders
  config.vm.synced_folder "../../src", "/home/vagrant/src"
  config.vm.synced_folder "../../Projects", "/home/vagrant/Projects"

# Do this as a separate setup, run ansible-playbook -i "someinventoryfile" setup.yml
  config.vm.provision "ansible" do |ansible|
#    ansible.groups = {
#      "pbx_group" => ["pbx"],
#      "dev_group" => ["dev"],
#      "all_groups:children" => ["pbx_group", "dev_group"]
#    }
  
    ansible.playbook = "../fogg-ansible/vagrant_setup.yml"
  end

  
end
