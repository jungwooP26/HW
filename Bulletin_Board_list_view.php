<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Bulletin_Board_list_view</title>
        <link rel="stylesheet" href="style.css">
        <style>
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
        <div class="center">
            <h1>Bulletin Board > List view</h1>
            <hr><br>

            <table>
                <tr>
                    <th>No.</th>
                    <th>Title</th>
                    <th>Name</th>
                    <th>Date</th>
                </tr>

                <?php
                $host = "localhost";
                $user = "root";
                $password = "";
                $dbname = "post";

                $conn = mysqli_connect($host, $user, $password, $dbname);

                if (!$conn) {
                    die("Connection failed: " . mysqli_connect_error());
                }

                $sql = "SELECT POST_No, POST_Title, POSTER_name, POST_Date FROM post ORDER BY POST_No DESC";
                $result = mysqli_query($conn, $sql);

                if (mysqli_num_rows($result) > 0) {
                    $i = 1;
                    while ($row = mysqli_fetch_assoc($result)) {
                        echo "<tr>";
                        echo "<td>" . $i . "</td>";
                        echo "<td><a href='Bulletin_Board_Viewing_Content.php?POST_No=" . $row['POST_No'] . "'>" . htmlspecialchars($row['POST_Title']) . "</a></td>";
                        echo "<td>" . htmlspecialchars($row['POSTER_name']) . "</td>";
                        echo "<td>" . $row['POST_Date'] . "</td>";
                        echo "</tr>";
                        $i++;
                    }
                } else {
                    echo "<tr><td colspan='4'>No posts found.</td></tr>";
                }

                mysqli_close($conn);
                ?>
            </table>

            <br><hr><br>
            <div class="btn-area">
                <button onclick="location.href='Bulletin_Board_Writing.php'">Write</button>
                <button onclick="location.href='index.html'">Logout</button>
            </div>
        </div>
    </body>
</html>