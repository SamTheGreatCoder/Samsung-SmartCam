<?php
/**
 * General Script Utils
 *
 * Unauthorized use of these files is an infringement of Canadian and
 * International copyright laws.  For full  copyright and license information, please
 * view the LICENSE file that was distributed with this platform.
 *
 * iWatchInstaller class
 * 
 * @package         
 * @creation-date   2014-04-11
 * @revision        1.0.0.0
 */
error_reporting(E_ALL ^ E_WARNING);

class iWatchLogger
{
    
    const MAX_LOG_SIZE = 524288;
    
    public function __set($name, $value)
    {
        switch($name)
        {
            case 'logfile':
            $this->logfile = $value;
            //create directory
            $dir = dirname($value);
            mkdir($dir,0766,true);
            break;

            default:
            throw new Exception("$name cannot be opened");
        }
    }

    public function write($message)
    {
        $message = date('Y-m-d H:i:s') .' - '.$message;
        $message .= "\n";

        $size = filesize($this->logfile);
        if ($size > iWatchLogger::MAX_LOG_SIZE) unlink($this->logfile);        
        return file_put_contents( $this->logfile, $message, FILE_APPEND );
    }
}