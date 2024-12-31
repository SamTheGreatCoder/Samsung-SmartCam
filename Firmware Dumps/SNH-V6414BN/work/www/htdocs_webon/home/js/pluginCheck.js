var plugins = (function(){
    var found = {};
    var version_reg = /[0-9]+/;
 
    if (window.ActiveXObject || "ActiveXObject" in window) {
        var plugin_list = {
            flash: 'ShockwaveFlash.ShockwaveFlash.1',
            pdf: 'AcroPDF.PDF',
            silverlight: 'AgControl.AgControl',
            quicktime: 'QuickTime.QuickTime',
			sisoplugin: 'WEBVIEWER_ACTIVE.webviewer_activeCtrl.1'
        }
 
        for (var plugin in plugin_list){
            var version = msieDetect(plugin_list[plugin]);
            if (version){
                var version_reg_val = version_reg.exec(version);
                found[plugin] = (version_reg_val && version_reg_val[0]) || '';
            }
        }
 
        if (navigator.javaEnabled()){
            found['java'] = '';
        }
    } else {
        var plugins = navigator.plugins;
        var reg = /Flash|PDF|Java|Silverlight|QuickTime|WebViewer/;
        for (var i = 0; i < plugins.length; i++) {
            var reg_val = reg.exec(plugins[i].description);
            if (reg_val){
                var plugin = reg_val[0].toLowerCase();
                var version = plugins[i].version || 
                    (plugins[i].name + ' ' + plugins[i].description);
                var version_reg_val = version_reg.exec(version);
                if (!found[plugin]) {
                    found[plugin] = (version_reg_val && version_reg_val[0]) || '';
                }
            }
        }
    }
 
    return found;
 
    function msieDetect(name){
        try {
            var active_x_obj = new ActiveXObject(name);
            try {
                return active_x_obj.GetVariable('$version');
            } catch(e) {
                try {
                    return active_x_obj.GetVersions();
                } catch (e) {
                    try {
                        var version;
                        for (var i = 1; i < 9; i++) {
                            if (active_x_obj.isVersionSupported(i + '.0')){
                                version = i;
                            }
                        }
                        return version || true;
                    } catch (e) {
                        return true;
                    }
                }
            }
        } catch(e){
            return false;
        }
    }
})();
