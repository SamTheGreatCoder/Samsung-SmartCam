<?php
require_once '/mnt/custom/iwatch/include/php/util.php';
require_once '/mnt/custom/iwatch/include/php/config.php';
require_once '/mnt/custom/iwatch/include/php/curl.php';
require_once '/mnt/custom/iwatch/include/php/installer.php';

/**
 * Installation Script 
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * IWLInstallationManager class
 * 
 * @package         
 * @creation-date   2015-12-05
 * @revision        1.0.0.0
 */
class IWLInstallationManager
{
	
	protected $_mode;

	/**********************************************************************
	 * run - Executes validation and installation routines
	 *
	 * @param string $mode installer mode
	 * @param array $file $_FILES data
	 * @param array $data $_POST data
	 */
    public function __construct( $mode = iWatchInstaller::IWL_INSTALLER_ACTIVATE )
    {
		$this->_mode = $mode;
		$this->logger = new iWatchLogger();
        $this->logger->logfile = iWatchConfig::LOGGER;		
    }
	/**********************************************************************
	 * run - Executes validation and installation routines
	 *
	 * @param string $mode installer mode
	 * @param array $file $_FILES data
	 * @param array $data $_POST data
	 */
	public function run( $data, $async = false )
	{
		// load credentials
		$credentials = iWatchUtils::loadCredentials();

		if ( $async ){
			$this->logger->write("InstallManager - preparing installation");
			// dump data to file for async pull
			$activationData = iWatchUtils::sanitizeJSON( $data );
			file_put_contents(iWatchConfig::IWL_ACTIVATION_DATA, $activationData);
			// create an async curl request
			$httpclient = new Curl();
			$httpclient->setAsync( true );
			$httpclient->setOpt("digest","");
			$httpclient->setBasicAuthentication($credentials["username"],$credentials["password"]);
			$httpclient->post("http://127.0.0.1/custom/iwatch/admin/asyncInstaller.php",array("mode"=>$this->_mode));
			return true;

		} else {			
			return false;
		}
	}
	
}