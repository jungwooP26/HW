<?php
if(isset($_POST['uid']) && $_POST['uid'] != '')
{
    $uid = $_POST['uid'];
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
    echo "good";
    exit;
} else
{
    echo "bad";
    exit;
}

mysqli_close($conn);
?>