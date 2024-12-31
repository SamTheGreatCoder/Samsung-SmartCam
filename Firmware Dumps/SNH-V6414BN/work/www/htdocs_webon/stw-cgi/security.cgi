<?php

require_once ('./adv/_define.inc');
CheckGuestAccount(FALSE);

define('MAX_IPV4_IPFILTER', 10);
define('MAX_IPV6_IPFILTER', 10);

function CalSubnetMask($prefix)
{
	$prefixVal = '';
	$dataVal = array("255", "254", "252", "248", "240", "224", "192", "128", "0");
	
	if($prefix >= 24)
	{
		$prefixVal = '255.255.255.';
		$prefixVal .= $dataVal[32-$prefix];
	}
	else if($prefix >= 16)
	{
		$prefixVal = '255.255.';
		$prefixVal .= ($dataVal[24-$prefix] . '.0');
	}
	else if($prefix >= 8)
	{
		$prefixVal = '255.';
		$prefixVal .= ($dataVal[16-$prefix] . '.0.0');
	}
	else
	{
		$prefixVal .= ($dataVal[8-$prefix] . '.0.0.0');
	}
	
	return $prefixVal;
}

function GetMyIPAddress($addrVal)
{
	$ipPattern 	= '/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/';
	if(preg_match($ipPattern, $addrVal, $ipArray) != 1) // if ipv6_enable==true, my ip show ipv6 address format. so need parsing
	{
		$splitIP = explode(':', $addrVal);
		$addrVal = $splitIP[count($splitIP)-1];
	}
	
	return $addrVal;
}

function GetMyIPv6Address($addrVal)
{
	$retVal = strpos($addrVal, '.');
	if ($retVal !== FALSE) {
		$splitIP = explode(':', $addrVal);
		$ipv4Addr = explode('.', $splitIP[count($splitIP)-1]);
		$tempAddr1	= ($ipv4Addr[0]<<8) | $ipv4Addr[1];
		$tempAddr2	= ($ipv4Addr[2]<<8) | $ipv4Addr[3];
		$tempAddr1 = dechex($tempAddr1);
		$tempAddr2 = dechex($tempAddr2);
		$addrVal = '';
		for ($index=0; $index<(count($splitIP)-1); ++$index) {
			$addrVal .= $splitIP[$index] . ':';
		}
		$addrVal .= $tempAddr1  . ':' . $tempAddr2;
	}
	
	return $addrVal;
}

function SplitIPv6Address($addr)
{
	$arrIP = explode(':', $addr);
	$frontValCnt = 0;
	$backValCnt = 0;
	$backAddr = array();
	
	for($i = 0 ; $i < count($arrIP) ; ++$i)
	{
		if(strlen($arrIP[$i]) == 0)
		{
			for($j = $i ; $j < count($arrIP) ; ++$j)
			{
				if(strlen($arrIP[$j]) != 0)
				{
					$backAddr[$backValCnt] = $arrIP[$j];
					$backValCnt++;
				}
			}
			break;
		}
		$frontValCnt++;
	}
	
	for($i = 0 ; $i < $backValCnt ; ++$i)
	{
		$arrIP[8 - ($backValCnt - $i)] = $backAddr[$i];
	}
	
	$offset = 8 - ($frontValCnt + $backValCnt);
	for($i = $frontValCnt ; $i < ($frontValCnt + $offset) ; ++$i)
	{
		$arrIP[$i] = 0;
	}
	
	return $arrIP;
}

function GetAddrBinary($addrVal, $valLength)
{
	$ipBinaryVal = 0;
	
	for ($i=0; $i<$valLength; ++$i) {
		$binVal = 0;
		if 		(substr($addrVal, $i, 1) == 'f' || substr($addrVal, $i, 1) == 'F') 	$binVal = 15;
		else if 	(substr($addrVal, $i, 1) == 'e' || substr($addrVal, $i, 1) == 'E') 	$binVal = 14;
		else if 	(substr($addrVal, $i, 1) == 'd' || substr($addrVal, $i, 1) == 'D') 	$binVal = 13;
		else if 	(substr($addrVal, $i, 1) == 'c' || substr($addrVal, $i, 1) == 'C')	$binVal = 12;
		else if 	(substr($addrVal, $i, 1) == 'b' || substr($addrVal, $i, 1) == 'B')	$binVal = 11;
		else if 	(substr($addrVal, $i, 1) == 'a' || substr($addrVal, 0, 1) == 'A')	$binVal = 10;
		else		$binVal = substr($addrVal, $i, 1);
		
		$ipBinaryVal = $ipBinaryVal << 4;
		$ipBinaryVal |= $binVal;
	}
	return $ipBinaryVal;
}

