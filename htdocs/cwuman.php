<?php
    include('proxy.php');
    if (!$authorized) { header('Location: login.php'); die(); }
?><!DOCTYPE html>
<html>
<head>
    <script type="text/javascript" src="/media/jquery-2.1.1.min.js"></script>
    <script type="text/javascript" src="/media/common.js"></script>
    <link rel="stylesheet" type="text/css" href="/media/reset.css">
    <style type="text/css">
        #all {
            position: absolute;
            top: 0; left: 0;
            bottom: 0; right: 0;
            background-color: yellow;
            font-size: 3em;
        }
        .tbox {
            position: absolute;
            width: 50%;
            height: 50%;
        }

        .pleft { left: 0; }
        .pright { right: 0; }
        .ptop { top: 0; }
        .pbottom { bottom: 0; }
        .pmiddle { top: 40%; }
        
        .center_indicator { position: absolute; top: 0; right: 0; bottom: 0; left: 0; z-index: 1;
                            color: white; text-align: center; 
                            height: 100%; font-size: 115px; }
        .reftemp { 
            text-align: left; 
            color: red;
            z-index: 1; height: 60px; font-size: 55px;
            position: absolute;
        }
        
        .pict {
            position: absolute;
            height: 60px;
            width: 60px;
            z-index: 1;
            bottom: 0;
        }

        #mbirrigation-rainMinutes {
			position: absolute;
			bottom: 0; right: 0;
            line-height: 60px;
			height: 60px;
            font-size: 55px;
        }
    </style>
    <script type="text/javascript">
        $(function() {
            var k = $('#all');
            k.click(function() { window.location = 'menu.php'; });
            rqReload();
            
            $("#forbid_cwu").click(function(e) {
                $.post('/proxy.php', {gurl: '/cwu_heating_state/antimake/'});
                e.stopPropagation();
                
            });
            
            $("#load_cwu").click(function(e) {
                $.post('/proxy.php', {gurl: '/cwu_heating_state/make/'});
                e.stopPropagation();
            });
        });
        
        function rqReload() {
            $.post('/proxy.php', {gurl: '/get/temperatures/'}, function(data) {
                update(data);
                setTimeout(rqReload, 3000);                
            });        
            $.post('/proxy.php', {gurl: '/get/cwu_heating_state/'}, function(data) {
                if (data['heating-cwu-system_state'] == 0)
                    $("#xheating-cwu-system_state").html("AUTO");
                if (data['heating-cwu-system_state'] == 1)
                    $("#xheating-cwu-system_state").html("£ADUJ");
                if (data['heating-cwu-system_state'] == 2)
                    $("#xheating-cwu-system_state").html("OSZCZÊDZAJ");
                setTimeout(rqReload, 3000);                
            });
        }
    </script>
</head>
<body>

    <div id="all">
        <span id="xheating-cwu-system_state"></span><br>
        <button id="load_cwu" style="font-size: 1.2em;">Za³aduj CWU</button><br>
        <button id="forbid_cwu" style="font-size: 1.2em;">Zabroñ CWU</button><br>
        Obecna CWU: <span id="mkheating-cwu"></span>C<br>
        Ref CWU: <span id="mkheating-cwu_ref"></span>C<br>
    </div>
</body>
</html>