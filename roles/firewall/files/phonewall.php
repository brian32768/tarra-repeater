<html><body>
<?php
$cmd = $_SERVER['PATH_INFO'][1];
if ($cmd == '0') {
   $output = shell_exec("/usr/local/bin/phonewall 0");
   
} elseif ($cmd == '1') {
   $output = shell_exec("/usr/local/bin/phonewall 1");
   print "The phonewall will close <b>one hour</b> from now.<br />";
}
$output = shell_exec("/usr/local/bin/phonewall");
print "The phonewall is <b>" . $output . "</b><br>";
$cmd = "1";
$word = 'open';
if ($output[0] == 'a') {
   $cmd = "0";
   $word = 'close';
}
print '<p>Click here to <a href="/phonewall.php/' . $cmd . '">' . $word . '</a></p>';
?>
</body></html>
