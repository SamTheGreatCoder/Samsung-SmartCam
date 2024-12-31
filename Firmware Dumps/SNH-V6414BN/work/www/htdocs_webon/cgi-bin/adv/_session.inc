<?php
define('MAX_INCORRECT_COUNT', 5);	// max incorrect count
define('NG', 0);
define('OK', 1);
define('LOCKED', 2);
// initialize session information
//
// sess_auth_type : 인증모드 1일 경우 로그인모드이다.
// sess_user_id : 로그인 아이디
// sess_auth_key : 인증키 ( md5(md5(id:pass):md5(ip:last)) )
// sess_sub_key : 서브키 ( md5(id:pass) )
// sess_incorrect_cnt : 비밀번호 틀림 횟수
// sess_last_access_time : 마지막 접속 시도 시간
// sess_ip : 로그인 브라우저 아이피
// sess_last_auth_time : 마지막 인증 시간 
// sess_last_page : 마지막 접속 페이지 

if (!isset($_SESSION['sess_auth_type'])) {
	// 기본값은 normal login으로 지정하고, 로그인페이지에서 분기 결정. 
	$_SESSION['sess_auth_type'] = 1;	
}

if (!isset($_SESSION['sess_ip'])) {
	$_SESSION['sess_ip'] = $_SERVER['REMOTE_ADDR'];
}
if (!isset($_SESSION['sess_last_auth_time'])) {
	$_SESSION['sess_last_auth_time'] = 0;
}
if (!isset($_SESSION['sess_last_page'])) {
	$_SESSION['sess_last_page'] = "/home/monitoring.cgi";
}

function ResponseLoginResult($_value)
{
	$msgType = array('NG', 'OK', 'LO');
	header("Content-Type: text/plain");
	header("Content-Length: 2");
	echo $msgType[$_value];
	exit;
}

//echo $_SESSION['sess_user_id']."<br />";
//echo "The cache limiter is now set to ".session_cache_limiter()."<br />";
//echo "The cached session pages expire after ".session_cache_expire();

// updateCount : Login / session 구분용도로 변경.
// updateCount : Incorrectcount control
function UserLogin($id, $lastAuthTime, $authKeyValue, $updateCount, $pass = '')
{
	//if (IsLoginLocked()) return LOCKED;

	$UserLoginClassInstances = GetClassInstance('userlogin');
	$userlogin = $UserLoginClassInstances['UserLogin'];
	
	// save current system clock time
	$systemClockTime = $userlogin->dataInfo['SystemClockTime']['value'];
	if ($lastAuthTime == 0) $lastAuthTime = $systemClockTime;	// for first login..

	$userlogin->dataInfo['ID']['value'] = $id;
	$userlogin->dataInfo['IP']['value'] = $_SESSION['sess_ip'];
	$userlogin->dataInfo['LastAuthTime']['value'] = $lastAuthTime;
	$userlogin->dataInfo['IsLoginCmd']['value'] = $updateCount;

	if (strlen($authKeyValue) == 0 && strlen($pass) != 0) 
	{
		$ha1 = md5($id.':'.$pass);
		$ha2 = md5($_SESSION['sess_ip'].':'.$lastAuthTime);
		$userlogin->dataInfo['AuthKey']['value'] = md5($ha1.':'.$ha2);
		
		$_SESSION['sess_sub_key'] = $ha1;
	}
	else 
	{
		$userlogin->dataInfo['AuthKey']['value'] = $authKeyValue;
	}
	
	$userlogin->headerInfo['Action'] = ACTION_SET;
	$userlogin->SetPayload();
	$GLOBALS['SOCKET_MANAGER']->Connection($userlogin);


	if ($GLOBALS['SOCKET_MANAGER']->dataInfo['ErrorCode']['value'] != 1) 	{
		//if ($updateCount) UpdateIncorrectCount();	// update incorrect count
		//if (IsLoginLocked()) return LOCKED;
		if ($GLOBALS['SOCKET_MANAGER']->dataInfo['ErrorCode']['value'] == 90) return LOCKED;
		else return NG;
	}
	else 
	{
		//ClearIncorrectCount();	// clear incorrect count

		$_SESSION['sess_user_id'] = $id;
		$_SESSION['sess_last_auth_time'] = $systemClockTime; // update current system clock time
		// $_SESSION['sess_last_auth_time'] = time(); // update current time
		
 		$ha2 = md5($_SESSION['sess_ip'].':'.$_SESSION['sess_last_auth_time']);
 		$_SESSION['sess_auth_key'] = md5($_SESSION['sess_sub_key'].':'.$ha2);	// save new auth key
		
		return OK;
	}
	//$GLOBALS['SOCKET_MANAGER']->CheckErrorCode();
	return OK;
}

// check valid session 
function CheckValidSession() {
	$url = $_SERVER['PHP_SELF'];
	
	// skip defaultset urls
	if ($url == '/login/account.cgi'
		|| $url == '/auth/userlogin.cgi')
	{
		return;
	}

	//var_dump(isset($_SESSION['sess_user_id']));
	
	// skip cgi-bin urls
	$cgi_bin_pattern = '/^\/cgi-bin\//';
	if (preg_match($cgi_bin_pattern, $url, $matches, PREG_OFFSET_CAPTURE) == 1) {
		return;
	}
	
	// skip cgi-bin-noauth urls
	$cgi_bin_pattern = '/^\/cgi-bin-noauth\//';
	if (preg_match($cgi_bin_pattern, $url, $matches, PREG_OFFSET_CAPTURE) == 1) {
		return;
	}
	
	if(!isset($_SESSION['sess_user_id'])){
		GoLoginPage();
	}
	else if (isset($_SESSION['sess_last_auth_time'])
			&& isset($_SESSION['sess_user_id'])
			&& isset($_SESSION['sess_ip'])
			&& isset($_SESSION['sess_auth_key'])
			&& UserLogin($_SESSION['sess_user_id'], $_SESSION['sess_last_auth_time'], $_SESSION['sess_auth_key'], 0) == OK )
	{
			// accessing setup directory is allowed for only admin user
			$setup_dir_pattern = '/^\/home\/setup\//';
			if (preg_match($setup_dir_pattern, $url, $matches, PREG_OFFSET_CAPTURE) == 1) {
				CheckAdminAccount();
			}
			// do nothing OK
	}
	else{
		
		// 1시간 후 로그아웃
		if (time() - $_SESSION['sess_last_auth_time'] > 3600) {
			session_unset();     // 현재 연결된 세션에 등록되어 있는 모든 변수의 값을 삭제한다
			session_destroy();  //현재의 세션을 종료한다
			GoLoginPage();
		}
		$url = $_SERVER['PHP_SELF'];
		if ( $url == '/home/loginpage.cgi' || $url == '/home/pw_restore.cgi' || $url == '/home/pw_change.cgi') {
			header('Location: /'); 
			exit;
		}
	}
}

// move to login page
function GoLoginPage() {

	$url = $_SERVER['PHP_SELF'];

	// skip urls
	if ( $url == '/home/loginpage.cgi' || $url == '/home/pw_restore.cgi' || $url == '/home/pw_change.cgi') return;

	$_SESSION['sess_last_page'] = $_SERVER['PHP_SELF'];
	header('Location: ' . '/home/loginpage.cgi'); 
	exit;
}

CheckValidSession();

?>
