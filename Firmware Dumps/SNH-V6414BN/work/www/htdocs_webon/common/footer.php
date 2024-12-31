<?php
require_once $_SERVER["DOCUMENT_ROOT"] . "/resources/languages/Language.php";
?>

<!-- s:footer_cl -->
<div id="footer_cl">
	<img src="/resources/images/dvc_copyright.png" class="footerLogo"/>
	<address>
		<?=$Lang["CopyrightⓒSAMSUNG TECHWIN CO, LTD 2012. All rights reserved."]?>
	</address>
</div>
<!-- e:footer_cl -->

<!-- s:모달윈도우  -->
<div id="mw_progress" style="display:none">
	<div class="bg"><!-- 내용넣지 마세요--></div>	
	<div id="popDiv" class="idCheck">
		<h3><input type="text" id="prog_title" value="" readonly="readonly" style="font-size:20px"/></h3>
		<div class="msg">
			<p><img src="/resources/images/working.gif"/></p>
			<p style="font-size:16px"><?=$Lang["Please wait a moment."]?>...</p>
		</div>		
	</div>	
</div>
<!-- e:모달윈도우 -->