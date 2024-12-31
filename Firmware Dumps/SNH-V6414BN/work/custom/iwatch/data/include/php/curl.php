<?php
require_once '/mnt/custom/iwatch/include/php/logger.php';

class Curl
{
    const CURL = '/usr/bin/curl';
    const CURL_RETRIES = 3;

        protected $_opts_map = array(
                                        "digest" => "--digest",
                                        "credentials" => "-u",
                                        "verbose" => "-v",
                                        "header" => "-H",
                                        "data" => "--data",
                                        "data-ascii" => "--data-ascii",
                                        "data-binary" => "--data-binary",
                                        "method" => "-X",
                                        "timeout" => "--connect-timeout",
                                        "maxtime" => "--max-time"

                          );

    private $args = "-k -s -w '\nMETADATA:total_time=%{time_total}&http_code=%{http_code}\n'";
    private $logger;
    private $url = null;
    private $response = null;
    private $async = false;
    private $raw_response = null;
    public $curl_code = 0;
    public $error = false;
    public $error_code = 0;
    public $error_message = null;
    public $http_status_code = 0;
    public $http_error_message = null;

    public function __construct()
    {
        $this->logger = new iWatchLogger();
        $this->logger->logfile = '/tmp/logs/iwl.curl.log';

    }

    public function get($url, $data = array(), $opts = array())
    {
        // set querystring
        if (is_array($data) && !empty($data)) {
            $this->setUrl( $this->buildURL($url,$data) );
        } else {
            $this->setUrl($url);
        }

        $this->setOpt("method", "GET");
        return $this->exec();
    }

    public function post($url, $data = array())
    {
        if (is_array($data) && !empty($data)) {
                        $this->setPostData($data);
        }

        $this->setOpt("method", "POST");
        $this->setUrl($url);
        return $this->exec();
    }

    public function postRaw($url, $data)
    {
       $tmpfname = tempnam("/tmp", "json");
       $handle = fopen($tmpfname, "w");
       if (!empty($data)) {
            fwrite($handle, $data);
            fclose($handle);
            $this->setRawData('@'.$tmpfname);
       }
       $this->setOpt("method", "POST");
       $this->setUrl($url);
       $response = $this->exec();
       unlink($tmpfname);

       return $response;
    }

    public function putRaw($url, $data)
    {
       $tmpfname = tempnam("/tmp", "json");
       $handle = fopen($tmpfname, "w");
       if (!empty($data)) {
            fwrite($handle, $data);
            fclose($handle);
            $this->setRawData('@'.$tmpfname);
       }
       $this->setOpt("method", "PUT");
       $this->setUrl($url);
       $response = $this->exec();
       unlink($tmpfname);

       return $response;
    }

    public function options($url, $data = array())
    {
        $this->setUrl($url);
        return $this->exec();
    }

    public function setBasicAuthentication($username, $password = '')
    {
                $this->setOpt("credentials", $username . ":" . $password);
    }

    public function setOpt($option, $value)
    {
                $option = $this->_opts_map[$option];
                if (!empty($option)) $this->args .= " " . $option;
                if (!empty($value)) $this->args .= " " .  "'" . $value . "'";
    }

    public function setHeader($header)
    {
                $this->setOpt("header", $header);
    }

    public function getOpt($option)
    {
        return $this->options[$option];
    }

    public function setUrl($url)
    {
        $this->url = $url;
    }

    public function setAsync($async)
    {
        $this->async = $async;
    }

    public function getUrl()
    {
        return $this->url;
    }

    public function getResponse(){
        return $this->raw_response;
    }

    public function getStatusCode(){
        return $this->http_status_code;
    }

    public function verbose($on = true)
    {
        if ($on) $this->setOpt("verbose", "");
    }

    private function buildURL($url, $data = array())
    {
        return $url . (empty($data) ? '' : '?' . http_build_query($data));
    }

    private function extractResponseMetaData( $data )
    {
        $metadata = array();
        $md_count = substr_count($data, 'METADATA:');
        $content = explode(PHP_EOL, $data);
        foreach ($content as $key => $value){
                if (strstr($value,'METADATA:')){
                        if (!strstr($value,'total_time=0.000')){   // treat multipart
                                parse_str(str_replace("METADATA:","",$value), $metadata);
                        }
                        unset ($content[$key]);
                }
        }

        // set metadata
        $this->http_status_code = array_key_exists('http_code',$metadata) ? intval($metadata['http_code']) : 0;

        //return content
        return implode(PHP_EOL, $content);
    }

    private function parseResponseHeaders($raw_headers)
    {

    }

    private function postfields($data)
    {
        return $data;
    }

    private function setPostData( $data = array() )
    {
            foreach ($data as $key => $value){
                    $this->setOpt("data", $key . "=" . $value);
            }
    }

    public function setRawData( $data ){
            $this->args .= " --data " . "'" . $data . "'";
    }


    protected function exec( )
    {
        $requestStr = Curl::CURL . " '" . $this->url . "' " . $this->args;
        if ($this->async){
                // detatch and ignore response
                $this->logger->write($requestStr);
                exec( $requestStr . " >> /tmp/logs/iwl.installer.log 2>&1 &");
        } else {
            for ($i = 0; $i < Curl::CURL_RETRIES; $i++){
                $this->logger->write($requestStr);
                ob_start();
                system($requestStr,$ret);
                $response = ob_get_contents();
                ob_end_clean();
                // Log Response
                $this->logger->write($response);
                $response = $this->extractResponseMetaData( $response );
                $this->curl_code = $ret;
                $this->raw_response = $response;
                if ( ($this->http_status_code == 0) || ($this->http_status_code == 404) ) {
                  sleep(1);
                } else {
                  break;
                }
           }

        }
        return ($this->http_status_code != 0);
    }
}