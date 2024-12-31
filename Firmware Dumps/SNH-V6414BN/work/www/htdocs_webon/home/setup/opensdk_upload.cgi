<?php
require_once ('../../cgi-bin/adv/_define.inc');
require_once ('../language/language_system_opensdk.cgi');

  $classInstances = GetClassInstance('');

  $uploadResult = 0;
  $errorStatus = 0;
  $AppNameLength = 0;
  $error_message = "";
  $Cap_Name = "";  // Including file extension. i.e. example.cap
  $App_Name = "";      // Excluding file extension. i.e. example
  $Cap_Size = 0;
  $Allowed_Size = 2097152; //max 2M is allowed

  $Cap_Name = $_FILES['myfile']['name'];
  $Cap_Size = $_FILES['myfile']['size'];
  $App_Name =  substr($Cap_Name, 0, -4); // Remove file extention
  error_log($Cap_Size,0);
  $allowedExts = "cap";
  $extension = end(explode(".", $_FILES["myfile"]["name"]));
  error_log($extension,0);
  $Target_Directory = $GLOBALS['SDK_APP_DOWNLOAD_DIRECTORY'].$Cap_Name;
  //&& $Cap_Size > $Allowed_Size
  if(strlen($App_Name) ==0){
	$errorStatus = 1;
	$error_message = $msg_uploadError_Invalid_File[$GLOBALS['LANGINDEX']];
  }else{
	  if($Cap_Size == 0){
		$errorStatus = 1;
		$error_message = $msg_uploadError_max_size[$GLOBALS['LANGINDEX']];
	  }
	  if (($extension != $allowedExts) && $errorStatus == 0){
		$errorStatus = 1;
		$error_message = $msg_uploadError_Ext_notallowed[$GLOBALS['LANGINDEX']];
	  }
  }
  
  
  /*if ($errorStatus == 0) &&(ctype_space(substr($App_Name, 0, 1)) || ctype_space(substr($App_Name, -1))))
  {
        $errorStatus = 1;
  	$error_message = "Upload Failed : Invalid File Name. Allowed characters : Alphabets (A-Z & a-z), Numbers (0-9), Underscore (_), White Space (space either at the “beginning” or “end” is not allowed).";
  }
  
  if ($errorStatus == 0)
  {
        $AppNameLength = strlen($App_Name);
        if($AppNameLength <= 0)
        {
            $errorStatus = 1;
  	    $error_message = "Upload Failed : Invalid File Name. Allowed characters : Alphabets (A-Z & a-z), Numbers (0-9), Underscore (_), White Space (space either at the “beginning” or “end” is not allowed).";
        }
        for ($i = 0; $i < $AppNameLength; $i++)
        {
            if(substr($App_Name, $i, 1) == "_" || ctype_space(substr($App_Name, $i, 1)) || ctype_alnum(substr($App_Name, $i, 1)))
            {
                 continue;
            }
            $errorStatus = 1;
            $error_message = "Upload Failed : Invalid File Name. Allowed characters : Alphabets (A-Z & a-z), Numbers (0-9), Underscore (_), White Space (space either at the “beginning” or “end” is not allowed).";
            break;
        }
  }*/

  if($errorStatus == 0)
  {
        if(@move_uploaded_file($_FILES['myfile']['tmp_name'], $Target_Directory ));
  	{
  		$uploadResult = 1;
  		unlink($_FILES['myfile']['tmp_name']);  // To delete temp files
  	}
  }

?>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
<script language="javascript" type="text/javascript">
  var appName = "<?php echo $App_Name; ?>";
  var app_downloaded_directory = "<?php echo $GLOBALS['SDK_APP_DOWNLOAD_DIRECTORY']; ?>";
  var error_message_str = "<?php echo $error_message; ?>";
  window.top.window.postUploadDetails(<?php echo $uploadResult; ?>, appName, app_downloaded_directory, error_message_str);
  //window.opener.postUploadDetails(<?php echo $uploadResult; ?>, appName, app_downloaded_directory, error_message_str);
</script>
