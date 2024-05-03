#!/usr/bin/env bash
# a script that sets up web servers for the deployment of web_static.

# Install Nginx if not already installed
sudo apt update
sudo apt -y install nginx

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create a fake HTML file for testing
sudo echo "Dying is easy young man, living is harder" > /data/web_static/releases/test/index.html

# Remove existing symbolic link and create a new one
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Append to Nginx configuration
sudo chmod +w /etc/nginx/sites-available/default

sudo sed -i '/^\tserver_name/ a\\tlocation /hbnb_static \{\n\t\talias /data/web_static/current;\n\t\}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
