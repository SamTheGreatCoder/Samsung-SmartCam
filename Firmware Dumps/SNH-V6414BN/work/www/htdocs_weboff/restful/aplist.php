<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/ipc_manager.php";
require_once $_SERVER["DOCUMENT_ROOT"] . "/utils/datetime_constant.php";

define("OFF_DNS"        , 65);
define("OFF_NETWORK"    , 230);
define("OFF_GATEWAY"    , 1588);
define("OFF_WLAN", 909);

switch ($_SERVER['REQUEST_METHOD']) {
  case "GET":
    ini_set("max_execution_time", 3);
    $result = requestToCamera(CMD_WIRELESS_SCANNING_2, ACTION_GET, TYPE_REQUEST, null);
    if ($result[0] == "OK") {
      if ($result[1] != null && count($result[1]) >= 88) {
        $count = byte2int($result[1], 0);
        $level = 0;
        $ssid = "";

        $xw = new xmlWriter();
        $xw->openMemory();
        $xw->startDocument('1.0','UTF-8');
        $xw->startElement ('Network');
        for($i=0,$j=4; $i<$count; $i++,$j+=84){
          $ssid = byte2str($result[1], $j, 64);
          $rssi = byte2int($result[1], $j+80);
          $security = byte2str($result[1], $j+64, 16);

          $xw->startElement ('aplist');
          $xw->writeElement ('id', $i+1);
          $xw->writeElement ('ssid', $ssid);
          $xw->writeElement ('rssi', $rssi);
          $xw->writeElement ('security', $security);
          $xw->endElement();
        }
        $xw->endElement();
        $xw->endDocument();
      }
      header("Content-type: application/xml");
      echo $xw->outputMemory(true);
    } else {
      header("HTTP/1.1 501 Not Implemented");
    } break;
  default:
    header("HTTP/1.1 404 Not Found");
    break;
}
?>
