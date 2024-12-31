<?php

require_once ('./adv/_define.inc');
CheckAdminAccount(FALSE);

///////////////////////////////////////////////
// FTP Transfer
//////////////////////////////////////////////
function submenu_ftp()
{
    $FTPMode = array(
        0 => 'Active',
        1 => 'Passive'
    );

    $responseOutput = new ResponseOutput();
    if ($_REQUEST['action'] != 'view' && $_REQUEST['action'] != 'set' && $_REQUEST['action'] != 'test')
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }

    $classInstances = GetClassInstance('ftpemail');

    $ftpConf = $classInstances['FTPSetting'];


    if ($_REQUEST['action'] == 'set')
    {
        foreach ($_REQUEST as $name => $value)
        {
            switch ($name)
            {
                case 'Mode':
                    {
                        $mode = array_search($value, $FTPMode);
                        if (is_bool($mode))
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $ftpConf->dataInfo['PassiveMode']['value'] = $mode;
                    }break;
                case 'Port':
                    {
                        if ($value < 1 || $value > 65535)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $ftpConf->dataInfo['Port']['value'] = $value;
                    }break;
                case 'Host':
                case 'Path':
                    /* case 'FileNameSuffix': */
                    {
                        if (strlen($value) > 32)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }

                        //$dataNameList = array('Host' => 'Server', 'Path' => 'Directory', 'Username' => 'UserName', 'Password' => 'Password'/* ,'FileNameSuffix'=>'FileNameSuffix' */);
                        $dataNameList = array('Host' => 'Server', 'Path' => 'Directory');
                        $ftpConf->dataInfo[$dataNameList[$name]]['value'] = $value;
                    } break;
                case 'Username':
                case 'Password':
                    {
                        if (strlen($value) > 30)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }

                        $dataNameList = array('Username' => 'UserName', 'Password' => 'Password');
                        $ftpConf->dataInfo[$dataNameList[$name]]['value'] = $value;
                    } break;
                default:
                    break;
            }
        }
        $ftpConf->payload = MakePayload($ftpConf->dataInfo);
        $ftpConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($ftpConf);
        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
        $responseOutput->outputMsg = 'Host=' . $ftpConf->dataInfo['Server']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Mode=' . $FTPMode[$ftpConf->dataInfo['PassiveMode']['value']] . "\r\n";
        $responseOutput->outputMsg .= 'Port=' . $ftpConf->dataInfo['Port']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Path=' . $ftpConf->dataInfo['Directory']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Username=' . $ftpConf->dataInfo['UserName']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Password=' . $ftpConf->dataInfo['Password']['value'] . "\r\n";
        //$responseOutput->outputMsg .= 'FileNameSuffix='. $ftpConf->dataInfo['FileNameSuffix']['value']."\r\n";			
    }
    else if ($_REQUEST['action'] == 'test')
    {
        $testConf = $classInstances['NetworkTestConfiguration'];
        $testConf->dataInfo['Operation']['value'] = 1;
        $testConf->headerInfo['Action'] = ACTION_START;
        $testConf->SetPayload();
        $GLOBALS['SOCKET_MANAGER']->Connection($testConf);

        $dataArr = array(0 => 'Fail', 1 => 'Success', 2 => 'Trying');
        $responseOutput->outputMsg .= 'Status=' . $dataArr[$testConf->result] . "\r\n";
    }
    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

