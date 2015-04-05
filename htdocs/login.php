<?php
    include('proxy.php');
    if ($authorized) { header('Location: menu.php'); die(); }
?><!DOCTYPE html>
<html>
    <head>
        <title>Login</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    </head>
    <body>

       <form action="login.php" method="post">
            Password: <input type="password" name="password"><br>
            <input type="submit" value="OK">
        </form>
        
    </body>
</html>