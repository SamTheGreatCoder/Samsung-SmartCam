<?php
require_once '/mnt/custom/iwatch/include/php/util.php';
require_once '/mnt/custom/iwatch/include/php/config.php';
require_once '/mnt/custom/iwatch/include/php/curl.php';
require_once '/mnt/custom/iwatch/include/php/iWLCamera.php';
require_once '/mnt/custom/iwatch/include/php/logger.php';
/**
 * WirelessManager Script 
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * WirelessManager class
 * 
 * @package         
 * @creation-date	2015-12-01 
 * @revision        1.0.0.0
 */
class WirelessManager
{
const CHECK_WIRELESS_RETRY = 15;
protected $_credentials = array();
    public function __construct( $creds = array() )
    {
		$this->_credentials = $creds;
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
	public function run( $data )
	{
		// load credentials
		$credentials = iWatchUtils::loadCredentials();
		// Configure Wireless
		$securityMode = 0;
		// configure wireless
		$success = false;
		$hiddenSSID = true;
		$wirelessActivated = false;
		$currentNetwork = iWatchCamera::getWirelessProfile(iWatchConfig::CAM_MODEL,$this->_credentials);

		// Check to see if current network is up
		if (  ($currentNetwork->Enable) && ( strcasecmp($currentNetwork->ConnectedSSID,$data->ssid) == 0 )){
			$netinfo = iWatchCamera::getNetworkProfile(iWatchConfig::CAM_MODEL, $this->_credentials);
			$address = trim($netinfo->IPv4Gateway);
			$pingresult = iWatchUtils::ping($address,0,20);			
			if ($pingresult['result']){
				$this->logger->write("WirelessManager - target network already connected ". $data->ssid);
				return true;
			}
		}

		$this->logger->write("WirelessManager - Verifying target network ". $data->ssid);
		// Ensure we detect the SSID in list before setting
        $wirelessList = iWatchCamera::getWirelessList(iWatchConfig::CAM_MODEL, $this->_credentials);
        foreach ($wirelessList as $network){
                if ($network->ssid == $data->ssid){
                		$hiddenSSID = false;
						$securityMode = $network->mode;
						if ($this->setNetwork(!$currentNetwork->Enable, $data, $securityMode)){
							$wirelessActivated = true;	
						}
                        break;
                } 
        }

        // attempt to configure hidden SSID with PSK                
        if ($hiddenSSID){
        	$wirelessSM = array("PSK","WEP","None");
        	$this->logger->write("WirelessManager - Unable to find target network....attempting hidden option... ". $data->ssid);
	        foreach ($wirelessSM as $mode){
				if ($this->setNetwork(!$currentNetwork->Enable, $data, $mode)){
					$wirelessActivated = true;	
					break;
				}
	        }
    	}


		$this->logger->write("WirelessManager - Wireless active...".$wirelessActivated);
		return $wirelessActivated;
	
	}

  public function setNetwork( $enable = false, $wirelessConfig, $securityMode ){
	$wirelessActivated = false;
	$success = false;

	// enable chipset if required
	if ($enable){
		$this->logger->write("WirelessManager - wireless disabled - activating ");	
		iWatchCamera::setWirelessState(iWatchConfig::CAM_MODEL,$this->_credentials,true);
	}

	// Set wireless profile
	$passphrase = (empty($wirelessConfig->passphrase)) ? null : $wirelessConfig->passphrase; 
	if (iWatchCamera::setWirelessProfile(iWatchConfig::CAM_MODEL,$this->_credentials,array("ssid"=>$wirelessConfig->ssid,"passphrase"=>$passphrase,"mode"=>$securityMode))){
		$this->logger->write("WirelessManager - Wireless connected....checking wireless status...");
		for ($i = 0; $i < WirelessManager::CHECK_WIRELESS_RETRY; $i++){
				if (iWatchCamera::getWirelessState(iWatchConfig::CAM_MODEL, $this->_credentials)){
						$netinfo = iWatchCamera::getNetworkProfile(iWatchConfig::CAM_MODEL, $this->_credentials);
						$address = trim($netinfo->IPv4Address);
						if ( !empty($address) ){
							$this->logger->write("WirelessManager - Device is connected...".$address);
							$success = true;
							break;
						} else {			
							sleep(3);
						}
				} else {
						sleep(5);
				}
		}	
	}

	return $success;
  }

 }