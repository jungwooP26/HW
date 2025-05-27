<?php
if(isset($_POST['uid']) && $_POST['uid'] != '' && isset($_POST['upw']) && $_POST['upw'] != '')
{
    $uid = $_POST['uid'];
    $upw = $_POST['upw'];
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

$id_sql = "SELECT * FROM users WHERE user_id = '$uid'";
$id_result = mysqli_query($conn, $id_sql);

if(mysqli_num_rows($id_result) == 0)
{
    echo "no_inf";
    exit;
} else
{
    $login_sql = "SELECT * FROM users WHERE user_id = '$uid' AND user_password = '$upw'";
    $login_result = mysqli_query($conn, $login_sql);

    if(mysqli_num_rows($login_result) == 1)
    {
        echo "success";
        exit;
    } else if(mysqli_num_rows($login_result) == 0)
    {
        echo "wrong_pw";
        exit;
    }
}

mysqli_close($conn);
?>