// for ip filtereing
// return 0 : input IP != my IP, return 1 : input IP = my IP
function CheckMyIP($_IPType, $_addr = '', $_prefix = 0)
{
	$myIPAddr = $_SERVER['REMOTE_ADDR'];
	
	if($_IPType == 4)
	{
		$myIPtmp = GetMyIPAddress($myIPAddr);
		$arrMyIP = explode('.', $myIPtmp);
		$myip_32 = ($arrMyIP[0]<<24) | ($arrMyIP[1]<<16) | ($arrMyIP[2]<<8) | $arrMyIP[3];
		
		$arrIP = explode('.', $_addr);
		$ip_32 = ($arrIP[0]<<24) | ($arrIP[1]<<16) | ($arrIP[2]<<8)| $arrIP[3];

		$subnetAdddr = explode('.', CalSubnetMask($_prefix));
		$nm_32 = ($subnetAdddr[0]<<24) | ($subnetAdddr[1]<<16) | ($subnetAdddr[2]<<8) | $subnetAdddr[3];

		if($_prefix == 32)
		{
			if ($arrMyIP[0] == $arrIP[0] && $arrMyIP[1] == $arrIP[1] && $arrMyIP[2] == $arrIP[2] && $arrMyIP[3] == $arrIP[3])
			{
				return 1;
			}
		}
		else
		{
			if(($ip_32 & $nm_32) == ($myip_32 & $nm_32))
			{
				return 1;
			}
		}
	}
	else //IPv6
	{
		$myIPv6 = GetMyIPv6Address($myIPAddr);
		$myIP = SplitIPv6Address(strtolower($myIPv6));
		
		$inputIP = SplitIPv6Address(strtolower($_addr));

		if($_prefix == 128)
		{
			if ($inputIP[0] == $myIP[0] && $inputIP[1] == $myIP[1] && $inputIP[2] == $myIP[2] && $inputIP[3] == $myIP[3] && 
				$inputIP[4] == $myIP[4] && $inputIP[5] == $myIP[5] && $inputIP[6] == $myIP[6] && $inputIP[7] == $myIP[7])
			{
				return 1;
			}
		}
		else
		{
			$min_mask = 0;	$max_mask = 0;
			$min_IP = SplitIPv6Address(strtolower($_addr));		$max_IP = SplitIPv6Address(strtolower($_addr));
			$div = intval($_prefix / 16);		$mod = intval($_prefix % 16);

			if($mod != 0)
			{
				for($i = (16 - $mod) ; $i < 16 ; $i++)
				{
					$tmp = 1 << $i;
					$min_mask |= $tmp;
				}
			}

			$min_IP[$div] = dechex(GetAddrBinary($min_IP[$div], strlen($min_IP[$div])) & $min_mask);

			for ($i=$div+1; $i<8; $i++) $min_IP[$i] = 0;

			if($mod != 0)
			{
				for($i = 0 ; $i < (16 - $mod) ; $i++)
				{
					$tmp = 1 << $i;
					$max_mask |= $tmp;
				}
			}
			else
			{
				$max_mask = 65535;
			}

			$max_IP[$div] = dechex(GetAddrBinary($max_IP[$div], strlen($max_IP[$div])) | $max_mask);
			for ($i=$div+1; $i<8; $i++) $max_IP[$i] = 'ffff';

			$isMatch = 0;

			for($ix = 0 ; $ix < 8 ; ++$ix)
			{
				if (hexdec($min_IP[$ix]) < hexdec($myIP[$ix]) && hexdec($myIP[$ix]) < hexdec($max_IP[$ix])) {
					$isMatch = 1;
					break;
				}
				else if ($min_IP[$ix] == $myIP[$ix] || $myIP[$ix] == $max_IP[$ix]) {
					if ($ix == 7) {
						if ($min_IP[$ix] == $myIP[$ix] || $myIP[$ix] == $max_IP[$ix]) {
							$isMatch = 1;
							break;
						}
					}
					continue;
				}
				else {
					break;
				}
			}

			if($isMatch == 1)
			{
				return 1;
			}
		}
	}
	
	return 0;
}

