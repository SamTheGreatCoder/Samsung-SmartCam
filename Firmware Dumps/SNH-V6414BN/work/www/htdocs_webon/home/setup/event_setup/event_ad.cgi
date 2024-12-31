<div class="h3_tit">
	<h3 class="wid220"><?php echo $t_ad[$GLOBALS['LANGINDEX']]; ?></h3>
</div>
<table style="width:670px; height:100px; margin-top:10px; margin-left:10px" border=0>
	<colgroup>
		<col style="width:100px;"/>
		<col style="width:480px;"/>
		<col style="width:20px;"/>
		<col style="width:30px;"/>
		<col style="width:30px;"/>
	</colgroup>	
	<tr>
		<th style="vertical-align:top; text-align:left"><?php echo $t_level[$GLOBALS['LANGINDEX']]; ?></th>
		<td>
			<img id="ad_threadshold_bar" src="../images/common/ad_bar.png" alt="" width="480px" style="height:1px; position: absolute" />
			<div style="width:480px; height:100px; background-color:#666f7a">
				<table id="ad_graph_table">
					<tbody>
						<tr>
							<td width="480px"></td>
						</tr>
					</tbody>
				</table>
			</div>
		</td>
		<td><img src="../images/setup/ad_levelbar.png" ></td>
		<td align="left">
			<div id="slider-vertical" style="height:100px; margin-left:6px"></div>
		</td>
		<td style="vertical-align:bottom;" align="left">
			<input type="text" class="text" id="event_ad_sensitivity" maxlength="3" style="width:25px; padding-left:5px" onKeyPress='return IsNum(event)' onKeyDown="OnlyNUm(event); OnKeyDownAdThreadshold(event);" />
		</td>
	</tr>
</table>
