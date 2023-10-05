#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static


apt-get -y update
apt-get -y install nginx


if ! nginx -v
then
	exit
fi


test_folder="/data/web_static/releases/test"
sym_link="/data/web_static/current"
nginx_conf="/etc/nginx/sites-available/default"

mkdir -p "$test_folder"
mkdir -p "/data/web_static/shared/"

printf %s "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" > "$test_folder/index.html"

ln -sf -T "$test_folder" "$sym_link"
chown -R ubuntu:ubuntu "/data"


text="\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}\n}"
sed -i -r "s/^}$/$text/" "$nginx_conf"

nginx -s reload
