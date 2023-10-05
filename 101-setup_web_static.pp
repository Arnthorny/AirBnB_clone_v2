# Automate the set up of your web servers for the deployment of web_static
# Similar to file  `0-setup_web_static.sh`
include stdlib

$repl_dir = "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n}"
$config_file = '/etc/nginx/sites-available/default'
$index_cnt = @(EOT)
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
| EOT

$test_folder = '/data/web_static/releases/test/'
$sym_link = '/data/web_static/current'

$dirs = [ '/data/', '/data/web_static/', '/data/web_static/releases/',
          '/data/web_static/shared/', '/data/web_static/releases/test/'
        ]

# This exec resource runs the `apt-get update` command
exec { 'apt update':
  command => '/usr/bin/apt-get update'
}

# This package resource installs the `nginx` package
package { 'nginx':
  ensure  => 'installed',
  require => Exec['apt update']
}

# This service resource declares the nginx service
service { 'nginx':
  ensure => running,
  enable => true
}

#This resource creates all required directories
file { $dirs:
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => Package['nginx'],
  recurse => true
}

#This resource creates a test html file
file { "${test_folder}/index.html":
  ensure  => 'file',
  content => $index_cnt,
  require => File['/data/web_static/releases/test/'],
}

#This resource creates a symlink
#file { $sym_link:
#  ensure  => 'link',
#  target  => $test_folder,
#  replace => yes,
#  require => File['/data/web_static/releases/test/'],
#}

exec { 'Symlink':
  command => "rm -f ${sym_link} && ln -s ${test_folder} ${sym_link}",
  path    => [ '/bin/', '/sbin/' , '/usr/bin/', '/usr/sbin/' ],
  require => File[$test_folder],
}

# This resource replaces the closing brace with a location context.
file_line { 'Add location context':
  ensure   => present,
  path     => $config_file,
  line     => $repl_dir,
  match    => '^}$',
  multiple => false,
  require  => Package['nginx'],
  notify   => Service['nginx']
}
