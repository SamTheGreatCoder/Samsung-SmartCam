<?php


   if (isset($_SERVER['QUERY_STRING'])) {
       $filename    =   basename($_SERVER['QUERY_STRING']) ;
   } else {
       $filename    =   "" ;
   }

   $full_filename = NULL ;

   if (is_file("/tmp/logs/".$filename)) {
       $full_filename = "/tmp/logs/".$filename ;
   } else if (is_file("/tmp/camera_data/".$filename)) {
       $full_filename = "/tmp/camera_data/".$filename ;
   }

   if ($full_filename != NULL){

      // the intended file is in /tmp

      header('Status: 200 OK', true, 200);
      header('Content-Description: File Transfer');
      header('Content-Type: application/octet-stream');
      header('Content-Disposition: attachment; filename='.$filename);
      header('Content-Transfer-Encoding: binary');
      header('Expires: 0');
      header('Cache-Control: must-revalidate');
      header('Pragma: public');
      header('Content-Length: ' . filesize($full_filename));

      ob_clean();
      flush();

      readfile($full_filename);

   } else {

      $message = PHP_EOL ;

      header('Status: 404 File Not Found', true, 404);
      header('Content-Type: text/plain');
      header('Content-Length: ' . strlen($message));

      echo ($message) ;


   }

   exit ;


?>

