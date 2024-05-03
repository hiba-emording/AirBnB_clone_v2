# sets up web servers for the deployment of web_static
# Define Nginx class from Puppet Forge nginx module
class { 'nginx': }

# Ensure directories are created
file { ['/data/web_static/releases/test', '/data/web_static/shared']:
  ensure => 'directory',
}

# Create fake HTML file
file { '/data/web_static/releases/test/index.html':
  content => 'Dying is easy young man, living is harder',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# Set ownership of the /data folder
file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Append to Nginx configuration
augeas { 'nginx_location':
  context => '/files/etc/nginx/sites-available/default',
  changes => "set server/location[last()+1] ''",
  notify  => Service['nginx'],
}

augeas { 'nginx_location_alias':
  context => '/files/etc/nginx/sites-available/default/server/location[last()]',
  changes => "set alias '/data/web_static/current'",
  notify  => Service['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure => 'running',
  enable => true,
}
