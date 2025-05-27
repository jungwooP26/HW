<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Bulletin_Board_Editing</title>
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
            $POST_No = intval($_GET['POST_No']);
            $sql = "SELECT * FROM post WHERE POST_No = $POST_No";
            $result = mysqli_query($conn, $sql);

            if ($row = mysqli_fetch_assoc($result)) {
                $title = $row['POST_Title'];
                $name = $row['POSTER_name'];
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
            <h1>Bulletin Board > Editing</h1><hr><br>
            <form id="editForm">
                <input type="hidden" name="POST_No" value="<?php echo $POST_No; ?>">
                <table>
                    <tr>
                        <td><strong>Name</strong></td>
                        <td><input type="text" name="name" readonly value="<?php echo $name; ?>" style="width: 100%;"></td>
                    </tr>
                    <?php if ($row['POST_password'] !== ''): ?>
                    <tr>
                        <td><strong>Password</strong></td>
                        <td><input type="password" name="password" required style="width: 100%;"></td>
                    </tr>
                    <?php endif; ?>
                    <tr>
                        <td><strong>Title</strong></td>
                        <td><input type="text" name="title" value="<?php echo $title; ?>" required style="width: 100%;"></td>
                    </tr>
                    <tr>
                        <td><strong>Content</strong></td>
                        <td><textarea name="content" rows="10" required style="width: 100%;"><?php echo $content; ?></textarea></td>
                    </tr>
                </table>
                <br><br>
                <div class="btn-area">
                    <button type="button" onclick="submitForm('edit')">Save</button>
                    <button type="button" onclick="submitForm('delete')">Delete</button>
                    <button type="button" onclick="location.href='Bulletin_Board_list_view.php'">List</button>
                </div>
            </form>
        </div>

        <script>
        function submitForm(actionType) {
            const form = document.getElementById("editForm");
            const formData = new FormData(form);
            formData.set("action", actionType);

            const Req = new XMLHttpRequest();
            Req.open("POST", "save_delete_ajax.php", true);

            Req.onreadystatechange = function () {
                if (Req.readyState == 4 && Req.status == 200) {
                    alert(Req.responseText);
                    window.location.href = "Bulletin_Board_list_view.php";
                }
            };

            Req.send(formData);
        }
        </script>
    </body>
</html>