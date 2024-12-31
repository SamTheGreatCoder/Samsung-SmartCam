<?php
session_start();
$_SESSION["marketUserName"] = null;
$_SESSION["marketPassword"] = null;
header("Location: ./system_market.cgi");
?>