///////////////////////////////////////////////
// SMTP Transfer
//////////////////////////////////////////////
function submenu_smtp()
{
    $Encryption = array(
        0 => 'None',
        1 => 'SSL'
    );
    $Authentication = array(
        0 => 'None',
        1 => 'SMTP',
        2 => 'POPBeforeSMTP'
    );

    $responseOutput = new ResponseOutput();
    if ($_REQUEST['action'] != 'view' && $_REQUEST['action'] != 'set' && $_REQUEST['action'] != 'test')
    {
        $responseOutput->errCode = STATUS_ACTION_NOT_FOUND;
        return $responseOutput;
    }
    $classInstances = GetClassInstance('ftpemail');
    $smtpConf = $classInstances['SMTPSetting'];
    //$popConf = $classInstances['POPSetting'];
    //$isPOP = 0;//PNA

    if ($_REQUEST['action'] == 'set')
    {
        if (count($_REQUEST) < 3)
        {
            $responseOutput->errCode = STATUS_INVALID_PARAMETER;
            return $responseOutput;
        }

        foreach ($_REQUEST as $name => $value)
        {
            switch ($name)
            {
                case 'Port':
                    {
                        if ($value < 1 || $value > 65535)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $smtpConf->dataInfo['Port']['value'] = $value;
                    }break;
                /*
                  case 'POPPort':
                  {
                  if (isset($_REQUEST['Authenticaion']) && $_REQUEST['Authenticaion'] != 'POPBeforeSMTP')
                  {
                  $responseOutput->outputMsg .= 'Invalid Authentication Value';
                  $responseOutput->status = STATUS_INVALID_SYNTAX;
                  return $responseOutput;
                  }
                  if ($value < 1 || $value > 65535)
                  {
                  $responseOutput->status = STATUS_INVALID_SYNTAX;
                  return $responseOutput;
                  }
                  $popConf->dataInfo['POPPort']['value'] = $value;
                  $isPOP = 1;
                  }break;
                 * 
                 */
                case 'Authentication':
                    {
                        $auth = array_search($value, $Authentication);
                        if (is_bool($auth))
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        if ($auth == 1)
                        {
                            $smtpConf->dataInfo['AuthNeeded']['value'] = 1;
                        }
                        else if ($auth == 0)
                        {
                            $smtpConf->dataInfo['AuthNeeded']['value'] = 0;
                        }
                        else
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                    }break;
                case 'Host':
                case 'Username':
                case 'Password':
                /*
                  case 'POPHost':
                  case 'POPUserName':
                  case 'POPPassword':
                 * 
                 */
                case 'Sender':
                case 'Recipient':
                case 'Subject':
                case 'Message':
                    {
                        if (($name == 'Host' || $name == 'Username' || $name == 'Password') && strlen($value) > 32)
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        /*
                          else if ($name == 'POPHost' && strlen($value) > 63)
                          {
                          $responseOutput->outputMsg .= 'POPHost length should not exceed 63 character(s)';
                          $responseOutput->status = STATUS_INVALID_SYNTAX;
                          return $responseOutput;
                          }
                         * 

                          else if (isset($_REQUEST['Authenticaion']) && $_REQUEST['Authenticaion'] != 'POPBeforeSMTP')
                          {
                          if (($name == 'POPHost') || ($name == 'POPUserName') || ($name == 'POPPassword'))
                          {
                          $responseOutput->outputMsg .= 'Invalid Authentication Value';
                          $responseOutput->status = STATUS_INVALID_SYNTAX;
                          return $responseOutput;
                          }
                          }
                         */
                        $dataNameList = array('Host' => 'Server', 'Username' => 'UserName', 'Password' => 'Password',
                            /* 'POPHost' => 'POPHost', 'POPUserName' => 'POPUserName', 'POPPassword' => 'POPPassword', */
                            'Sender' => 'Sender', 'Recipient' => 'Recipient', 'Subject' => 'Subject', 'Message' => 'Body');

                        /*
                         * if (($name == 'POPHost') || ($name == 'POPUserName') || ($name == 'POPPassword'))
                          {
                          $popConf->dataInfo[$dataNameList[$name]]['value'] = $value;
                          $isPOP = 1;
                          }
                          else
                         * 
                         */
                        {
                            $smtpConf->dataInfo[$dataNameList[$name]]['value'] = $value;
                        }
                    }
                    break;
                case 'Encryption':
                    {
                        $encryption = array_search($value, $Encryption);
                        if (is_bool($encryption))
                        {
                            $responseOutput->errCode = STATUS_INVALID_VALUE;
                            return $responseOutput;
                        }
                        $smtpConf->dataInfo['SSLEnabled']['value'] = $encryption;
                    }
                    break;

                default:
                    break;
            }
        }
        $smtpConf->payload = MakePayload($smtpConf->dataInfo);
        $smtpConf->headerInfo['Action'] = ACTION_SET;
        $GLOBALS['SOCKET_MANAGER']->Connection($smtpConf);
        /*
          if ($isPOP)
          {
          $popConf->payload = MakePayload($popConf->dataInfo);
          $popConf->headerInfo['Action'] = ACTION_SET;
          $GLOBALS['SOCKET_MANAGER']->Connection($popConf);
          }
         * 
         */
        $responseOutput->outputMsg = 'OK';
    }
    else if ($_REQUEST['action'] == 'view')
    {
        $responseOutput->outputMsg = 'Host=' . $smtpConf->dataInfo['Server']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Port=' . $smtpConf->dataInfo['Port']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Username=' . $smtpConf->dataInfo['UserName']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Password=' . $smtpConf->dataInfo['Password']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Authentication=' . $Authentication[$smtpConf->dataInfo['AuthNeeded']['value']] . "\r\n";
        /*
          if ($smtpConf->dataInfo['AuthNeeded']['value'] == 'POPBeforeSMTP')
          {
          $responseOutput->outputMsg .= 'POPHost=' . $popConf->dataInfo['POPHost']['value'] . "\r\n";
          $responseOutput->outputMsg .= 'POPPort=' . $popConf->dataInfo['POPPort']['value'] . "\r\n";
          $responseOutput->outputMsg .= 'POPUserName=' . $popConf->dataInfo['POPUserName']['value'] . "\r\n";
          $responseOutput->outputMsg .= 'POPPassword=' . $popConf->dataInfo['POPPassword']['value'] . "\r\n";
          }
         * 
         */
        $responseOutput->outputMsg .= 'Sender=' . $smtpConf->dataInfo['Sender']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Recipient=' . $smtpConf->dataInfo['Recipient']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Subject=' . $smtpConf->dataInfo['Subject']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Message=' . $smtpConf->dataInfo['Body']['value'] . "\r\n";
        $responseOutput->outputMsg .= 'Encryption=' . $Encryption[$smtpConf->dataInfo['SSLEnabled']['value']] . "\r\n";
    }
    else if ($_REQUEST['action'] == 'test')
    {
        $testConf = $classInstances['NetworkTestConfiguration'];
        $testConf->dataInfo['Operation']['value'] = 0;
        $testConf->headerInfo['Action'] = ACTION_START;
        $testConf->SetPayload();
        $GLOBALS['SOCKET_MANAGER']->Connection($testConf);

        $dataArr = array(0 => 'Fail', 1 => 'Success', 2 => 'Trying');
        $responseOutput->outputMsg .= 'Status=' . $dataArr[$testConf->result] . "\r\n";
    }
    $responseOutput->errCode = STATUS_OK;
    return $responseOutput;
}

