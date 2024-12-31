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
