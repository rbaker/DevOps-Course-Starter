Vagrant.configure("2") do |config|
  
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provision "shell", privileged: false, inline: <<-SHELL

    sudo apt-get update -y
    sudo apt-get install libedit-dev -y
    sudo apt-get install libncurses5-dev -y
    sudo apt-get install build-essential -y
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo 'eval "$(pyenv init --path)"' >> ~/.profile
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    . ~/.profile
    . ~/.bashrc
    pyenv install 3.9.2
    pyenv global 3.9.2
    curl -ssl https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

  SHELL
  
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
    cd /vagrant
    poetry update package
    poetry install
    mkdir -p logs
    nohup $(poetry env info -p)/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app --daemon --access-logfile logs/accesslog.txt --log-file logs/log.txt 
    "}
  end

end
