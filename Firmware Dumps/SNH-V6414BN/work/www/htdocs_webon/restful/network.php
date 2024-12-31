<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/datetime_constant.php";

define("OFF_DNS"        , 65);
define("OFF_NETWORK"    , 230);
define("OFF_GATEWAY"    , 1588);
define("OFF_WLAN", 909);
define("OFF_NETWORK_CHANGED",   11709);
define("HOSTNAME_SETTING_SIZE", 65);
define("DNS_SETTING_SIZE", 165);
define("INTERFACE_SETTING_SIZE", 387);

switch ($_SERVER['REQUEST_METHOD']) {
  case "GET":
    $result_network_config_v2 = requestToCamera(CMD_NETWORK_CONFIGURATION_V2, ACTION_GET, TYPE_REQUEST, null);
    $result_network_if_extention = requestToCamera(CMD_NETWORK_IF_EXTENSION, ACTION_GET, TYPE_REQUEST, null);
    $fromdhcp = 0; $dns1 = array(); $dns2 = array(); $ipAddress = array(); $dhcp_static = 0;
    $subnet = array(); $prefix = array(); $gateway = "";
    $useWLAN = 0; $ssid = ""; $currentPW = "";
    $error = "";
    if ($result_network_config_v2[0] == "OK") {
      $mac = byte2str($result_network_config_v2[1], OFF_NETWORK+65, 18);  //MAC
      $fromdhcp = $result_network_config_v2[1][OFF_NETWORK+84];   //DHCP?
      $dns1[1] = byte2str($result_network_config_v2[1], OFF_DNS+84, 40);          //DHCP dns1
      $dns2[1] = byte2str($result_network_config_v2[1], OFF_DNS+125, 40);         //DHCP dns2
      $dns1[0] = byte2str($result_network_config_v2[1], OFF_DNS+2, 40);               //Static dns1
      $dns2[0] = byte2str($result_network_config_v2[1], OFF_DNS+43, 40);          //Static dns2
      $ipAddress[0] = byte2str($result_network_config_v2[1], OFF_NETWORK+85, 16); //Static ip
      $ipAddress[1] = byte2str($result_network_config_v2[1], OFF_NETWORK+105, 16);    //DHCP ip
      $prefix[0] = byte2int($result_network_config_v2[1], OFF_NETWORK+101);           //Static    subnetmask
      $prefix[1] = byte2int($result_network_config_v2[1], OFF_NETWORK+121);           //DHCP subnetmask
      for ($i=0; $i<2; $i++) {
        if ($prefix[$i] == 8) {
          $subnet[$i] = "255.0.0.0";
        } else if ($prefix[$i] == 16) {
          $subnet[$i] = "255.255.0.0";
        } else if($prefix[$i] == 24) {
          $subnet[$i] = "255.255.255.0";
        } else if($prefix[$i] == 32) {
          $subnet[$i] = "255.255.255.255";
        } else {
          $subnet[$i] = "0.0.0.0";
        }
      }
      $gateway = byte2str($result_network_config_v2[1], OFF_GATEWAY, 16); //gateway

      if ($fromdhcp == 1) {
        $fromdhcp = "true";
        $dhcp_static = 1;
      } else {
        $fromdhcp = "false";
        $dhcp_static = 0;
      }

      //wireless
      $useWLAN = $result_network_if_extention[1][681];
      $ssid = byte2str($result_network_if_extention[1], 64, 128);
      $security = $result_network_if_extention[1][325];

      switch ($useWLAN) {
        case "0":
          $useWLAN = "Wired";
          break;
        case "1":
          $useWLAN = "Wireless";
          break;
        default;
        break;
      }

      switch ($security) {
        case "0":
          $security = "OPEN";
          break;
        case "1":
          $security = "WEP";
          break;
        case "2":
          $security = "WPA";
          break;
        default;
        break;
      }

      $xw = new xmlWriter();
      $xw->openMemory();
      $xw->startDocument('1.0','UTF-8');
      $xw->startElement ('Network');
      $xw->writeElement ('connectedNetwork', $useWLAN);
      $xw->startElement ('wired');
      $xw->writeElement ('fromDHCP', $fromdhcp);
      $xw->writeElement ('mac', $mac);
      $xw->writeElement ('ip', $ipAddress[$dhcp_static]);
      $xw->writeElement ('gateway', $gateway);
      $xw->writeElement ('subnetmask', $subnet[$dhcp_static]);
      $xw->writeElement ('dns1', $dns1[$dhcp_static]);
      if ($dns2[$dhcp_static] != "")
        $xw->writeElement ('dns2', $dns2[$dhcp_static]);
      $xw->endElement();
      $xw->startElement ('wireless');
      $xw->writeElement ('fromDHCP', $fromdhcp);
      $xw->writeElement ('mac', $mac);
      $xw->writeElement ('ip', $ipAddress[$dhcp_static]);
      $xw->writeElement ('gateway', $gateway);
      $xw->writeElement ('subnetmask', $subnet[$dhcp_static]);
      $xw->writeElement ('dns1', $dns1[$dhcp_static]);
      if ($dns2[$dhcp_static] != "")
        $xw->writeElement ('dns2', $dns2[$dhcp_static]);
      $xw->writeElement ('ssid', $ssid);
      $xw->writeElement ('security', $security);
      $xw->endElement();
      $xw->endElement();
      $xw->endDocument();

      header("Content-type: application/xml");
      echo $xw->outputMemory(true);
    } else {
      header("HTTP/1.1 501 Not Implemented");
    }
    break;

  case "PUT":

    //input XML
    $xml = file_get_contents('php://input');

    //XML Parser
    require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/DMC_xmlParser.php";

    $parser = new XMLParser($xml);
    $parser->Parse();
    $selectedNetwork = $parser->document->selectednetwork[0]->tagData;
    $wired_fromdhcp = $parser->document->wired[0]->fromdhcp[0]->tagData;
    $wired_ip = $parser->document->wired[0]->ip[0]->tagData;
    $wired_gateway = $parser->document->wired[0]->gateway[0]->tagData;
    $wired_subnetmask = $parser->document->wired[0]->subnetmask[0]->tagData;
    $wired_dns1 = $parser->document->wired[0]->dns1[0]->tagData;
    $wired_dns2 = $parser->document->wired[0]->dns2[0]->tagData;

    $wireless_ip = $parser->document->wireless[0]->ip[0]->tagData;
    $wireless_gateway = $parser->document->wireless[0]->gateway[0]->tagData;
    $wireless_subnetmask = $parser->document->wireless[0]->subnetmask[0]->tagData;
    $wireless_dns1 = $parser->document->wireless[0]->dns1[0]->tagData;
    $wireless_dns2 = $parser->document->wireless[0]->dns2[0]->tagData;
    $ssid = $parser->document->wireless[0]->ssid[0]->tagData;
    $password = $parser->document->wireless[0]->password[0]->tagData;
    $security = $parser->document->wireless[0]->security[0]->tagData;

    if ($wired_fromdhcp == "true") {
      $wired_fromdhcp = 1;
    } else {
      $wired_fromdhcp = 0;
    }
    $network_v2 = array_fill(0, 8587, 0x00);  // CMD_NETWORK_CONFIGURATION_V2 size = 8587
    $network_wireless = array_fill(0, 5830, 0x00);  //  CMD_NETWORK_IF_EXTENSION size = 5830

    $result_network_config_v2 = requestToCamera(CMD_NETWORK_CONFIGURATION_V2, ACTION_GET, TYPE_REQUEST, null);
    $result_network_if_extention = requestToCamera(CMD_NETWORK_IF_EXTENSION, ACTION_GET, TYPE_REQUEST, null);

    $network_v2 = $result_network_config_v2[1];
    $network_wireless = $result_network_if_extention[1];
    switch ($selectedNetwork){
      case "Wired":
        $network_v2[OFF_NETWORK+84] = $wired_fromdhcp;
        if ($wired_fromdhcp == "0") {
          str2byte($network_v2, $wired_dns1, OFF_DNS+2, 40);      //DNS 1
          str2byte($network_v2, $wired_dns2, OFF_DNS+43, 40);     //DNS 2
          str2byte($network_v2, $wired_ip, OFF_NETWORK+85, 16);   //IP Address
          str2byte($network_v2, $wired_gateway, OFF_GATEWAY, 16);     //Gateway
        }
        break;
      case "Wireless":
        ini_set("max_execution_time", 20);
        $wireless_enable = HOSTNAME_SETTING_SIZE + DNS_SETTING_SIZE + INTERFACE_SETTING_SIZE + 64; //TOKEN
        $p2p_enable = $wireless_enable + INTERFACE_SETTING_SIZE;
	$network_v2[$wireless_enable] = 1;
	$network_v2[$p2p_enable] = 0;
        $token = byte2str($network_v2, 617, 64);
        str2byte($network_wireless, $token, 0, 64);
        if ($security != "") {
          switch ($security) {
            case "OPEN":
              $security = 0;
              str2byte($network_wireless, "", 327, 256);
              break;
            case "WEP":
              $security = 1;
              str2byte($network_wireless, $password, 327, 256);
              break;
            case "WPA":
              $security = 2;
              str2byte($network_wireless, $password, 327, 256);
              break;
            default;
            break;
          }
          $network_wireless[325] = $security; //type
        }
          str2byte($network_wireless, $ssid, 64, 128);    //ssid
        break;
      default;
      break;
    }

    $result_network_if_extention = requestToCamera(CMD_NETWORK_IF_EXTENSION, ACTION_SET, TYPE_REQUEST, $network_wireless);
    $result_network_config_v2 = requestToCamera(CMD_NETWORK_CONFIGURATION_V2, ACTION_SET, TYPE_REQUEST, $network_v2);
    if ($result_network_config_v2[0] != "OK")
      header("HTTP/1.1 501 Not Implemented");
    break;

  default:
    header("HTTP/1.1 404 Not Found");
    break;
}
?>
