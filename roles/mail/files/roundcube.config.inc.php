<?php

# I should put a better password in here.
$config['db_dsnw'] = 'mysql://roundcube:phoneme@localhost/roundcube';

$config['default_host'] = 'localhost';
$config['smtp_server'] = 'localhost';
$config['smtp_port'] = 25;
$config['smtp_user'] = '';
$config['smtp_pass'] = '';
$config['support_url'] = '';
$config['product_name'] = 'Vastra Voice Mail';
$config['des_key'] = '0IoSa6ICkJBvRy87hXXHsxxs';
$config['plugins'] = array(
  'archive',
  'zipdownload',
  'password',
);
$config['skin'] = 'classic';
$config['skin_logo'] = '/images/logo.png';

$config['imap_auth_type'] = PLAIN;
?>

