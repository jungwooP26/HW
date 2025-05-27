<?php
$conn = mysqli_connect("localhost", "root", "", "post");

$no = 0;
$title = '';
$content = '';
$password = '';
$action = '';

if (isset($_POST['POST_No'])) {
    $no = $_POST['POST_No'];
}
if (isset($_POST['title'])) {
    $title = $_POST['title'];
}
if (isset($_POST['content'])) {
    $content = $_POST['content'];
}
if (isset($_POST['password'])) {
    $password = $_POST['password'];
}
if (isset($_POST['action'])) {
    $action = $_POST['action'];
}

$result = mysqli_query($conn, "SELECT * FROM post WHERE POST_No = $no");
$row = mysqli_fetch_assoc($result);
$dbpw = $row['POST_password'];

if ($dbpw !== '' && $dbpw !== $password) {
    echo "Incorrect password.";
    exit;
}


if ($action == "edit") {
    mysqli_query($conn, "UPDATE post SET POST_Title='$title', POST_Content='$content' WHERE POST_No = $no");
    echo "The post has been successfully updated.";
    exit;
} elseif ($action == "delete") {
    mysqli_query($conn, "DELETE FROM post WHERE POST_No = $no");
    echo "The post has been successfully deleted.";
    exit;
}

mysqli_close($conn);
?>