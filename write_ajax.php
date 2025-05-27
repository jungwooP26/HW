<?php
$conn = mysqli_connect("localhost", "root", "", "post");

if ($conn == false) {
    echo "Database connection failed.";
    exit;
}

$name = $_POST['name'];
$pw = isset($_POST['password']) ? $_POST['password'] : '';
$title = $_POST['title'];
$content = $_POST['content'];
$date = date('Y-m-d');

$sql = "INSERT INTO post (POST_Title, POSTER_name, POST_Content, POST_Date, POST_password)
        VALUES ('$title', '$name', '$content', '$date', '$pw')";

if (mysqli_query($conn, $sql)) {
    echo "The post has been successfully submitted.";
} else {
    echo "Failed to submit the post: " . mysqli_error($conn);
}

mysqli_close($conn);
?>