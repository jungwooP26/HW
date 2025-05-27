<?php
if (isset($_POST['uid']) && $_POST['uid'] != '' && isset($_POST['upw']) && $_POST['upw'] != '' && isset($_POST['uname']) && $_POST['uname'] != '' && isset($_POST['uemail']) && $_POST['uemail'] != '') {
    $uid = $_POST['uid'];
    $upw = $_POST['upw'];
    $uname = $_POST['uname'];
    $uemail = $_POST['uemail'];
} else {
    echo "no_input";
    exit;
}

$host = "localhost";
$user = "root";
$password = "";
$dbname = "user";

$conn = mysqli_connect($host, $user, $password, $dbname);

if(!$conn)
{
    die("Connection failed: " . mysqli_connect_error());
}

$sql = "INSERT INTO users (user_id, user_password, user_name, user_email)
        VALUES ('$uid', '$upw', '$uname', '$uemail')";

if (mysqli_query($conn, $sql)) {
    echo "success";
} else {
    echo "fail";
}

mysqli_close($conn);
?>