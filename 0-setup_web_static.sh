#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static


if ! nginx -v >> /dev/null 2>&1
then
	apt-get -y update
	apt-get -y install nginx
fi


test_folder="/data/web_static/releases/test/"
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

rm -f "$sym_link"
ln -s "$test_folder" "$sym_link"

chown -R ubuntu:ubuntu "/data/"


text="\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}\n}"
sed -i -r "s/^}$/$text/" "$nginx_conf"

service nginx restart
