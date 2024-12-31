<?php
require_once '/mnt/custom/iwatch/include/php/installManager.php';

/**
 * Activation Script 
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * 
 * @package         
 * @creation-date   2015-12-05
 * @revision        1.0.0.0
 */

// Ensure request method is POST
if ($_SERVER['REQUEST_METHOD'] != 'POST') {
	header('HTTP/1.0 405 Method not supported', true, 405);
	exit;
}

$async_mode = true;
// get raw post body
$data  = file_get_contents("php://input");
// Instantiate iWatch Installer and run async with POST params
$iwlInstaller = new IWLInstallationManager( );
if (!$iwlInstaller->run( $data, $async_mode ) ){
	header('HTTP/1.0 500 General Error', true, 500);
	exit;
} else {
	echo '{"result":"OK"}';
}