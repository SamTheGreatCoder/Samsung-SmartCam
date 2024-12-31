<?php
session_start();
$_SESSION["MARKET_SERVER_IP"] = $_POST["MARKET_SERVER_IP"];
$_SESSION["MARKET_SERVER_PORT"] = $_POST["MARKET_SERVER_PORT"];
header("Location: ./system_market.cgi");
?>
