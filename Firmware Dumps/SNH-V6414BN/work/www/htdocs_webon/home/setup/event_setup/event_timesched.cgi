<?php
$intervalTime = 0;
$intervalUnit = 0;
$interval = $event_class['timesched']->dataInfo['Interval']['value'];
if ($interval/600 <= 1) {
	$intervalUnit = 10;
	$intervalTime = $interval/10;
}
else {
	$intervalUnit = 600;
	$intervalTime = $interval/600;
}

echo "<div class=\"h3_tit\" style='overflow:auto;width:100%'>
			<h3 class=\"wid220\">".$t_transferInterval[$GLOBALS['LANGINDEX']]."</h3>
		</div>
		<table class=\"data_write\" >
			<colgroup>
				<col style=\"width:180px;\" />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope=\"row\">".$t_oneImageper[$GLOBALS['LANGINDEX']]."</th>
					<td>
						<select name=\"select\" id=\"event_timesched_interval\" class=\"selectbox_style\" style=\"width:46px; margin-right:10px\">
			        		<option value=\"5\"".($intervalTime == 5 ? "selected=\"selected\"" : "").">5</option>
							<option value=\"10\"".($intervalTime == 10 ? "selected=\"selected\"" : "").">10</option>
							<option value=\"15\"".($intervalTime == 15 ? "selected=\"selected\"" : "").">15</option>
							<option value=\"30\"".($intervalTime == 30 ? "selected=\"selected\"" : "").">30</option>
		           		<option value=\"45\"".($intervalTime == 45 ? "selected=\"selected\"" : "").">45</option>
		           		<option value=\"60\"".($intervalTime == 60 ? "selected=\"selected\"" : "").">60</option>
		      		</select>
		      		<select name=\"select\" id=\"event_timesched_interval_unit\" class=\"selectbox_style\" style=\"width:180px\">
		           		<option value=\"10\"".($intervalUnit == 10 ? "selected=\"selected\"" : "").">".$t_seconds[$GLOBALS['LANGINDEX']]."</option>
		           		<option value=\"600\"".($intervalUnit == 600 ? "selected=\"selected\"" : "").">".$t_minutes[$GLOBALS['LANGINDEX']]."</option>
		   			</select>
					</td>
				</tr>
			</tbody>
		</table>";
?>
