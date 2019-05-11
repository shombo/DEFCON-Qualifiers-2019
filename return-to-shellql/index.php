#!/usr/bin/php-cgi
<?php

if (isset($_GET['source']))
{
   show_source(__FILE__);
   exit();
}

$link = mysqli_connect('127.0.0.1:31337', 'shellql', 'shellql', 'shellql');

//sleep(300);


if (isset($_POST['shell']))
{
   $hexdshell = bin2hex($_POST['shell']);
   $txt = "HERE is shell length = " . (strlen($hexdshell)/2) . "-----------------------------\n" . $hexdshell . "\n------------------------------\n";
   $myfile = file_put_contents('/tmp/logs.txt', $txt.PHP_EOL , FILE_APPEND | LOCK_EX);
   fwrite($myfile, $txt);
   fclose($myfile);

   if (strlen($_POST['shell']) <= 1000)
   {
          echo $_POST['shell'];
          shellme($_POST['shell']);
   }
   exit();
}



?>

<html>

<form action="index.php" method=POST>
shell <input type=text name=shell required><br>
<input type=submit value="shell me">
</form>

<a href="?source">debug me</a> <br>

</html>