///////////////////////////////////////////////
// HTTP Transfer
//////////////////////////////////////////////
/* NOT SUPPORTED NOW
  function submenu_http()
  {
  $responseOutput = new ResponseOutput();
  if ($_REQUEST['action'] != 'view' && $_REQUEST['action'] != 'set')
  {
  $responseOutput->status = STATUS_INVALID_SYNTAX;
  return $responseOutput;
  }
  $classInstances = GetClassInstance('ftpemail');
  $httpConf = $classInstances['HTTPSetting'];
  if ($_REQUEST['action'] == 'set')
  {
  foreach ($_REQUEST as $name => $value)
  {
  switch ($name)
  {
  case 'URL':
  {
  $httpConf->dataInfo['URL']['value'] = $value;
  }break;
  case 'ProxyPort':
  {
  if ($value < 1 || $value > 65535)
  {
  $responseOutput->outputMsg .= 'Invalid Proxy Port Value';
  $responseOutput->status = STATUS_INVALID_SYNTAX;
  return $responseOutput;
  }
  $httpConf->dataInfo['ProxyPort']['value'] = $value;
  }break;
  case 'Username':
  case 'Password':
  case 'ProxyHost':
  case 'ProxyUsername':
  case 'ProxyPassword':
  {
  if ($name == 'ProxyHost' && strlen($value) > 63)
  {
  $responseOutput->outputMsg .= 'ProxyHost length should not exceed 63 character(s)';
  $responseOutput->status = STATUS_INVALID_SYNTAX;
  return $responseOutput;
  }
  $dataNameList = array('Username' => 'Username', 'Password' => 'Password', 'ProxyHost' => 'ProxyHost', 'ProxyUsername' => 'ProxyUsername', 'ProxyPassword' => 'ProxyPassword');
  $httpConf->dataInfo[$dataNameList[$name]]['value'] = $value;
  }break;
  default:
  break;
  }
  }
  $httpConf->payload = MakePayload($httpConf->dataInfo);
  $httpConf->headerInfo['Action'] = ACTION_SET;
  $GLOBALS['SOCKET_MANAGER']->Connection($httpConf);
  $responseOutput->outputMsg = 'OK';
  }
  else if ($_REQUEST['action'] == 'view')
  {
  $responseOutput->outputMsg = 'URL=' . $httpConf->dataInfo['URL']['value'] . "\r\n";
  $responseOutput->outputMsg .= 'Username=' . $httpConf->dataInfo['Username']['value'] . "\r\n";
  $responseOutput->outputMsg .= 'Password=' . $httpConf->dataInfo['Password']['value'] . "\r\n";
  $responseOutput->outputMsg .= 'ProxyHost=' . $httpConf->dataInfo['ProxyHost']['value'] . "\r\n";
  $responseOutput->outputMsg .= 'ProxyPort=' . $httpConf->dataInfo['ProxyPort']['value'] . "\r\n";
  $responseOutput->outputMsg .= 'ProxyUsername=' . $httpConf->dataInfo['ProxyUsername']['value'] . "\r\n";
  $responseOutput->outputMsg .= 'ProxyPassword=' . $httpConf->dataInfo['ProxyPassword']['value'] . "\r\n";
  }
  $responseOutput->status = STATUS_OK;
  return $responseOutput;
  }

 * 
 */

///////////////////////////////////////////////
// CGI Command
///////////////////////////////////////////////
switch (@$_REQUEST['msubmenu'])
{
    case 'ftp':
    case 'smtp':
        //case 'http':  NOT SUPPORTED NOW
        {

            $funcName = 'submenu_' . $_REQUEST['msubmenu'];
            SendResponse($funcName());
            break;
        }
    default:
        {
            $responseOutput = new ResponseOutput();
            $responseOutput->errCode = STATUS_SUBMENU_NOT_FOUND;
            SendResponse($responseOutput);
        }
}
?>
