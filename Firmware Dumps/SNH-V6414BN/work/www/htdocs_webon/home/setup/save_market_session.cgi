<?php
session_start();
$_SESSION["marketUserName"] = $_POST["marketUserName"];
$_SESSION["marketPassword"] = $_POST["marketPassword"];
header("Location: ./system_market.cgi");
//header("Location: ./auth_system_market.cgi");
echo $_SESSION["marketUserName"];
echo $_SESSION["marketPassword"];
?>
