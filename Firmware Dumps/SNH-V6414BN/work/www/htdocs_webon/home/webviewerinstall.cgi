<?php
$temp = $_SERVER['HTTP_USER_AGENT'];

if(strstr($temp, "Mac") != null) $os_name = "Mac";
else if(strstr($temp, "Windows") != null) $os_name = "Windows";

if($os_name == "Mac") $runtime = "./STWWebviewer.pkg";
else if($os_name == "Windows") $runtime = "./STWWebViewer.exe";
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>SAMSUNG NETWORK CAMERA</title>
</head>
<body>
<p>Network Camera Webviewer Plugin Installation/Update.</p>
<p>
<a href="<?php echo $runtime; ?>">Click Here</a>
</p>
</body>
</html>
