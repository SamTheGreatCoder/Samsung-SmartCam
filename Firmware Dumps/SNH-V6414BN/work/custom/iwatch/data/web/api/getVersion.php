#!/usr/www/php-cgi
<?php

/**
 * iWatchLife getVersion.php script (returns version number)
 *
 * The contents of this file are considered proprietary information
 * for the use of iWatchLife employees only.
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * @package
 * @creation-date       2012-10-30
 * @revision        1.0.0.0
 */

$IWL_HOME="/mnt/custom/iwatch" ;
putenv ("IWL_HOME=$IWL_HOME") ;


/**************************************************************
 *
 * Script Main
 *
 **************************************************************/

$http_request_type =  strtolower($_SERVER['REQUEST_METHOD']) ;

if ($http_request_type == 'get') {

  $version_file = NULL ;

  // handle GET

  if (isset($_SERVER['QUERY_STRING'])) {
      $query_string     =   $_SERVER['QUERY_STRING'] ;
      putenv ("QUERY_STRING=$query_string") ;
  }

  if ($query_string === "type=base") {
      $version_file = "base.ver" ;
  } else if ($query_string === "type=iwatch") {
      $version_file = "iwatch.ver" ;
  } else {
    $status_line = "400 Bad type." ;
    $status      = 400;
    $message     = "Bad version type given. Needs to be either base or iwatch." ;
  }

  if ($version_file != NULL) {

      if (file_exists ("$IWL_HOME/conf/$version_file")) {
          $status_line = "200 OK" ;
          $status      = 200 ;
          $message     = file_get_contents ("$IWL_HOME/conf/$version_file") ;
      } else {
          $status_line = "400 No version file" ;
          $status      = 400;
          $message     = "No version file $IWL_HOME/conf/$version_file" ;
      }

  }

} else {

  $status_line = "400 Not GET" ;
  $status      = 400;
  $message     = "getVersion needs to be a GET request.";

}

$cl             =   strlen ($message) ;

header("$status_line", true, (int)$status);
header("Content-Type: text/html");
header("Content-Length: $cl");

echo ($message);

exit

?>


