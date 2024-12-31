
<?php
require_once ('../language/language_tooltip.cgi');

$width = $GLOBALS['VIEWER_RESOLUTION']['width'];
$height = $GLOBALS['VIEWER_RESOLUTION']['height'];
?>

<style>
	#plugin_control_area{
		text-align: center;
		padding-top: 20px;
		background-color: #2B313E;
		width: 680px;
		height: <?php echo $height+5;?>px;
	}
	#VideoSetup{
		background:#2B313E;
		width: <?php echo $width;?>px;
		height: <?php echo $height;?>px;
		float: center;
		position:relative;
	}
	#VideoSetup .drawArea-position{
		position: absolute;
		width: <?php echo $width;?>px;
		height: <?php echo $height;?>px;
		<?php if($classInstances['Information']->dataInfo['Rotate']['value'] == 0 || $classInstances['Information']->dataInfo['Rotate']['value'] == 2){ ?>
			left: 20px;
		<?php }else{ ?>
			<?php if($GLOBALS['M_MAX_RESOLUTION'] == MAX_1_MEGA && $GLOBALS['M_ISP_TYPE'] == ISP_TYPE_HISILICON) { ?>
			left: 80px; // Litenet 1.3M
			<?php } else { ?>
			left: 160px;
			<?php } ?>
		<?php } ?>
	}
	#poly-dialog, #poly-dialog-appear {
		margin-left:20px;
	}
	.ui-slider-vertical .ui-slider-range {
		background: #000000;
	}
	img {	
		cursor:pointer;
	}
	
</style>
<script type="text/javascript" language="javascript">
	$(document).ready(function(){
		$(document).tooltip({
			open: function (event, ui) {
				setTimeout(function () {
					$(ui.tooltip).hide();
				}, 3000);
			}
		});
	});

	<?php if($event_name == 'externalPTZ'){ ?>	
		function OnClickExternalPTZ(cmd){		//[cmd] : "stop":0, "up":1, "down":2, "left":3, "right":4, "upLeft":5, "upRight":6, "downLeft":7, "downRight":8, "zoomIn":9, "zoomOut":10, "near":11, "far":12
			var externSpeed = $("#externPtzSpeed").val();
			SISOPlugin.externalPtz.control(externSpeed,cmd);
		}
	<?php } ?>
	<?php if($GLOBALS["M_SUPPORT_AZIMUTH"]) { ?>
		function OnClickAzimuthPosition()
		{
			var msg = "<SetPTZAzimuthPosition></SetPTZAzimuthPosition>";
			RequestAjaxMsg(msg, "<?php echo $t_apply[$GLOBALS['LANGINDEX']]; ?>", ajaxReqUrl, 'NO_REFRESH', 'true');
			$("#imgAzimuth").show();
			window.setTimeout(function(){
				$("#imgAzimuth").hide();	
			},2000);
		}
	<?php } ?>
</script>

