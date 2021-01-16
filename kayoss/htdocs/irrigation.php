<?php
    include('proxy.php');
    if (!$authorized) { header('Location: login.php'); die(); }
?><!DOCTYPE html>
<html>
<head>
	<title>Irygacja</title>
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
            background-color: blue;
        }
		
			#section-visstan {
				width: 100%;
				background-color: blue;
				height: 110px;
				line-height: 110px;
				font-size: 4em;
				font-weight: bold;
				text-align: center;
				color: white;
			}
		
			.rainblock {
				float: left;
				width: 50%;
				background-color: lightblue;
			}
			.rainblock .descript {
				width: 100%;
				text-align: center;
				margin-top: 20px;
				color: white;
				font-size: 2em;
			}
			
			.rainblock .value {
				width: 100%;
				margin-top: 20px;
				font-size: 3em;
				margin-bottom: 15px;
				text-align: center;
				color: white;
			}

			#mbirrigation-rainMinutes {
				width: 100%;
				height: 50px;
				background-color: lightblue;
				line-height: 50px;
				color: white;
				font-size: 2em;
				text-align: center;
			}
			
			#mbirrigation-leakDetected {
				width: 100%;
				height: 50px;
				background-color: red;
				line-height: 50px;
				color: white;
				font-size: 2em;
				text-align: center;
			}
	
			.switch {
				width: 10%;
				height: 100px;
				color: white;
				float: left;
			}
			.switch .descr {
				width: 100%;
				font-size: 2em;
				line-height: 100px;
				text-align: center;
				transform: rotate(90deg);
				transform-origin: center middle 0;
				
			}
	
	</style>
    <script type="text/javascript">
		function dropper() {
			if ($(this).css('background-color') == 'rgb(0, 128, 0)')
				var tgtVal = 1;
			else
				var tgtVal = 0;
				
			$.post('/proxy.php', {gurl: '/set/irrigation/override/', 
				circuit: $(this).attr('data-id'),
				value: tgtVal}, function() { rqReload(true); });
		}
	
        $(function() {
            $('#section-visstan').click(function() { window.location = 'menu.php'; });
            $('.rainblock').click(function() { window.location = 'menu.php'; });
            $('#mbirrigation-leakDetected').click(function() { window.location = 'menu.php'; });
            $('#mbirrigation-rainMinutes').click(function() { window.location = 'menu.php'; });
			
			
            rqReload();
			
			$('#mscrirrigation-overrideS1').click(dropper);
			$('#mscrirrigation-overrideS2').click(dropper);
			$('#mscrirrigation-overrideS3').click(dropper);
			$('#mscrirrigation-overrideS4').click(dropper);
			$('#mscrirrigation-overrideS5').click(dropper);
			$('#mscrirrigation-overrideS6').click(dropper);
			
			$('#mscrirrigation-overrideNakr').click(dropper);
			$('#mscrirrigation-forbidDrop').click(dropper);
			$('#mscrirrigation-forbidIrrig').click(dropper);
			$('#mscrirrigation-forbidKos').click(dropper);
			
        });
        		
        function rqReload(dontreload) {
            $.post('/proxy.php', {gurl: '/get/irrigation/'}, function(data) {
                update(data);
				
				var visStan = {
					0:	'STOP',
					1: 	'S1: Od tarasu',
					2:	'S2: Przed domem',
					3:	'S3: Warzywnik',
					4:  'S4: Ogród lewa',
					5:  'S5: Rabata',
					6:	'S6: Ogród prawa',
					7:  'Kroplenie'
				};
				
				$('#section-visstan').html(visStan[data['irrigation-visStan']]);
				
				if (dontreload == null)
					setTimeout(rqReload, 3000);                
            });
        }
    </script>
</head>
<body>

    <div id="all">
	
		<div id="section-visstan"></div>
		<div class="rainblock">
			<div class="descript">Wczoraj</div>
			<div class="value"><strong id="mkirrigation-prevdayCounter"></strong>0 l</div>
		</div>
		<div class="rainblock">
			<div class="descript">Dzisiaj</div>
			<div class="value"><strong id="mkirrigation-dailyCounter"></strong>0 l</div>
		</div>
		<div style="clear: both;"></div>
				
		<div class="switch" id="mscrirrigation-overrideS1" data-id="s1"><div class="descr">S1</div></div>
		<div class="switch" id="mscrirrigation-overrideS2" data-id="s2"><div class="descr">S2</div></div>
		<div class="switch" id="mscrirrigation-overrideS3" data-id="s3"><div class="descr">S3</div></div>
		<div class="switch" id="mscrirrigation-overrideS4" data-id="s4"><div class="descr">S4</div></div>
		<div class="switch" id="mscrirrigation-overrideS5" data-id="s5"><div class="descr">S5</div></div>
		<div class="switch" id="mscrirrigation-overrideS6" data-id="s6"><div class="descr">S6</div></div>
		
		<div class="switch" id="mscrirrigation-overrideNakr" data-id="nakr"><div class="descr">SK</div></div>
		
		<div class="switch" id="mscrirrigation-forbidDrop" data-id="forbid_drop"><div class="descr">KROP</div></div>
		<div class="switch" id="mscrirrigation-forbidIrrig" data-id="forbid_irrig"><div class="descr">IRYG</div></div>
        
		<div class="switch" id="mscrirrigation-forbidKos" data-id="forbid_kos"><div class="descr">KOSR</div></div>

		<div id="mbirrigation-rainMinutes">Pada <span id="mkirrigation-rainMinutes"></span> minut</div>
		<div id="mbirrigation-leakDetected">WYKRYTO PRZECIEK</div>
    </div>
</body>
</html>