// ip filtering
function submenu_ipfilter()
{
    CheckAdminAccount(FALSE);
    $responseOutput = new ResponseOutput();

    $classInstances = GetClassInstance('ipfilter');
    $ipFiltering = $classInstances['IPFilterConfiguration'];

    global $boolArray;

    $AccessTypeArr = array(0 => 'Deny', 1 => 'Allow');

    if ($_REQUEST['action'] == 'add')
    {
        if (!isset($_REQUEST['IPType']) || !isset($_REQUEST['Address']))
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        if ($_REQUEST['IPType'] != 'IPv4' && $_REQUEST['IPType'] != 'IPv6')
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }

        $index = -1;
    }
    else if ($_REQUEST['action'] == 'update' || $_REQUEST['action'] == 'remove')
    {
        if (!isset($_REQUEST['IPType']) || !isset($_REQUEST['IPIndex']))
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        if ($_REQUEST['IPType'] != 'IPv4' && $_REQUEST['IPType'] != 'IPv6')
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }

        if ($_REQUEST['IPIndex'] < 1 || $_REQUEST['IPIndex'] > 10)
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }

        $index = ($_REQUEST['IPIndex'] - 1);
    }
	
    if ($_REQUEST['action'] == 'set')
    {
        if (isset($_REQUEST['AccessType']))
        {
            if ($_REQUEST['AccessType'] != 'Allow' && $_REQUEST['AccessType'] != 'Deny')
            {
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }

            $ipFiltering->defaultPolicy = array_search($_REQUEST['AccessType'], $AccessTypeArr);
			
			$addMyIP = 1;	$index = -1;
			for ($i = 0; $i < MAX_IPV4_IPFILTER; ++$i)
			{
				if(CheckMyIP(4, $ipFiltering->ipv4IPFilter[$i]->dataInfo['Address']['value'], $ipFiltering->ipv4IPFilter[$i]->dataInfo['Prefix']['value']) == 1)
				{
					if($ipFiltering->defaultPolicy == 0) //Deny
					{
						$ipFiltering->ipv4IPFilter[$i]->dataInfo['Enabled']['value'] = 0;
						$ipFiltering->ipv4IPFilter[$i]->dataInfo['Address']['value'] = '';
						$ipFiltering->ipv4IPFilter[$i]->dataInfo['Prefix']['value'] = 32;
						$ipFiltering->ipv4IPFilter[$i]->payload = MakePayload($ipFiltering->ipv4IPFilter[$i]->dataInfo);
					}
					else
					{
						if($ipFiltering->ipv4IPFilter[$i]->dataInfo['Enabled']['value'] == 0)
						{
							$ipFiltering->ipv4IPFilter[$i]->dataInfo['Enabled']['value'] = 1;
							$ipFiltering->ipv4IPFilter[$i]->payload = MakePayload($ipFiltering->ipv4IPFilter[$i]->dataInfo);
						}
						
						$addMyIP = 0;
					}
				}
				
				if ($index == -1)
				{
					if ($ipFiltering->ipv4IPFilter[$i]->dataInfo['Address']['value'] == NULL)
					{
						$index = $i;
					}
				}
			}
			
			if($addMyIP == 1 && $ipFiltering->defaultPolicy == 1)
			{
				if($index == -1)
				{
					$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
					return $responseOutput;
				}
				
				$ipFiltering->ipv4IPFilter[$index]->dataInfo['Enabled']['value'] = 1;
				$ipFiltering->ipv4IPFilter[$index]->dataInfo['Prefix']['value'] = 24;
				$ipFiltering->ipv4IPFilter[$index]->dataInfo['Address']['value'] = GetMyIPAddress($_SERVER['REMOTE_ADDR']);
				
				$ipFiltering->ipv4IPFilter[$index]->payload = MakePayload($ipFiltering->ipv4IPFilter[$index]->dataInfo);
			}
			
			$addMyIP = 1;	$index = -1;
			for ($i = 0; $i < MAX_IPV6_IPFILTER; ++$i)
			{
				if(CheckMyIP(6, $ipFiltering->ipv6IPFilter[$i]->dataInfo['Address']['value'], $ipFiltering->ipv6IPFilter[$i]->dataInfo['Prefix']['value']) == 1)
				{
					if($ipFiltering->defaultPolicy == 0)
					{
						$ipFiltering->ipv6IPFilter[$i]->dataInfo['Enabled']['value'] = 0;
						$ipFiltering->ipv6IPFilter[$i]->dataInfo['Address']['value'] = '';
						$ipFiltering->ipv6IPFilter[$i]->dataInfo['Prefix']['value'] = 128;
						$ipFiltering->ipv6IPFilter[$i]->payload = MakePayload($ipFiltering->ipv6IPFilter[$i]->dataInfo);
					}
					else
					{
						if($ipFiltering->ipv6IPFilter[$i]->dataInfo['Enabled']['value'] == 0)
						{
							$ipFiltering->ipv6IPFilter[$i]->dataInfo['Enabled']['value'] = 1;
							$ipFiltering->ipv6IPFilter[$i]->payload = MakePayload($ipFiltering->ipv6IPFilter[$i]->dataInfo);
						}
						
						$addMyIP = 0;
					}
				}
				
				if ($index == -1)
				{
					if ($ipFiltering->ipv6IPFilter[$i]->dataInfo['Address']['value'] == NULL)
					{
						$index = $i;
					}
				}
			}
			
			if($addMyIP == 1 && $ipFiltering->defaultPolicy == 1 && $classInstances['Information']->dataInfo['IPv6Enable']['value'] == 1)
			{
				if($index == -1)
				{
					$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
					return $responseOutput;
				}
				
				$myIPAddr = GetMyIPv6Address($_SERVER['REMOTE_ADDR']);
				$tmpMyIP = explode(':', $myIPAddr);
				$chkPoint = explode('::', $myIPAddr, -1);
				$preStr = '';
				
				if(count($tmpMyIP) < 8 && empty($chkPoint))
					$preStr = '::';
				
				$ipFiltering->ipv6IPFilter[$index]->dataInfo['Address']['value'] = $preStr . $myIPAddr;
				$ipFiltering->ipv6IPFilter[$index]->dataInfo['Enabled']['value'] = 1;
				$ipFiltering->ipv6IPFilter[$index]->dataInfo['Prefix']['value'] = 64;
				$ipFiltering->ipv6IPFilter[$index]->payload = MakePayload($ipFiltering->ipv6IPFilter[$index]->dataInfo);
			}

            $ipFiltering->headerInfo['Action'] = ACTION_SET;
            $ipFiltering->SetPayload();
            $GLOBALS['SOCKET_MANAGER']->Connection($ipFiltering);

            $responseOutput->outputMsg = 'OK';
        }
        else
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }
    }
    else if ($_REQUEST['action'] == 'add' || $_REQUEST['action'] == 'update')
    {
        if (!isset($_REQUEST['Enable']))
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        if ($_REQUEST['Enable'] != 'True' && $_REQUEST['Enable'] != 'False')
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }

        if ($_REQUEST['IPType'] == 'IPv4')
        {
            if ($_REQUEST['action'] == 'add')
            {
                for ($i = 0; $i < MAX_IPV4_IPFILTER; ++$i)
                {
                    if ($ipFiltering->ipv4IPFilter[$i]->dataInfo['Address']['value'] == $_REQUEST['Address'])
                    {
                        $responseOutput->errCode = STATUS_DUPLICATE_VALUE;
                        return $responseOutput;
                    }

                    if ($index == -1)
                    {
                        if ($ipFiltering->ipv4IPFilter[$i]->dataInfo['Address']['value'] == NULL)
                        {
                            $index = $i;
                        }
                    }
                }

                if ($index == -1)
                {
                    $responseOutput->errCode = STATUS_LIST_FULL;
                    return $responseOutput;
                }

                $responseOutput->outputMsg = 'OK' . "\r\n";
                $responseOutput->outputMsg .= 'IPIndex=' . ($index + 1);
            }
            else
            {
                if (isset($_REQUEST['Address']))
                {
                    for ($i = 0; $i < MAX_IPV4_IPFILTER; ++$i)
                    {
                        if ($i != $index && $ipFiltering->ipv4IPFilter[$i]->dataInfo['Address']['value'] == $_REQUEST['Address'])
                        {
                            $responseOutput->errCode = STATUS_DUPLICATE_VALUE;
                            return $responseOutput;
                        }
                    }
                }

                $responseOutput->outputMsg = 'OK';
            }

            if (isset($_REQUEST['Address']))
            {
                $ipFiltering->ipv4IPFilter[$index]->dataInfo['Address']['value'] = $_REQUEST['Address'];
            }

            $ipFiltering->ipv4IPFilter[$index]->dataInfo['Enabled']['value'] = array_search($_REQUEST['Enable'], $boolArray);

            if (isset($_REQUEST['Mask']))
            {
                $ipFiltering->ipv4IPFilter[$index]->dataInfo['Prefix']['value'] = $_REQUEST['Mask'];
            }
			
			if(CheckMyIP(4, $ipFiltering->ipv4IPFilter[$index]->dataInfo['Address']['value'], $ipFiltering->ipv4IPFilter[$index]->dataInfo['Prefix']['value']) == 1)
			{
				if($ipFiltering->defaultPolicy == 0 && $ipFiltering->ipv4IPFilter[$index]->dataInfo['Enabled']['value'] == 1)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				else if($ipFiltering->defaultPolicy == 1 && $ipFiltering->ipv4IPFilter[$index]->dataInfo['Enabled']['value'] == 0)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
			}

            $ipFiltering->ipv4IPFilter[$index]->payload = MakePayload($ipFiltering->ipv4IPFilter[$index]->dataInfo);
        }
        else //IPv6
        {
            if ($_REQUEST['action'] == 'add')
            {
                for ($i = 0; $i < MAX_IPV6_IPFILTER; ++$i)
                {
                    if ($ipFiltering->ipv6IPFilter[$i]->dataInfo['Address']['value'] == $_REQUEST['Address'])
                    {
                        $responseOutput->errCode = STATUS_DUPLICATE_VALUE;
                        return $responseOutput;
                    }

                    if ($index == -1)
                    {
                        if ($ipFiltering->ipv6IPFilter[$i]->dataInfo['Address']['value'] == NULL)
                        {
                            $index = $i;
                        }
                    }
                }

                if ($index == -1)
                {
                    $responseOutput->errCode = STATUS_LIST_FULL;
                    return $responseOutput;
                }

                $responseOutput->outputMsg = 'OK' . "\r\n";
                $responseOutput->outputMsg .= 'IPIndex=' . ($index + 1);
            }
            else
            {
                if (isset($_REQUEST['Address']))
                {
                    for ($i = 0; $i < MAX_IPV6_IPFILTER; ++$i)
                    {
                        if ($i != $index && $ipFiltering->ipv6IPFilter[$i]->dataInfo['Address']['value'] == $_REQUEST['Address'])
                        {
                            $responseOutput->errCode = STATUS_DUPLICATE_VALUE;
                            return $responseOutput;
                        }
                    }
                }

                $responseOutput->outputMsg = 'OK';
            }

            if (isset($_REQUEST['Address']))
            {
                $ipFiltering->ipv6IPFilter[$index]->dataInfo['Address']['value'] = $_REQUEST['Address'];
            }

            $ipFiltering->ipv6IPFilter[$index]->dataInfo['Enabled']['value'] = array_search($_REQUEST['Enable'], $boolArray);

            if (isset($_REQUEST['Mask']))
            {
                $ipFiltering->ipv6IPFilter[$index]->dataInfo['Prefix']['value'] = $_REQUEST['Mask'];
            }
			
			if(CheckMyIP(6, $ipFiltering->ipv6IPFilter[$index]->dataInfo['Address']['value'], $ipFiltering->ipv6IPFilter[$index]->dataInfo['Prefix']['value']) == 1 
				&& $classInstances['Information']->dataInfo['IPv6Enable']['value'] == 1)
			{
				if($ipFiltering->defaultPolicy == 0 && $ipFiltering->ipv6IPFilter[$index]->dataInfo['Enabled']['value'] == 1)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
				else if($ipFiltering->defaultPolicy == 1 && $ipFiltering->ipv6IPFilter[$index]->dataInfo['Enabled']['value'] == 0)
				{
					$responseOutput->errCode = STATUS_INVALID_VALUE;
					return $responseOutput;
				}
			}

            $ipFiltering->ipv6IPFilter[$index]->payload = MakePayload($ipFiltering->ipv6IPFilter[$index]->dataInfo);
        }

        $ipFiltering->headerInfo['Action'] = ACTION_SET;
        $ipFiltering->SetPayload();
        $GLOBALS['SOCKET_MANAGER']->Connection($ipFiltering);
    }
    else if ($_REQUEST['action'] == 'remove')
    {
        if ($_REQUEST['IPType'] == 'IPv4')
        {
			if($ipFiltering->defaultPolicy == 1 && CheckMyIP(4, $ipFiltering->ipv4IPFilter[$index]->dataInfo['Address']['value'], $ipFiltering->ipv4IPFilter[$index]->dataInfo['Prefix']['value']) == 1
				&& $ipFiltering->ipv4IPFilter[$index]->dataInfo['Enabled']['value'] == 1)
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}
			
            $ipFiltering->ipv4IPFilter[$index]->dataInfo['Enabled']['value'] = 0;
            $ipFiltering->ipv4IPFilter[$index]->dataInfo['Address']['value'] = '';
            $ipFiltering->ipv4IPFilter[$index]->dataInfo['Prefix']['value'] = 32;

            $ipFiltering->ipv4IPFilter[$index]->payload = MakePayload($ipFiltering->ipv4IPFilter[$index]->dataInfo);
        }
        else if ($_REQUEST['IPType'] == 'IPv6')
        {
			if($ipFiltering->defaultPolicy == 1 && CheckMyIP(6, $ipFiltering->ipv6IPFilter[$index]->dataInfo['Address']['value'], $ipFiltering->ipv6IPFilter[$index]->dataInfo['Prefix']['value']) == 1
				&& $classInstances['Information']->dataInfo['IPv6Enable']['value'] == 1 && $ipFiltering->ipv6IPFilter[$index]->dataInfo['Enabled']['value'] == 1)
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}
			
            $ipFiltering->ipv6IPFilter[$index]->dataInfo['Enabled']['value'] = 0;
            $ipFiltering->ipv6IPFilter[$index]->dataInfo['Address']['value'] = '';
            $ipFiltering->ipv6IPFilter[$index]->dataInfo['Prefix']['value'] = 128;

            $ipFiltering->ipv6IPFilter[$index]->payload = MakePayload($ipFiltering->ipv6IPFilter[$index]->dataInfo);
        }

        $ipFiltering->headerInfo['Action'] = ACTION_SET;
        $ipFiltering->SetPayload();
        $GLOBALS['SOCKET_MANAGER']->Connection($ipFiltering);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
        $ipv4Msg = $ipv6Msg = '';

        for ($index = 0; $index < MAX_IPV4_IPFILTER; ++$index)
        {
            if ($ipFiltering->ipv4IPFilter[$index]->dataInfo['Address']['value'] != NULL)
            {
                $ipv4Msg .= 'ipfilter.IPv4.' . ($index + 1) . '=' . $ipFiltering->ipv4IPFilter[$index]->dataInfo['Address']['value'] . '/' . $ipFiltering->ipv4IPFilter[$index]->dataInfo['Prefix']['value']
                    . '/' . $boolArray[$ipFiltering->ipv4IPFilter[$index]->dataInfo['Enabled']['value']] . "\r\n";
            }

            if ($ipFiltering->ipv6IPFilter[$index]->dataInfo['Address']['value'] != NULL)
            {
                $ipv6Msg .= 'ipfilter.IPv6.' . ($index + 1) . '=' . $ipFiltering->ipv6IPFilter[$index]->dataInfo['Address']['value'] . '/' . $ipFiltering->ipv6IPFilter[$index]->dataInfo['Prefix']['value']
                    . '/' . $boolArray[$ipFiltering->ipv6IPFilter[$index]->dataInfo['Enabled']['value']] . "\r\n";
            }
        }

        $responseOutput->outputMsg = '"ipfilter.IPType.IPIndex=Address/Mask/Enable"' . "\r\n";

        $responseOutput->outputMsg .= 'AccessType=' . $AccessTypeArr[$ipFiltering->defaultPolicy] . "\r\n";
        $responseOutput->outputMsg .= $ipv4Msg . "\r\n";
        $responseOutput->outputMsg .= $ipv6Msg . "\r\n";
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