<table>
	<tr>
		<td>			
			<div id="plugin_control_area">
				<div id="VideoSetup">
					<?php if($GLOBALS["M_SUPPORT_AZIMUTH"]) { ?>
					<img id="imgAzimuth" style="position:absolute; left:<?php echo ($width/2);?>px; top:<?php echo ($height/2)-55;?>px; display:none;z-index:1000;" src="../images/common/azimuth.png" />	
					<?php } ?>
					<div id="DisableVideoSetup" class="drawArea-position" style="top: 0px; background-color:#000000; display:none; z-index:1000; filter:alpha(opacity=0.5); opacity:0.5; -moz-opacity:0.5; -ms-filter: 'progid:DXImageTransform.Microsoft.Alpha(Opacity=50)';"></div>
					<span id="pluginArea" class="drawArea-position" style="background-color:black"></span>
				<?php if($event_name == "ptzlimit" ) { ?>
					<div id="PtzLimitGuide" class="drawArea-position"></div>
				<?php } else { ?>
					<?php if(GetBrowserName() == 'IE') { ?>
					<span id="" class="drawArea-position" style="background:#000;opacity:0;filter:alpha(opacity=0);"></span> 
					<?php } ?>
				<?php } ?>
				<?php if($event_name == "videosetup" || $event_name == "ptztracking" || $event_name == 'smartcodec' || $event_name == 'focussetup') { ?>
					<div id="polyDraw" class="drawArea-position">
						<canvas id="myCanvas" width="<?php echo $width;?>" height="<?php echo $height;?>"></canvas>
						<?php if(GetBrowserName() == 'IE' && ieversion() <= 8) { ?>
						<span class="drawArea-position" style="left:0px;background:#000;opacity:0;filter:alpha(opacity=0);"></span> 
						<?php } ?>						
						<canvas id="imgTemp" width="<?php echo $width;?>" height="<?php echo $height;?>" style="position: absolute;top:0px;left:0px;z-index:1000"></canvas>
					</div>
				<?php } else if($event_name == "fd") { ?>
					<div id="FDPolyDraw" class="drawArea-position">
						<canvas id="FDPoly" width="<?php echo $width;?>" height="<?php echo $height;?>"></canvas>
						<?php if(GetBrowserName() == 'IE' && ieversion() <= 8) { ?>
						<span class="drawArea-position" style="left:0px;background:#000;opacity:0;filter:alpha(opacity=0);"></span> 
						<?php } ?>
						<canvas id="FDPolyTemp" width="<?php echo $width;?>" height="<?php echo $height;?>" style="position: absolute;top:0px;left:0px;z-index:1000;" ></canvas>
					</div>
				<?php } else if($event_name == "va" || $event_name == "presetedit") { ?>
					<div id="polyDraw" class="drawArea-position">
						<canvas id="myCanvas" width="<?php echo $width;?>" height="<?php echo $height;?>"></canvas>
						<?php if(GetBrowserName() == 'IE' && ieversion() <= 8) { ?>
						<span class="drawArea-position" style="left:0px;background:#000;opacity:0;filter:alpha(opacity=0);"></span>
						<?php } ?>
						<canvas id="imgTemp" width="<?php echo $width;?>" height="<?php echo $height;?>" style="position: absolute;top:0px;left:0px;z-index:1000;"></canvas>
					</div>
					<div id="fullScreen" class="drawArea-position">
						<canvas id="fullCanvas" width="<?php echo $width;?>" height="<?php echo $height;?>" style="background:red;opacity:0.5;filter:alpha(opacity=50);" ></canvas>
					</div>
					<div id="lineDraw" class="drawArea-position">
						<canvas id="LineCanvas" width="<?php echo $width;?>" height="<?php echo $height;?>"></canvas>
						<?php if(GetBrowserName() == 'IE' && ieversion() <= 8) { ?>
						<span class="drawArea-position" style="left:0px;background:#000;opacity:0;filter:alpha(opacity=0);"></span>
						<?php } ?>
						<canvas id="LineCanvasTmp" width="<?php echo $width;?>" height="<?php echo $height;?>" style="position: absolute;top:0px;left:0px;z-index:1000;"></canvas>
					</div>
					<div id="rectangleDraw" class="drawArea-position">
						<canvas id="myCanvasRect" width="<?php echo $width;?>" height="<?php echo $height;?>"></canvas>						
						<?php if(GetBrowserName() == 'IE' && ieversion() <= 8) { ?>
						<span class="drawArea-position" style="left:0px;background:#000;opacity:0;filter:alpha(opacity=0);"></span>
						<?php } ?>						
						<canvas id="myCanvasRectTmp" width=" <?php echo $width;?>" height="<?php echo $height;?>" style="position: absolute;top:0px;left:0px;z-index:1000;" ></canvas>
					</div>
					<div id="MDPolyDraw" class="drawArea-position">
						<canvas id="MDPoly" width="<?php echo $width;?>" height="<?php echo $height;?>"></canvas>
						<?php if(GetBrowserName() == 'IE' && ieversion() <= 8) { ?>
						<span class="drawArea-position" style="left:0px;background:#000;opacity:0;filter:alpha(opacity=0);"></span> 
						<?php } ?>						
						<canvas id="MDPolyTemp" width="<?php echo $width;?>" height="<?php echo $height;?>" style="position: absolute;top:0px;left:0px;z-index:1000;" ></canvas>
					</div>
					<div id="max_min" class="drawArea-position">						
						<div id="maxMinCover"  style="position: absolute; top: 0px; left: 0px; z-index: 1000; width: <?php echo $width;?>px; height: <?php echo $height;?>px;" ></div>
						<div id="minRect" style="border:1px solid yellow;position: absolute;background:blue;opacity:0.2;filter:alpha(opacity=20);"></div>
						<div id="maxRect" style="border:1px solid yellow;position: absolute;background:red;opacity:0.2;filter:alpha(opacity=20);"></div>
						<div id="minMaxTemp" style="border:1px solid blue;position: absolute;display:none"></div>
					</div>		
					<div id="poly-dialog" title="Defined Area Based Rule" style="display:none" > 
						<p><input type="checkbox" name="poly_type" id="polyEntering" value="Entering" ><label for="polyEntering"><?php echo $t_entering[$GLOBALS['LANGINDEX']]; ?></label></p>
						<p><input type="checkbox" name="poly_type" id="polyExiting" value="Exiting" ><label for="polyExiting"><?php echo $t_exiting[$GLOBALS['LANGINDEX']]; ?></label> </p>
					</div>
					<div id="poly-dialog-appear" title="Defined Area Based Rule" style="display:none; margin-left:20px;" > 
						<p><input type="checkbox" name="appear_type" id="app_disapp" value="Appearance/Disappearance" > <label for="app_disapp"><?php echo $t_appear_disappear[$GLOBALS['LANGINDEX']]; ?></label></p>
					</div>
					<div id="poly-dialog-entireArea" title="Entire Area Based Rule" style="display:none; margin-left:20px;" > 
						<p><input type="checkbox" name="appPoly_type" id="app_disapp_entire" value="Appearance/Disappearance" > <label for="app_disapp_entire"><?php echo $t_appear_disappear[$GLOBALS['LANGINDEX']]; ?></label> </p>
					</div>
					<div id="line-dialog" title="Defined Area Based Rule" style="display:none; margin-left:20px;" >
						<p><input type="checkbox" name="right" id="right" value="right" ><label for="right"><?php echo $t_right[$GLOBALS['LANGINDEX']]; ?></label></p>
						<p><input type="checkbox" name="left" id="left" value="left" ><label for="left"><?php echo $t_left[$GLOBALS['LANGINDEX']]; ?></label></p>
					</div>
				<?php } else { }?>
				</div> <!-- end VideoSetup-->
			</div>
		</td>
		</tr>
		<tr>
		<td class="ptzControl">			
			<div id="ptzcontrol" style="background-color:#2B313E;padding-top:20px; ">
				<div style="width:240px;height:148px; position:relative; margin-left:auto; margin-right:auto; text-align:center; top:-5px; left:-162px;">				
					<?php if ($GLOBALS['M_SUPPORT_PTZ']) { ?>
					<div id="PTZArea" style="background: url(../images/common/PTZ/ptcontrol_bg.png); background-repeat: no-repeat;">
						<div id="MOVEArea" style="height:138px; width:190px; position:relative; margin-left:0px; margin-right:auto; z-index:1">
						</div>
						<div style="position:absolute;top:57px;left:83px; z-index:100">
							<img id="Move-Btn" src="../images/common/PTZ/jog.png" />
						</div>
					</div>
						<!-- AUTO TRACKING -->
						<?php 
							if($event_name == "ptztracking") { ?>				
							<div style="position:absolute;left:227px;top:70px;">
								<img id="btnAutoTracking_on" src="../images/common/PTZ/autotracking_on_normal.png" 
									onclick="OnClickAutoTracking('1')" 
									onMouseOver="ChangeImage('btnAutoTracking_on','../images/common/PTZ/autotracking_on_press.png');"
									 onMouseOut="ChangeImage('btnAutoTracking_on','../images/common/PTZ/autotracking_on_normal.png');"
									title="<?php echo $t_autotracking_on[$GLOBALS['LANGINDEX']]; ?>"/>
							</div>
							<div style="position:absolute;left:227px;top:108px;">
								<img id="btnAutoTracking_off" src="../images/common/PTZ/autotracking_off_normal.png" 
									onclick="OnClickAutoTracking('0')" 
									onMouseOver="ChangeImage('btnAutoTracking_off','../images/common/PTZ/autotracking_off_press.png');"
									  onMouseOut="ChangeImage('btnAutoTracking_off','../images/common/PTZ/autotracking_off_normal.png');"
									title="<?php echo $t_autotracking_off[$GLOBALS['LANGINDEX']]; ?>"/>
							</div>
						<?php
							}
							else if ($event_name == "presetedit") {
						?>
							<div style="position:absolute;left:565px;top:70px;">
								<img id="home-start" src="../images/common/PTZ/gohome_normal.png" 	title="<?php echo $t_goHomePosition[$GLOBALS['LANGINDEX']]; ?>"/>
							</div>
							<div style="position:absolute;left:565px;top:108px;">
								<img id="home-set" src="../images/common/PTZ/sethome_normal.png" title="<?php echo $t_setHomePosition[$GLOBALS['LANGINDEX']]; ?>"/>	
							</div>													
							<div style="position:absolute;left:565px;top:0px;" onclick="OnClickSavePreset();">	
								<img id="savePreset_btn" src="../images/common/PTZ/ptzsavepreset_normal.png" 
									onMouseOver="ChangeImage('savePreset_btn','../images/common/PTZ/ptzsavepreset_press.png');"
									onMouseOut="ChangeImage('savePreset_btn','../images/common/PTZ/ptzsavepreset_normal.png');"
									title="<?php echo $t_setPreset[$GLOBALS['LANGINDEX']]; ?>"/>
							</div>						
						<?php 
							}
						?>
					
						<!-- FOCUS -->
							<div style="position:absolute;top:0px;left:-38px;">
								<img id="btnAutoFocus" src="../images/common/PTZ/AF_normal.png"
									onclick="javascript:OnClickAutoFocus()"
									onMouseOver="ChangeImage('btnAutoFocus','../images/common/PTZ/AF_press.png');"
									onMouseOut="ChangeImage('btnAutoFocus','../images/common/PTZ/AF_normal.png');"
									title="<?php echo $t_autoFocus[$GLOBALS['LANGINDEX']]; ?>" />
							</div>
							<div style="position:absolute;top:72px;left:-38px;">
								<img id="Near-Btn" src="../images/common/PTZ/near_normal.png"
									onMouseOver="ChangeImage('Near-Btn','../images/common/PTZ/near_press.png');"
									onMouseOut="SISOPlugin.ptzControl.onClickPtzStop(); ChangeImage('Near-Btn','../images/common/PTZ/near_normal.png');"
									onMouseDown="SISOPlugin.ptzControl.onClickFocus('Near');" 
									onMouseUp = "SISOPlugin.ptzControl.onClickPtzStop();" 
									title="<?php echo $t_near[$GLOBALS['LANGINDEX']]; ?>" />
							 </div>
							<div style="position:absolute;top:108px;left:-38px;">
								<img id="Far-Btn" src="../images/common/PTZ/far_normal.png"
									onMouseOver="ChangeImage('Far-Btn','../images/common/PTZ/far_press.png');"
									onMouseOut="SISOPlugin.ptzControl.onClickPtzStop(); ChangeImage('Far-Btn','../images/common/PTZ/far_normal.png');" 
									onMouseDown="SISOPlugin.ptzControl.onClickFocus('Far');" 
									onMouseUp = "SISOPlugin.ptzControl.onClickPtzStop();" 
									title="<?php echo $t_far[$GLOBALS['LANGINDEX']]; ?>" />
							</div>
					
						<!-- ZOOM -->
							<div style="position:absolute;top:118px;left:198px;">
								<img id="Minus-Btn" src="../images/common/PTZ/zoomout_normal.png"
									onMouseOver="ChangeImage('Minus-Btn','../images/common/PTZ/zoomout_press.png');"
									onMouseOut="SISOPlugin.ptzControl.onClickPtzStop(); ChangeImage('Minus-Btn','../images/common/PTZ/zoomout_normal.png');"
									onMouseDown="SISOPlugin.ptzControl.onClickZoom('Out', 'btn');"
									onMouseUp = "SISOPlugin.ptzControl.onClickPtzStop();"
									title="<?php echo $t_zoomOut[$GLOBALS['LANGINDEX']]; ?>" />
								<img id="Minus-Btn-Disable" src="../images/common/PTZ/zoomout_normal.png" style="display:none; cursor:default;"/>
							</div>
							<div style="position:absolute;top:0px;left:198px;">
								<img id="Plus-Btn" src="../images/common/PTZ/zoomin_normal.png"
									onMouseOver="ChangeImage('Plus-Btn','../images/common/PTZ/zoomin_press.png');"
									onMouseOut="SISOPlugin.ptzControl.onClickPtzStop(); ChangeImage('Plus-Btn','../images/common/PTZ/zoomin_normal.png');"
									onMouseDown="SISOPlugin.ptzControl.onClickZoom('In', 'btn');"
									onMouseUp = "SISOPlugin.ptzControl.onClickPtzStop();"
									title="<?php echo $t_zoomIn[$GLOBALS['LANGINDEX']]; ?>" />
								<img id="Plus-Btn-Disable" src="../images/common/PTZ/zoomin_normal.png" style="display:none; cursor:default;"/>
							</div>
					
						<!-- SPEED -->
							<div id="ptzSpeed" style="height:80px;position:absolute;top:28px;left:207px;"></div>
						</div>
					</div> <!-- end ptzcontrol-->
					<?php }else if($event_name == 'externalPTZ'){ ?>	
					<div id="PTZArea" style="background: url(../images/common/ExternalPtz/BOX_bg.png); background-repeat: no-repeat;height:128px; width:128px;"></div>
					<div style="width:50px;position:absolute;top:-8px;left:37px;">
						<img id="Top-Btn" src="../images/common/ExternalPtz/top.png" usemap="#top" />
						<map name="top"
							onMouseOut="ChangeImage('Top-Btn','../images/common/ExternalPtz/top.png');OnClickExternalPTZ(0);"
							onMouseover="ChangeImage('Top-Btn','../images/common/ExternalPtz/top_press.png');"
							onDragstart=""
							onMouseDown="OnClickExternalPTZ(1);ChangeImage('Top-Btn','../images/common/ExternalPtz/top_press.png');"
							onMouseUp = "OnClickExternalPTZ(0);">
							<area shape="poly" coords="0,13 , 60,13, 52,42, 8,42 " />
						</map>
					</div>
					<div style="width:50px;position:absolute;top:4px;left:2px;">
						<img id="TopLeft-Btn" src="../images/common/ExternalPtz/top_left.png" usemap="#top_left" />
						<map name="top_left"
							onMouseOut="ChangeImage('TopLeft-Btn','../images/common/ExternalPtz/top_left.png');OnClickExternalPTZ(0);"
							onMouseover="ChangeImage('TopLeft-Btn','../images/common/ExternalPtz/top_left_press.png');"
							onDragstart=""
							onMouseDown="OnClickExternalPTZ(5);ChangeImage('TopLeft-Btn','../images/common/ExternalPtz/top_left_press.png');"
							onMouseUp = "OnClickExternalPTZ(0);">
							<area shape="poly" coords="2,40, 40,2, 52,25, 25,52" />
						</map>
					</div>
					<div style="width:50px;position:absolute;top:4px;left:74px;">
						<img id="TopRight-Btn" src="../images/common/ExternalPtz/top_right.png" usemap="#top_right" />
						<map name="top_right"
							onMouseOut="ChangeImage('TopRight-Btn','../images/common/ExternalPtz/top_right.png');OnClickExternalPTZ(0);"
							onMouseover="ChangeImage('TopRight-Btn','../images/common/ExternalPtz/top_right_press.png');"
							onDragstart=""
							onMouseDown="OnClickExternalPTZ(6);ChangeImage('TopRight-Btn','../images/common/ExternalPtz/top_right_press.png');"
							onMouseUp = "OnClickExternalPTZ(0);">
							<area shape="poly" coords="5,28, 17,3, 57,43, 32,55" />
						</map>
					</div>
					<div style="width:50px;position:absolute;top:39px;left:-9px;">
						<img id="Left-Btn" src="../images/common/ExternalPtz/left.png" usemap="#left" />
						<map name="left"
							onMouseOut="ChangeImage('Left-Btn','../images/common/ExternalPtz/left.png');OnClickExternalPTZ(0);"
							onMouseover="ChangeImage('Left-Btn','../images/common/ExternalPtz/left_press.png');"
							onDragstart=""
							onMouseDown="OnClickExternalPTZ(3);ChangeImage('Left-Btn','../images/common/ExternalPtz/left_press.png');"
							onMouseUp = "OnClickExternalPTZ(0);" >
							<area shape="poly" coords="13,1, 40,12, 40,48, 13,59" />
						</map>
					</div>
					<div style="width:50px;position:absolute;top:40px;left:84px;">
						<img id="Right-Btn" src="../images/common/ExternalPtz/right.png" usemap="#right" />
						<map name="right"
							onMouseOut="ChangeImage('Right-Btn','../images/common/ExternalPtz/right.png');OnClickExternalPTZ(0);"
							onMouseover="ChangeImage('Right-Btn','../images/common/ExternalPtz/right_press.png');"
							onDragstart=""
							onMouseDown="OnClickExternalPTZ(4);ChangeImage('Right-Btn','../images/common/ExternalPtz/right_press.png');"
							onMouseUp = "OnClickExternalPTZ(0);">
							<area shape="poly" coords="15,12, 44,0, 44,59, 15,48" />
						</map>
					</div>
					<div style="width:50px;position:absolute;top:75px;left:3px;">
						<img id="DownLeft-Btn" src="../images/common/ExternalPtz/bottom_left.png" usemap="#down_left" />
						<map name="down_left"
							onMouseOut="ChangeImage('DownLeft-Btn','../images/common/ExternalPtz/bottom_left.png');OnClickExternalPTZ(0);"
							onMouseover="ChangeImage('DownLeft-Btn','../images/common/ExternalPtz/bottom_left_press.png');"
							onDragstart=""
							onMouseDown="OnClickExternalPTZ(7);ChangeImage('DownLeft-Btn','../images/common/ExternalPtz/bottom_left_press.png');"
							onMouseUp = "OnClickExternalPTZ(0);">
							<area shape="poly" coords="1,17, 26,7, 52,33, 41,58" />
						</map>
					</div>
					<div style="width:50px;position:absolute;top:75px;left:71px;">
						<img id="DownRight-Btn" src="../images/common/ExternalPtz/bottom_right.png" usemap="#down_right" />
						<map name="down_right"
							onMouseOut="ChangeImage('DownRight-Btn','../images/common/ExternalPtz/bottom_right.png');OnClickExternalPTZ(0);"
							onMouseover="ChangeImage('DownRight-Btn','../images/common/ExternalPtz/bottom_right_press.png');"
							onDragstart=""
							onMouseDown="OnClickExternalPTZ(8);ChangeImage('DownRight-Btn','../images/common/ExternalPtz/bottom_right_press.png');"
							onMouseUp = "OnClickExternalPTZ(0);">
							<area shape="poly" coords="7,30, 34,4, 59,16, 18,57" />
						</map>
					</div>
					<div style="width:50px;position:absolute;top:87px;left:37px;">
						<img id="Down-Btn" src="../images/common/ExternalPtz/bottom.png" usemap="#down" />
						<map name="down"
							onMouseOut="ChangeImage('Down-Btn','../images/common/ExternalPtz/bottom.png');OnClickExternalPTZ(0);"
							onMouseover="ChangeImage('Down-Btn','../images/common/ExternalPtz/bottom_press.png');"
							onDragstart=""
							onMouseDown="OnClickExternalPTZ(2);ChangeImage('Down-Btn','../images/common/ExternalPtz/bottom_press.png');"
							onMouseUp = "OnClickExternalPTZ(0);">
							<area shape="poly" coords="12,18, 47,18, 59,47, 0,47" />
						</map>
					</div>
					<div style="position:absolute;top:61px;left:-40px;">
						<img id="Near-Btn" src="../images/common/PTZ/near_normal.png"
							onMouseOver="ChangeImage('Near-Btn','../images/common/PTZ/near_press.png');"
							onMouseOut="OnClickExternalPTZ(0); ChangeImage('Near-Btn','../images/common/PTZ/near_normal.png');"
							onMouseDown="OnClickExternalPTZ(11);" 
							onMouseUp = "OnClickExternalPTZ(0);" 
							title="<?php echo $t_near[$GLOBALS['LANGINDEX']]; ?>" />
					 </div>
					<div style="position:absolute;top:95px;left:-40px;">
						<img id="Far-Btn" src="../images/common/PTZ/far_normal.png"
							onMouseOver="ChangeImage('Far-Btn','../images/common/PTZ/far_press.png');"
							onMouseOut="OnClickExternalPTZ(0); ChangeImage('Far-Btn','../images/common/PTZ/far_normal.png');" 
							onMouseDown="OnClickExternalPTZ(12);" 
							onMouseUp = "OnClickExternalPTZ(0);" 
							title="<?php echo $t_far[$GLOBALS['LANGINDEX']]; ?>" />
					</div>
					<div style="width:30px;position:absolute;top:37px;left:138px;">
						<img id="Minus-Btn" src="../images/common/ExternalPtz/zoom_in_normal.png"
							onMouseOver="ChangeImage('Minus-Btn','../images/common/ExternalPtz/zoom_in_press.png');"						
							onMouseOut="OnClickExternalPTZ(0);ChangeImage('Minus-Btn','../images/common/ExternalPtz/zoom_in_normal.png');"
							onMouseDown="OnClickExternalPTZ(10);"
							onMouseUp = "OnClickExternalPTZ(0);"
							title="<?php echo $t_zoomOut[$GLOBALS['LANGINDEX']]; ?>" />
					</div>
					<div style="width:30px;position:absolute;top:71px;left:138px;">
						<img id="Plus-Btn" src="../images/common/ExternalPtz/zoom_out_normal.png"
							onMouseOver="ChangeImage('Plus-Btn','../images/common/ExternalPtz/zoom_out_press.png');"
							onMouseOut="OnClickExternalPTZ(0);ChangeImage('Plus-Btn','../images/common/ExternalPtz/zoom_out_normal.png');"
							onMouseDown="OnClickExternalPTZ(9);"
							onMouseUp = "OnClickExternalPTZ(0);"
							title="<?php echo $t_zoomIn[$GLOBALS['LANGINDEX']]; ?>" />
					</div>
					<div style="width:40px;position:absolute;top:105px;left:138px;">
						<select id="externPtzSpeed" class="selectbox_style" style="width:40px;">
							<option value=1>1</option>
							<option value=2>2</option>
							<option value=3>3</option>
							<option value=4>4</option>
							<option value=5>5</option>
							<option value=6 selected="selected">6</option>
						</select>
					</div>					
					<?php } ?>					
					<?php if($GLOBALS["M_SUPPORT_AZIMUTH"]) { ?>
					<div id="azimuthArea" style="position:relative;display:none">
						<div style="position: absolute;top: -156px;left:610px;">
							<a href="javascript:OnClickAzimuthPosition()" class="btn_type01" style="width:50px;height:28px;cursor:pointer;" title="<?php echo $t_setNorth[$GLOBALS['LANGINDEX']]; ?>" >
								<img id="Azimuth-Btn" style="margin-top:3px"src="../images/common/btn_azimuth.png"/>
							</a>
						</div>
					</div>
					<?php } ?>
					<!-- PTZ Buttons-->
					<?php if($event_name == "videosetup" || $event_name == "ptztracking" ) {	 ?>
					<div style="position:relative;">
						<?php if ($GLOBALS['M_SUPPORT_PTZ']) { ?>
						<div id="VideoSetupEdit" style="position: absolute;top: -170px;left:450px;">
						<?php }else{ ?>
						<div id="VideoSetupEdit" style="position: absolute;top: -15px;left:392px;">
						<?php } ?>
							<div id="AreaList">
								<ul id="AreaNames"></ul>
							</div>
							<div class="DisableAreaList" style="display:none;"></div>
						</div>
						<?php if ($GLOBALS['M_SUPPORT_PTZ']) { ?>
						<div style="position:absolute;top:-37px;left:410px;">
						<?php }else{ ?>
						<div style="position:absolute;top:118px;left:352px;">
						<?php } ?>
							<img id="DeleteArea" src="../images/common/btn/remove_normal.png"
								onMouseOver="ChangeImage('DeleteArea','../images/common/btn/remove_cli.png');"
								onMouseOut="ChangeImage('DeleteArea','../images/common/btn/remove_normal.png');"
								title="<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>" />
							<img id="DeleteArea_disable" src="../images/common/btn/remove_normal.png"
								title="<?php echo $t_delete[$GLOBALS['LANGINDEX']]; ?>" 
								style="cursor:default; display:none;" />
						</div>
					<?php } ?>					
				</div>
	<script>
		$('.ptzControl').hide();
	</script>
	</td>
	</tr>
	<tr>
	<td>
		<div style="background-color:#2B313E;width:680px;height:17px;position:relative;">
			<?php if ($GLOBALS['M_SUPPORT_PTZ'] || $event_name == 'externalPTZ' || $event_name == "videosetup" || $event_name == "ptztracking") { ?>
			<img id="imgSlidePTZ" src="../images/common/PTZ/show.png" onclick="javascript:SISOPlugin.ptzControl.onClickPTZSlide();" style="margin-left:255px;cursor:pointer;" alt="lnb_arrow" />		

			<span id="showBtn" style="position:absolute;left:265px;top:0px;cursor:pointer;width:140px;text-align:center;" onclick="javascript:SISOPlugin.ptzControl.onClickPTZSlide();"><img style="position:relative;text-align:center;color:#fff;" src="../images/common/PTZ/show_btn.png" /> <?php echo $t_show[$GLOBALS['LANGINDEX']]; ?></span>
			<span id="hideBtn" style="position:absolute;left:265px;top:0px;cursor:pointer;width:140px;text-align:center;display:none" onclick="javascript:SISOPlugin.ptzControl.onClickPTZSlide();"><img style="position:relative;text-align:center;color:#fff;" src="../images/common/PTZ/hide_btn.png" /> <?php echo $t_hide[$GLOBALS['LANGINDEX']]; ?></span>		
			<?php } ?>
		</div>
	</td>
	</tr>
</table>

