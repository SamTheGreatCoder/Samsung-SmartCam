<?php
$pageData = explode(";", $_POST["data"]);
if($pageData[0] == "CHECK_SERVER"){
	echo "OK";
}
?>