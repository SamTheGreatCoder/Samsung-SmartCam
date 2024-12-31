<?php

/**
 * Uninstall Script 
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * iWatchUninstaller class
 *       
 * @package         
 * @creation-date	2015-12-01 
 * @revision        1.0.0.0
 */
class iWatchUninstaller
{
	/* constants */
	const BASE_PATH = '/tmp';
	const IWL_ROOT_PATH  = '/mnt/custom/iwatch';


	/**********************************************************************
	 * run - Executes validation and installation routines
	 *
	 * @param string $mode installer mode
	 * @param array $file $_FILES data
	 * @param array $data $_POST data
	 */
	public function run( $data = null )
	{
		exec( iWatchUninstaller::IWL_ROOT_PATH . "/scripts/uninstall.sh" . " >> /tmp/iwl.firmware.log 2>&1 &");
		echo '{"result":"OK"}';
		
	}

}


/**
 * Script Main
 *
 * The contents of this file are considered proprietary information 
 * for the use of iWatchLife employees only.
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 */

// Ensure request method is POST
if ($_SERVER['REQUEST_METHOD'] != 'POST') {
	header('HTTP/1.0 405 Method not supported', true, 405);
	exit;
}

// Instantiate iWatch Installer and run with POST params
$iwlUninstaller = new iWatchUninstaller();
$iwlUninstaller->run( $_POST );