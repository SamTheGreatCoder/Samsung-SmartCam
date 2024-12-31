<?php
	$buffer = $_POST['log']; 
	$file_name = $_POST['model']."_".$_POST['type']."_".$_POST['time'].".txt";
	
	header("Content-Type: text/plain"); 
	header("Content-Length: " . strlen($buffer)); 
	header("Content-Disposition: attachment; filename=".$file_name); 
	  
	print($buffer); 
?>

