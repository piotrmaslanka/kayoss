<?php
	include('proxy.php');
	if (!$authorized) { header('Location: login.php'); die(); }
?><!DOCTYPE html>
<html><head><title>BMS</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<script type="text/javascript" src="/media/jquery-2.1.1.min.js"></script>
</script>
</head>
<body>
<div>
	<a href="heating.php" style="font-size: 5em;">OGRZEWANIE</a><br><br>
	<a href="camera.php" style="font-size: 5em;">KAMERA</a>
</div>
</body>
</html>