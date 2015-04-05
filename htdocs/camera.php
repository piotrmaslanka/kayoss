<?php
    error_reporting(0);
    @ini_set('display_errors', 0);
	include('proxy.php');
	if (!$authorized) { header('Location: login.php'); die(); }

	define('CAMPATH', 'E:\\kamery');

	function get_cameras() {
		$k = scandir(CAMPATH);
		return array_slice($k, 2, count($k)-2, true);
	}

    function get_camera_days($camera) {
        $k = scandir(CAMPATH.'\\'.$camera);
		return array_slice($k, 2, count($k)-2, true);        
    }

	if (isset($_GET['feed'])) {
		// Output a image to stdout
		header('Content-Type: image/jpeg');
		if (isset($_GET['date'])) {
            // date is in form Y-M-D H:M:S
            sscanf($_GET['date'], "%d-%d-%d %d:%d:%d", $year, $month, $day, $hour, $minute, $second);
            $pp = CAMPATH.'\\'.$_GET['camera'].'\\'.sprintf("%'04d-%'02d-%'02d", $year, $month, $day).'\\'.sprintf("%'02d-%'02d-%'02d", $hour, $minute, $second).'.jpg';
            
            if (!file_exists($pp)) $pp = $pp . '.jpg';
            
			header('Content-Length: '.filesize($pp));
			header('X-Timestamp: '.$pp); 
            readfile($pp);
			// User picked a particular date/time
		} else {
			// Just get current image
			$pp = CAMPATH.'\\'.$_GET['camera'];
			$k = scandir($pp, 1);
			$k = ($k[0] == 'Thumbs.db') ? $k[1] : $k[0];
			// OK, we have all days now. Pick the most recent.
			$pp = $pp . '\\'. $k;

			// We have the most recent day, pick the most recent date
			$k = scandir($pp, 1);	
			$k = ($k[0] == 'Thumbs.db') ? $k[1] : $k[0];
			$pp = $pp.'\\'.$k;
			header('Content-Length: '.filesize($pp));
			header('X-Timestamp: '.$pp);
			readfile($pp);
		}
		flush();
		exit();
	}

	if (isset($_GET['camera'])) {

		// Ascertain disposition
		if ($_GET['dispo'] == 'fullscreen') {
			// Review current images.
			?><!DOCTYPE html>
		<html><head><title>Camera System</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<script type="text/javascript" src="/media/jquery-2.1.1.min.js"></script>
		<script type="text/javascript">
		function refresh() {
			$('#bg').attr('src', 'camera.php?camera=<?php echo $_GET['camera']; ?>&feed=1&random='+Math.random()*100000);
			setTimeout(refresh, 1000);
		}
		$(function() { 
			refresh();
			$("#bg").click(function() { window.location = 'menu.php'; });
		})
		</script>
		</head>
		<body style="margin: 0 0 0 0; overflow: hidden;"><div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;"><img id="bg" style="width: 100%; height: 100%;"></div></body></html>
			<?php
		}
        
        if ($_GET['dispo'] == 'pickhistory') {
            // pick history on a camera            
            $camdays = get_camera_days($_GET['camera']);
            ?><!DOCTYPE html>
		<html><head><title>Camera System</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<script type="text/javascript" src="/media/jquery-2.1.1.min.js"></script>
		<script type="text/javascript">
        var camd = null;
        function setcam(camday) {
            $('a').css('font-weight', 'normal');
            $('#'+camday).css('font-weight', 'bold');
            camd = camday;
        }
        function roll() {
            var hour = $('#hour').val();
            var minute = $('#minute').val();
            
            window.location = 'camera.php?camera=<?php echo $_GET['camera']; ?>&dispo=history&day='+camd+'&hour='+hour+'&minute='+minute;
        }
		</script>
		</head>
		<body>
            <table>
                <tr>
                    <td>
                        <?php foreach($camdays as $camday) { ?>
                        <a href="javascript:setcam('<?php echo $camday; ?>')" id="<?php echo $camday; ?>"><?php echo $camday; ?></a><br>
                        <?php } ?>
                    </td>
                    <td>
                        <input type="text" id="hour" value="0">:<input type="text" id="minute" value="0"><br><br>
                        <a href="javascript:roll()">OGLĄDAJ</a><br>
                        <a href="camera.php?history=1">KAMERY</a><br>
                    </td>
                </tr>
            </table>
        </body></html><?php
        }
        
        if ($_GET['dispo'] == 'history') {
            // Parse history that is starts from
            $day = $_GET['day'];
            $hour = $_GET['hour'];
            $minute = $_GET['minute'];
            
            
			// Review current images.
			?><!DOCTYPE html>
		<html><head><title>Camera System</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<script type="text/javascript" src="/media/jquery-2.1.1.min.js"></script>
		<script type="text/javascript">
        var day = "<?php echo $day; ?>";
        var hour = <?php echo $hour; ?>;
        var minute = <?php echo $minute; ?>;
        var second = 0;
		function next() {
			$('#bg').attr('src', 'camera.php?camera=<?php echo $_GET['camera']; ?>&feed=1&date='+day+'%20'+hour+'%3A'+minute+'%3A'+second+'&random='+Math.random()*100000);
            
            if (second == 59) {
                if (minute == 59) {
                    hour += 1;
                    minute = 0;
                } else 
                    minute += 1
                second = 0;
            } else 
                second += 1;
            
			setTimeout(next, 1000);
		}
		$(function() { 
			next();
			$("#bg").click(function() { history.go(-1); });
		})
		</script>
		</head>
		<body style="margin: 0 0 0 0; overflow: hidden;"><div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;"><img id="bg" style="width: 100%; height: 100%;"></div></body></html>
			<?php
        }

	} else {        
		$proxa = 'fullscreen';
        if (isset($_GET['history'])) $proxa = 'pickhistory';
		// Print all cameras
		?><!DOCTYPE html>
		<html><head><title>Camera System</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head>
		<body>
		<div style="font-size: 5em;">
		<a href="menu.php">MENU</a>&nbsp;           
		<?php
            if ($proxa == 'fullscreen') {
            ?> <a href="camera.php?history=1">ARCHIWUM</a> <?php } else { ?> <a href="camera.php">PODGLĄD</a> <?php }

            $k = 1;
			foreach (get_cameras() as $cam) {
				$k += 1;
				echo ('<a href="camera.php?camera='.$cam.'&dispo='.$proxa.'">'.$cam.'</a>&nbsp;&nbsp;');
				if ($k == 2) { echo('<br>'); $k = 0; }
			}
		?>
		</div>
		</body></html>
		<?php
	}
?>