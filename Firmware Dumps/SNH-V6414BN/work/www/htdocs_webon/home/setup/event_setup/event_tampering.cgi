<?php
echo "<div class=\"h3_tit\" style='overflow:auto;width:100%;'>
			<h3 class=\"wid220\">".$t_tampering[$GLOBALS['LANGINDEX']]."</h3>
		</div>
		<table class=\"data_write\" >
			<colgroup>
				<col style=\"width:180px;\"/>
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope=\"row\">".$t_sensitivity[$GLOBALS['LANGINDEX']]."</th>
					<td>
						<select id=\"event_tampering_sensitivity\" class=\"selectbox_style\">
							<option value=\"1\"".($event_class[$eventType]->dataInfo['Sensitivity']['value']==1 ? "selected=\"selected\"" : "").">".$t_low[$GLOBALS['LANGINDEX']]."</option>
							<option value=\"2\"".($event_class[$eventType]->dataInfo['Sensitivity']['value']==2 ? "selected=\"selected\"" : "").">".$t_normal[$GLOBALS['LANGINDEX']]."</option>
							<option value=\"3\"".($event_class[$eventType]->dataInfo['Sensitivity']['value']==3 ? "selected=\"selected\"" : "").">".$t_high[$GLOBALS['LANGINDEX']]."</option>
						</select>
					</td>
				</tr>
			</tbody>
		</table>";
?>