// 802.1x
function submenu_802Dot1x()
{
	$EAPType = array(
			0 => 'EAP-TLS',
			1 => 'LEAP',
	);
	
    CheckAdminAccount(FALSE);
    $responseOutput = new ResponseOutput();

    $classInstances = GetClassInstance('8021x');

    global $boolArray;

    if ($_REQUEST['action'] == 'set')
    {
        $dataNameArr = array('InterfaceName' => '', 'Enable' => 'Enabled', 'EAPOLType' => 'EAPType', 'EAPOLVersion' => 'EapolVersion', 'EAPOLId' => 'EapID', 'EAPOLPassword' => 'PrivateKeyPassword');

        foreach ($dataNameArr as $param => $data)
        {
            if (!isset($_REQUEST[$param]))
            {
                continue;
            }

            if ($param == 'InterfaceName')
            {
                $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                return $responseOutput;
            }

            if	($param == 'EAPOLType')
            {
            	 /** WN3_PTZ Does not support */
            	if ($GLOBALS['M_ISP_TYPE'] == ISP_TYPE_WN3_PTZ && $_REQUEST[$param] == 'LEAP')
            	{
            		$responseOutput->errCode = STATUS_INVALID_VALUE;
            		return $responseOutput;
            	}	
            	
            	/** Invalid Checking */
            	if($_REQUEST[$param] != 'EAP-TLS' && $_REQUEST[$param] != 'LEAP')
            	{
            		$responseOutput->errCode = STATUS_INVALID_VALUE;
            		return $responseOutput;
            	}
            }
            
            if ($param == 'Enable')
            {
                if($_REQUEST[$param] != 'True' && $_REQUEST[$param] != 'False')
                {
                    $responseOutput->errCode = STATUS_INVALID_VALUE;
                    return $responseOutput;
                }
                
                $classInstances['Configuration802Dot1x']->dataInfo[$data]['value'] = array_search($_REQUEST[$param], $boolArray);
            }
            else if ($param == 'EAPOLType')
            {
            	$classInstances['Configuration802Dot1x']->dataInfo[$data]['value'] = array_search($_REQUEST[$param], $EAPType);
            }
            else
            {
                $classInstances['Configuration802Dot1x']->setting802Dot1x->dataInfo[$data]['value'] = $_REQUEST[$param];
            }
        }

        $classInstances['Configuration802Dot1x']->headerInfo['Action'] = ACTION_SET;
        $classInstances['Configuration802Dot1x']->setting802Dot1x->payload = MakePayload($classInstances['Configuration802Dot1x']->setting802Dot1x->dataInfo);
        $classInstances['Configuration802Dot1x']->SetPayload();
        $GLOBALS['SOCKET_MANAGER']->Connection($classInstances['Configuration802Dot1x']);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_GET['action'] == 'install')
    {
        $targetClass = new Data802Dot1x();
        
        $xmlInfo = CheckXMLMessage();
        
        $targetClass->headerInfo['Action'] = ACTION_SET;
		$targetClass->XMLtoArray($xmlInfo['menu']);
        
        $typeArr = array(1 => 'CACertificate', 2 => 'ClientCertificate', 3 => 'ClientPrivateKey');
        $targetClass->publicCertType = array_search($targetClass->publicCertType, $typeArr);
        
        $targetClass->SetPayload();
		$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
        
        $responseOutput->outputMsg = 'OK';
    }
    else if ($_GET['action'] == 'remove')
    {
        $targetClass = new Data802Dot1x();
        
        if(isset($_GET['CertificateType']))
        {
            $typeArr = array(1 => 'CACertificate', 2 => 'ClientCertificate', 3 => 'ClientPrivateKey');
            $targetClass->publicCertType = array_search($_GET['CertificateType'], $typeArr);
        }
        else
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }
        
        $targetClass->headerInfo['Action'] = ACTION_REMOVE;
		$targetClass->payload = pack('c1', $targetClass->publicCertType);
        $GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
        
        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
        $responseOutput->outputMsg = 'InterfaceName=' . trim($classInstances['Configuration802Dot1x']->dataInfo['InterfaceToken']['value']) . "\r\n";
        $responseOutput->outputMsg .= 'Enable=' . $boolArray[$classInstances['Configuration802Dot1x']->dataInfo['Enabled']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'EAPOLType=' . $EAPType[$classInstances['Configuration802Dot1x']->dataInfo['EAPType']['value']] . "\r\n";
        
                       
        $statusArr = array(0 => 'Stopped', 1 => 'Unauthorized', 2 => 'Authorized', 3 => 'Unknown');
        $responseOutput->outputMsg .= 'Status=' . $statusArr[$classInstances['Configuration802Dot1x']->dataInfo['Status']['value']] . "\r\n";
        
        $responseOutput->outputMsg .= 'CACertificateInstalled=' . $boolArray[$classInstances['Configuration802Dot1x']->certificate802Dot1x->dataInfo['CaCertificate']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'ClientCertificateInstalled=' . $boolArray[$classInstances['Configuration802Dot1x']->certificate802Dot1x->dataInfo['ClientCertificate']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'ClientPrivateKeyInstalled=' . $boolArray[$classInstances['Configuration802Dot1x']->certificate802Dot1x->dataInfo['ClientPrivateKey']['value']] . "\r\n";

        $responseOutput->outputMsg .= 'EAPOLVersion=' . $classInstances['Configuration802Dot1x']->setting802Dot1x->dataInfo['EapolVersion']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'EAPOLId=' . $classInstances['Configuration802Dot1x']->setting802Dot1x->dataInfo['EapID']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'EAPOLPassword=' . $classInstances['Configuration802Dot1x']->setting802Dot1x->dataInfo['PrivateKeyPassword']['value'] . "\r\n";
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

// rtsp
function submenu_rtsp()
{
    $responseOutput = new ResponseOutput();

    CheckAdminAccount(FALSE);
    $classInstances = GetClassInstance('user');
    $userConf = $classInstances['UserConfiguration']->user[11];

    if ($_REQUEST['action'] == 'set')
    {
        if (isset($_REQUEST['RTSPAuthentication']))
        {
			if($_REQUEST['RTSPAuthentication'] != 'Anonymous' && $_REQUEST['RTSPAuthentication'] != 'Protected')
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}
			
            $userConf->dataInfo['UserRightProfile']['value'] = ($_REQUEST['RTSPAuthentication'] == 'Anonymous' ? 1 : 0);
        }
        else
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $userConf->payload = MakePayload($userConf->dataInfo);

        $classInstances['UserConfiguration']->headerInfo['Action'] = ACTION_SET;
        $classInstances['UserConfiguration']->SetPayload();
        $GLOBALS['SOCKET_MANAGER']->Connection($classInstances['UserConfiguration']);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
        $responseOutput->outputMsg = 'RTSPAuthentication=' . ($userConf->dataInfo['UserRightProfile']['value'] == 1 ? 'Anonymous' : 'Protected') . "\r\n";
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

// SSL
function submenu_ssl()
{
    CheckAdminAccount(FALSE);
    $responseOutput = new ResponseOutput();

    $classInstances = GetClassInstance('https');
    $PolicyArr = array(0 => 'HTTP', 1 => 'HTTPSProprietary', 2 => 'HTTPSPublic');

    $allowed_params = array("msubmenu", "action", "PublicCertificateInstalled", "Policy", "PublicCertificateName");

    if(CheckAllowedParams($allowed_params) === FALSE)
    {
		$responseOutput->errCode = STATUS_INVALID_PARAMETER;
		return $responseOutput;
	}

    if ($_REQUEST['action'] == 'set')
    {
        if (!isset($_REQUEST['Policy']))
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        if(array_search($_REQUEST['Policy'], $PolicyArr) === FALSE)
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }

		/* Can't be changed to HTTPSpublic Mode without PublicCertificate */
        if((strlen($classInstances['HTTPSConfiguration']->dataInfo['PublicCertName']['value'])) == 0)
        {
        	if($_REQUEST['Policy'] == "HTTPSPublic")
        	{
				/* new errCode message will be added */
	            $responseOutput->errCode = STATUS_UNKNOWN_ERROR;
	            return $responseOutput;
        	}
        }

        $classInstances['HTTPSConfiguration']->dataInfo['Mode']['value'] = array_search($_REQUEST['Policy'], $PolicyArr);

        $classInstances['HTTPSConfiguration']->headerInfo['Action'] = ACTION_SET;
        $classInstances['HTTPSConfiguration']->payload = MakePayload($classInstances['HTTPSConfiguration']->dataInfo);
        $GLOBALS['SOCKET_MANAGER']->Connection($classInstances['HTTPSConfiguration']);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_GET['action'] == 'install')
    {
        $targetClass = new HTTPSData();
        
        $xmlInfo = CheckXMLMessage();
        
        $targetClass->headerInfo['Action'] = ACTION_SET;
		$targetClass->XMLtoArray($xmlInfo['menu']);
        
		$GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
        
        $responseOutput->outputMsg = 'OK';
    }
    else if ($_GET['action'] == 'remove')
    {
        $targetClass = new HTTPSData();
        
		/* Can't work remove action if there is no PublicCertificate */
        if((strlen($classInstances['HTTPSConfiguration']->dataInfo['PublicCertName']['value'])) == 0)
        {
        	/* new errCode message will be added */
        	$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
			return $responseOutput;
        }

		/* PublicCertificate only can be removed when 'Secure connection system' is not HTTPSPublic */
        if($PolicyArr[$classInstances['HTTPSConfiguration']->dataInfo['Mode']['value']] != "HTTPSPublic")
        {
	        if(isset($_GET['PublicCertificateName']))
			{
				$targetClass->publicCertName = $_GET['PublicCertificateName'];
	        }
			else
			{
				/* new errCode message will be added */
				$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
				return $responseOutput;
			}
        }
        else
        {
        	$responseOutput->errCode = STATUS_UNKNOWN_ERROR;
    	    return $responseOutput;
        }
        
        $targetClass->headerInfo['Action'] = ACTION_REMOVE;
		$targetClass->payload = pack('a32', $targetClass->publicCertName);
        $GLOBALS['SOCKET_MANAGER']->Connection($targetClass);
        
        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
        $responseOutput->outputMsg = 'PublicCertificateInstalled=' . (strlen($classInstances['HTTPSConfiguration']->dataInfo['PublicCertName']['value']) ? 'True' : 'False') . "\r\n";
        $responseOutput->outputMsg .= 'Policy=' . $PolicyArr[$classInstances['HTTPSConfiguration']->dataInfo['Mode']['value']] . "\r\n";

      /*  if (strlen($classInstances['HTTPSConfiguration']->dataInfo['PublicCertName']['value']) != 0)
        { */
            $responseOutput->outputMsg .= 'PublicCertificateName=' . trim($classInstances['HTTPSConfiguration']->dataInfo['PublicCertName']['value']) . "\r\n";
       // }
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

// Guest
function submenu_guest()
{
    $responseOutput = new ResponseOutput();

    CheckAdminAccount(FALSE);
    $classInstances = GetClassInstance('user');
    $userConf = $classInstances['UserConfiguration']->user[11];

    global $boolArray;

    if ($_REQUEST['action'] == 'set')
    {
        if (isset($_REQUEST['Enable']))
        {
			if($_REQUEST['Enable'] != 'True' && $_REQUEST['Enable'] != 'False')
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
				return $responseOutput;
			}
			
            $userConf->dataInfo['Enabled']['value'] = array_search($_REQUEST['Enable'], $boolArray);
            $userConf->payload = MakePayload($userConf->dataInfo);

            $classInstances['UserConfiguration']->headerInfo['Action'] = ACTION_SET;
            $classInstances['UserConfiguration']->SetPayload();
            $GLOBALS['SOCKET_MANAGER']->Connection($classInstances['UserConfiguration']);

            $responseOutput->outputMsg = 'OK';
        }
        else
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }
    }
    else if ($_REQUEST['action'] == 'view')
    {
        $responseOutput->outputMsg = 'Enable=' . $boolArray[$userConf->dataInfo['Enabled']['value']] . "\r\n";
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

// camerausers
function submenu_users()
{
    $responseOutput = new ResponseOutput();

    $classInstances = GetClassInstance('user');

    global $boolArray;

    $max_user = MAX_USER_10;

    $allowed_params = array("msubmenu", "action", "UserID", "Index", "UserName", "Enable", "VideoProfileAccess", "PTZAccess", "AudioInAccess", "AudioOutAccess", "AlarmOutputAccess", "ViewerAccess", "Password", "GroupID");

    if(CheckAllowedParams($allowed_params) === FALSE)
    {
    	$responseOutput->errCode = STATUS_INVALID_PARAMETER;
        return $responseOutput;
	}

    if (($_REQUEST['UserID'] == 'admin' || (isset($_REQUEST['Index']) && $_REQUEST['Index'] == 0)) && ($_REQUEST['action'] != 'update' && $_REQUEST['action'] != 'view'))
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    if (isset($_REQUEST['Index']) && ($_REQUEST['Index'] < 0 || $_REQUEST['Index'] > ($max_user - 2)))
    {
        $responseOutput->errCode = STATUS_INVALID_VALUE;
        return $responseOutput;
    }

    if ($_REQUEST['action'] == 'add')
    {
        if (!isset($_REQUEST['UserID']) || !isset($_REQUEST['Password']))
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $index = -1;
        for ($i = 1; $i < ($max_user - 1); ++$i)
        {
            if ($classInstances['UserConfiguration']->user[$i]->dataInfo['Name']['value'] == $_REQUEST['UserID'])
            {
                $responseOutput->errCode = STATUS_DUPLICATE_VALUE;
                return $responseOutput;
            }

            if ($index == -1)
            {
                if ($classInstances['UserConfiguration']->user[$i]->dataInfo['Name']['value'] == NULL || !isset($classInstances['UserConfiguration']->user[$i]->dataInfo['Name']['value']))
                {
                    $index = $i;
                }
            }
        }

        if ($index == -1)
        {
            $responseOutput->errCode = STATUS_LIST_FULL;
            return $responseOutput;
        }
        
        $responseOutput->outputMsg = 'OK' . "\r\n";
        $responseOutput->outputMsg .= 'Index=' . $index;
    }
    else if ($_REQUEST['action'] == 'update')
    {
        if (!isset($_REQUEST['Index']) || !isset($_REQUEST['UserID']) || !isset($_REQUEST['Password']))
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }

        $index = (int)$_REQUEST['Index'];

        for ($i = 0; $i < ($max_user - 1); ++$i)
        {
            if ($i != $index && $classInstances['UserConfiguration']->user[$i]->dataInfo['Name']['value'] == $_REQUEST['UserID'])
            {
                $responseOutput->errCode = STATUS_DUPLICATE_VALUE;
                return $responseOutput;
            }
        }

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'remove')
    {
        if (isset($_REQUEST['Index']))
        {
            $index = (int)$_REQUEST['Index'];
        }
        else if (isset($_REQUEST['UserID']))
        {
            $index = -1;
            for ($i = 0; $i < ($max_user - 1); ++$i)
            {
                if ($classInstances['UserConfiguration']->user[$i]->dataInfo['Name']['value'] == $_REQUEST['UserID'])
                {
                    $index = $i;
                    break;
                }
            }

            if ($index == -1)
            {
                $responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
            }
        }
        else
        {
            $responseOutput->errCode = STATUS_MISSING_PARAMETER;
            return $responseOutput;
        }
    }

    if ($_REQUEST['action'] == 'add' || $_REQUEST['action'] == 'update')
    {
        CheckAdminAccount(FALSE);
        
        if($_REQUEST['UserID'] == NULL || $_REQUEST['Password'] == NULL)
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }
        
        if (strlen($_REQUEST['UserID']) > 8 || strlen($_REQUEST['Password']) > 15)
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }

        $userConf = $classInstances['UserConfiguration']->user[$index];

        if ($_REQUEST['action'] == 'update' && $userConf->dataInfo['Name']['value'] == NULL)
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }
        
        if ($index == 0 && ($_REQUEST['UserID'] != 'admin'))
        {
            $responseOutput->errCode = STATUS_INVALID_VALUE;
            return $responseOutput;
        }

        $userConf->dataInfo['Name']['value'] = $_REQUEST['UserID'];
        $userConf->dataInfo['Password']['value'] = $_REQUEST['Password'];

        $userParamArr = array('Enable' => 'Enabled', 'VideoProfileAccess' => 'UserRightProfile', 'PTZAccess' => 'UserRightPTZ', 'AudioInAccess' => 'UserRightAudioIn'
            , 'AudioOutAccess' => 'UserRightAudioOut', 'AlarmOutputAccess' => 'UserRightRelay');

        foreach ($userParamArr as $param => $data)
        {
            if (isset($_REQUEST[$param]))
            {
                if ($_REQUEST['UserID'] == 'admin')
                {
                    $responseOutput->errCode = STATUS_INVALID_PARAMETER;
                    return $responseOutput;
                }

                if ($_REQUEST[$param] != 'True' && $_REQUEST[$param] != 'False')
                {
                    $responseOutput->errCode = STATUS_INVALID_VALUE;
                    return $responseOutput;
                }

                if (($param == 'AudioInAccess' || $param == 'AudioOutAccess') && $GLOBALS['M_SUPPORT_AUDIO'] == 0)
                {
                    $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                    return $responseOutput;
                }

                if ($param == 'AlarmOutputAccess' && $GLOBALS['M_ALARMOUT_COUNT'] == 0)
                {
                    $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                    return $responseOutput;
                }

                if ($param == 'PTZAccess' && ($GLOBALS['M_SUPPORT_EXTERNAL_PTZ'] == 0 && $GLOBALS['M_SUPPORT_PTZ'] == 0))
                {
                    $responseOutput->errCode = STATUS_NOT_IMPLEMENTED;
                    return $responseOutput;
                }

                $userConf->dataInfo[$data]['value'] = array_search($_REQUEST[$param], $boolArray);
            }
        }

        $userConf->payload = MakePayload($userConf->dataInfo);

        $classInstances['UserConfiguration']->headerInfo['Action'] = ACTION_SET;
        $classInstances['UserConfiguration']->SetPayload();
        $GLOBALS['SOCKET_MANAGER']->Connection($classInstances['UserConfiguration']);
    }
    else if ($_REQUEST['action'] == 'remove')
    {
        CheckAdminAccount(FALSE);
        
        $classInstances['UserConfiguration']->user[$index]->payload = MakePayload($classInstances['UserConfiguration']->user[$index]->dataInfo);

        $classInstances['UserConfiguration']->headerInfo['Action'] = ACTION_REMOVE;
        $classInstances['UserConfiguration']->SetPayloadForAddRemove($index);
        $GLOBALS['SOCKET_MANAGER']->Connection($classInstances['UserConfiguration']);

        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
        $responseOutput->outputMsg = '"Users.Index=UserID/Password/Enable/VideoProfileAccess/PTZAccess/AudioInAccess/AudioOutAccess/AlarmOutputAccess"' . "\r\n";

        if (isset($_REQUEST['UserID']))
        {			
			SetUserInfo($classInstances['UserConfiguration']->user);
			
			if($GLOBALS['USERINFO']['name'] != "admin" && $GLOBALS['USERINFO']['name'] != $_REQUEST['UserID'])
			{
				$responseOutput->errCode = STATUS_INVALID_VALUE;
                return $responseOutput;
			}
            
            for ($index = 0; $index < ($max_user - 1); ++$index)
            {           	
                if ($classInstances['UserConfiguration']->user[$index]->dataInfo['Name']['value'] == $_REQUEST['UserID'])
                {
                    $userConf = $classInstances['UserConfiguration']->user[$index];

                    $newPassword = str_replace("/", "&", $userConf->dataInfo['Password']['value']);

                    $responseOutput->outputMsg .= 'Users.' . $index . '=' . $userConf->dataInfo['Name']['value'] . '/' .$newPassword . '/'
                        . $boolArray[$userConf->dataInfo['Enabled']['value']] . '/' . $boolArray[$userConf->dataInfo['UserRightProfile']['value']] . '/';

                    if ($GLOBALS['M_SUPPORT_EXTERNAL_PTZ'] || $GLOBALS['M_SUPPORT_PTZ'])
                    {
                        $responseOutput->outputMsg .= $boolArray[$userConf->dataInfo['UserRightPTZ']['value']];
                    }

                    $responseOutput->outputMsg .= '/';

                    if ($GLOBALS['M_SUPPORT_AUDIO'])
                    {
                        $responseOutput->outputMsg .= $boolArray[$userConf->dataInfo['UserRightAudioIn']['value']] . '/';

	                    if ($GLOBALS['M_SUPPORT_AUDIO_OUT'])
	                    {
	                        $responseOutput->outputMsg .= $boolArray[$userConf->dataInfo['UserRightAudioOut']['value']] . '/';
	                    }
	                    else
	                    {
	                        $responseOutput->outputMsg .= '/';
	                    }						
                    }
                    else
                    {
                        $responseOutput->outputMsg .= '//';
                    }

                    if ($GLOBALS['M_ALARMOUT_COUNT'])
                    {
                        $responseOutput->outputMsg .= $boolArray[$userConf->dataInfo['UserRightRelay']['value']];
                    }

                    $responseOutput->outputMsg .= "\r\n";

                    break;
                }
            }
        }
        else
        {			
            SetUserInfo($classInstances['UserConfiguration']->user);
			
            for ($index = 0; $index < ($max_user - 1); ++$index)
            {	
                $userConf = $classInstances['UserConfiguration']->user[$index];

                if($GLOBALS['USERINFO']['name'] != admin && $userConf->dataInfo['Name']['value'] != $GLOBALS['USERINFO']['name'])
                {
					continue;
                }

                if ($userConf->dataInfo['Name']['value'] == NULL)
                {
                    continue;
                }

                $newPassword = str_replace("/", "&", $userConf->dataInfo['Password']['value']);

                $responseOutput->outputMsg .= 'Users.' . $index . '=' . $userConf->dataInfo['Name']['value'] . '/' . $newPassword . '/'
                                            . $boolArray[$userConf->dataInfo['Enabled']['value']] . '/' . $boolArray[$userConf->dataInfo['UserRightProfile']['value']] . '/';

                if ($GLOBALS['M_SUPPORT_EXTERNAL_PTZ'] || $GLOBALS['M_SUPPORT_PTZ'])
                {
                    $responseOutput->outputMsg .= $boolArray[$userConf->dataInfo['UserRightPTZ']['value']];
                }

                $responseOutput->outputMsg .= '/';

                if ($GLOBALS['M_SUPPORT_AUDIO'])
                {
                    $responseOutput->outputMsg .= $boolArray[$userConf->dataInfo['UserRightAudioIn']['value']] . '/';

                    if ($GLOBALS['M_SUPPORT_AUDIO_OUT'])
                    {
                        $responseOutput->outputMsg .= $boolArray[$userConf->dataInfo['UserRightAudioOut']['value']] . '/';
                    }
                    else
                    {
                        $responseOutput->outputMsg .= '/';
                    }						
                }
                else
                {
                    $responseOutput->outputMsg .= '//';
                }

                if ($GLOBALS['M_ALARMOUT_COUNT'])
                {
                    $responseOutput->outputMsg .= $boolArray[$userConf->dataInfo['UserRightRelay']['value']];
                }

                $responseOutput->outputMsg .= "\r\n";
            }
        }
    }

    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

// msubmenu
switch (@$_REQUEST['msubmenu'])
{
    case 'ipfilter':
        {
            if ($_REQUEST['action'] != 'view' && $_REQUEST['action'] != 'set' && $_REQUEST['action'] != 'remove' && $_REQUEST['action'] != 'add' && $_REQUEST['action'] != 'update')
            {
                $responseOutput = new ResponseOutput();
                $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
                SendResponse($responseOutput);
            }

            SendResponse(submenu_ipfilter());
        } break;
    case '802Dot1x': case 'ssl':
        {
            if ($_REQUEST['action'] != 'view' && $_REQUEST['action'] != 'set' && $_REQUEST['action'] != 'install' && $_REQUEST['action'] != 'remove')
            {
                $responseOutput = new ResponseOutput();
                $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
                SendResponse($responseOutput);
            }

            $funcName = 'submenu_' . $_REQUEST['msubmenu'];
            SendResponse($funcName());
        }
    case 'rtsp': case 'guest':
        {
            if ($_REQUEST['action'] != 'view' && $_REQUEST['action'] != 'set')
            {
                $responseOutput = new ResponseOutput();
                $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
                SendResponse($responseOutput);
            }

            $funcName = 'submenu_' . $_REQUEST['msubmenu'];
            SendResponse($funcName());
        }
    case 'users':
        {
            if ($_REQUEST['action'] != 'view' && $_REQUEST['action'] != 'add' && $_REQUEST['action'] != 'update' && $_REQUEST['action'] != 'remove')
            {
                $responseOutput = new ResponseOutput();
                $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
                SendResponse($responseOutput);
            }

            $funcName = 'submenu_' . $_REQUEST['msubmenu'];
            SendResponse($funcName());
        }
    default:
        {
            $responseOutput = new ResponseOutput();
            $responseOutput->errCode = STATUS_SUBMENU_NOT_FOUND;
            SendResponse($responseOutput);
        }
}
?>
