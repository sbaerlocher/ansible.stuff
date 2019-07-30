Vagrant.require_version ">= 2.0.0"

Vagrant.configure(1) do |config|

 config.vm.box = "debian/stretch64"
 config.vm.provision "shell", inline: "apt install --yes git python3-pip python-apt"
 config.vm.provision "ansible" do |ansible|
   ansible.verbose = "v"
   ansible.playbook = "playbook.yml"
 end
end
