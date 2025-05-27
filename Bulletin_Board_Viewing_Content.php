<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Bulletin_Board_Viewing_Content</title>
        <link rel="stylesheet" href="style.css">
        <style>
            input, textarea {
                border: none;
                outline: none;
            }
            table {
                width: 70%;
                margin: 0 auto;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #888;
                padding: 8px;
                text-align: center;
            }
            .center {
                text-align: center;
                margin-top: 50px;
            }
            .btn-area {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <?php
        $host = "localhost";
        $user = "root";
        $password = "";
        $dbname = "post";

        $conn = mysqli_connect($host, $user, $password, $dbname);

        if (!$conn) {
            die("Connection failed: " . mysqli_connect_error());
        }

        if (isset($_GET['POST_No'])) {
            $POST_No = $_GET['POST_No'];
            $sql = "SELECT * FROM post WHERE POST_No = $POST_No";
            $result = mysqli_query($conn, $sql);

            if ($row = mysqli_fetch_assoc($result)) {
                $title = $row['POST_Title'];
                $name = $row['POSTER_name'];
                $date = $row['POST_Date'];
                $content = $row['POST_Content'];
            } else {
                echo "<script>alert('The post does not exist.'); location.href='Bulletin_Board_list_view.php';</script>";
                exit;
            }
        } else {
            echo "<script>alert('Invalid access.'); location.href='Bulletin_Board_list_view.php';</script>";
            exit;
        }

        mysqli_close($conn);
        ?>

        <div class="center">
            <h1>Bulletin Board > Viewing Content</h1><hr><br>
            <form>
                <table>
                    <tr>
                        <td><strong>Title</strong></td>
                        <td><input type="text" readonly value="<?php echo $title; ?>" style="width: 100%;"></td>
                    </tr>
                    <tr>
                        <td><strong>Name</strong></td>
                        <td><input type="text" readonly value="<?php echo $name; ?>" style="width: 100%;"></td>
                    </tr>
                    <tr>
                        <td><strong>Date</strong></td>
                        <td><input type="text" readonly value="<?php echo $date; ?>" style="width: 100%;"></td>
                    </tr>
                    <tr>
                        <td><strong>Content</strong></td>
                        <td><textarea readonly rows="10" style="width: 100%;"><?php echo $content; ?></textarea></td>
                    </tr>
                </table>
                <br><br>
                <div class="btn-area">
                    <button type="button" onclick="location.href='Bulletin_Board_Editing.php?POST_No=<?php echo $POST_No; ?>'">Edit</button>
                    <button type="button" onclick="location.href='Bulletin_Board_list_view.php'">List</button>
                </div>
            </form>
        </div>
    </body>
</html>