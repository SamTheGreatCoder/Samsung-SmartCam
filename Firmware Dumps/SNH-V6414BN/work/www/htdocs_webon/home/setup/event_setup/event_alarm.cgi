<div class="h3_tit">
	<h3 class="wid320"><?php echo $t_inputDeviceSetup[$GLOBALS['LANGINDEX']]; ?></h3>
</div>
<table class="data_write" >
	<colgroup>
		<col style="width:180px;"/>
		<col />
	</colgroup>
	<tbody>
		<tr>
			<th scope="row"><?php echo $t_type[$GLOBALS['LANGINDEX']]; ?></th>
			<td>
				<select name="select" id="event_alarm_type" class="selectbox_style">
		         <option value="0" <?php if ($event_class[$eventType]->dataInfo['Type']['value'] == 0) echo "selected=\"selected\""; ?>> <?php echo $t_normal_open[$GLOBALS['LANGINDEX']]; ?></option>
					<option value="1" <?php if ($event_class[$eventType]->dataInfo['Type']['value'] == 1) echo "selected=\"selected\""; ?>> <?php echo $t_normal_close[$GLOBALS['LANGINDEX']]; ?></option>
				</select>
			</td>
		</tr>
	</tbody>
</table>
