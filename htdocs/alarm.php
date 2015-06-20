<?php
    include('proxy.php');
    if (!$authorized) { header('Location: login.php'); die(); }
?><!DOCTYPE html>
<html>
<head>
	<title>Alarm</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf=8">
    <script type="text/javascript" src="/media/jquery-2.1.1.min.js"></script>
    <script type="text/javascript" src="/media/common.js"></script>
    <link rel="stylesheet" type="text/css" href="/media/reset.css">
    <style type="text/css">
        #all {
            position: absolute;
            top: 0; left: 0;
            bottom: 0; right: 0;
			overflow: hidden;
            background-color: yellow;
        }

        table, #tab { 
            z-index: 1;
            margin: auto;
            width: 400px;
        }
        
        .circuit {
            background-color: green;
            padding: 10px 10px 10px 10px;
            text-align: center;
            border: 1px solid black;
            font-size: 400%;
            color: white;
        }
	
	</style>
    <script type="text/javascript">
	
        function reload() {
            $.post('/proxy.php', {gurl: '/alarm/get/'}, function(data) {
                var ap = data['alarm-presence'];
                var ax = data['alarm-mask'];
                var al = [0, 0, 0, 0, 0];
            
                if (data['failures-alarm'] == 0) 
                    $("#all").css('background-color', 'green');
                else
                    $("#all").css('background-color', 'red');
                
                // 0 - Nothing, 1 - Present, 2 - Masked, 3 - Alarm
                if (ap & 1) al[0] += 1; if (ax & 1) al[0] += 2;
                if (ap & 2) al[1] += 1; if (ax & 2) al[1] += 2;
                if (ap & 4) al[2] += 1; if (ax & 4) al[2] += 2;
                if (ap & 8) al[3] += 1; if (ax & 8) al[3] += 2;
                if (ap & 16) al[4] += 1; if (ax & 16) al[4] += 2;

                for (var i=0; i<5; i++) {
                    if (al[i] == 0) {
                        $("#c"+i).attr('al-masked', '0'); $("#c"+i).attr('al-present', '0');
                        $("#c"+i).css('background-color', 'green');
                    } else if (al[i] == 1) {
                        $("#c"+i).attr('al-masked', '0'); $("#c"+i).attr('al-present', '1');
                        $("#c"+i).css('background-color', 'black');
                    } else if (al[i] == 2) {
                        $("#c"+i).attr('al-masked', '1'); $("#c"+i).attr('al-present', '0');
                        $("#c"+i).css('background-color', 'yellow');
                    } else if (al[i] == 3) {
                        $("#c"+i).attr('al-masked', '1'); $("#c"+i).attr('al-present', '1');
                        $("#c"+i).css('background-color', 'red');
                    }
                }
                
                $.post('/proxy.php', {gurl: '/alarm/clear/persistence/'}, function() { setTimeout(reload, 3000); });
            });        
        }
        
        function rearm(what) {
            var isMasked = ($("#c"+what).attr('al-masked') == 1);
            
            if (isMasked) 
                $.post('/proxy.php', {gurl: '/alarm/disarm/', 'circuit': what});
            else
                $.post('/proxy.php', {gurl: '/alarm/arm/', 'circuit': what});
        }
        
        $(function() {			
            reload();
			
            $('#all').click(function() { window.location = 'menu.php'; });
			$('#c0').click(function(e) { rearm(0); e.stopPropagation(); });
			$('#c1').click(function(e) { rearm(1); e.stopPropagation(); });
			$('#c2').click(function(e) { rearm(2); e.stopPropagation(); });
			$('#c3').click(function(e) { rearm(3); e.stopPropagation(); });
			$('#c4').click(function(e) { rearm(4); e.stopPropagation(); });
        });
    </script>
</head>
<body>
    <div id="all">
        <div id="tab">
        <table>
            <tr><td class="circuit" id="c0">Sabota&zdot;</td></tr>
            <tr><td class="circuit" id="c1">Schody</td></tr>
            <tr><td class="circuit" id="c2">Korytarz</td></tr>
            <tr><td class="circuit" id="c3">Piwnica</td></tr>
            <tr><td class="circuit" id="c4">Kom&oacute;rka</td></tr>
        </table>
        </div>
    </div>
</body>
</html>