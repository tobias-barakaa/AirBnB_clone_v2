# Ensure Nginx is installed
package { 'nginx':
  ensure => 'installed',
}

# Create necessary directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => 'directory',
}

# Deploy a simple HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => 'Holberton School for the win!',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Remove existing symbolic link
file { '/data/web_static/current':
  ensure => 'absent',
}

# Create a new symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Define an Nginx server configuration block
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => template('your_module/nginx_config.erb'),
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Ensure Nginx service is running and enabled
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => Package['nginx'],
}
