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
            color: white; 
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
            line-height: 60px;
            font-size: 55px;
        }
    </style>
    <script type="text/javascript">
        $(function() {
            var k = $('.center_indicator');
            k.css('line-height', k.height()+'px');
            k.click(function() { window.location = 'menu.php'; });
            rqReload();
        });
        
        function rqReload() {
            $.post('/proxy.php', {gurl: '/get/temperatures/'}, function(data) {
                update(data);
                setTimeout(rqReload, 3000);                
            });
        }
    </script>
</head>
<body>

    <div id="all">
        <div class="tbox pleft ptop" style="background-color: green;">
            <div class="center_indicator" id="mkheating-external"></div>
            <div id="mbirrigation-rainMinutes" style="position: absolute; bottom: 0; right: 0; height: 20%;">
                <img src="/media/umbrella.png" style="height: 60px; display: inline;">
                <span id="mkirrigation-rainMinutes" style="color: white;"></span>
            </div>
        </div> 
        <div class="tbox pleft pbottom" style="background-color: blue;">
            <div class="center_indicator" id="mkheating-cwu"></div>
            <div class="pleft pbottom reftemp" id="mkheating-cwu_ref"></div>
            <img src="/media/kran.gif" id="mbheating-pump_load" class="pict" style="right: 0;">
            <img src="/media/pump.png" id="mbheating-pump_circ" class="pict" style="right: 20%;">
        </div> 
        <div class="tbox pright ptop" style="background-color: black;">
            <div class="center_indicator" id="mkheating-internal"></div>
            <div class="pleft pbottom reftemp" id="mkheating-internal_ref"></div>
            <div class="pright ptop reftemp" id="mkheating-up" style="text-align: right;"></div>
            <div class="pright pmiddle reftemp" id="mkheating-mid" style="text-align: right;"></div>
        </div> 
        <div class="tbox pright pbottom" style="background-color: red;">
            <div class="center_indicator" id="mkheating-boiler"></div>
            <div class="pleft pbottom reftemp" id="mkheating-co_ref"></div>
            <img src="/media/flame.png" id="mbheating-burner" class="pict" style="right: 0;">
            <img src="/media/pump.png" id="mbheating-pump_co" class="pict" style="right: 20%;">
        </div> 
        
    </div>
</body>
</html>