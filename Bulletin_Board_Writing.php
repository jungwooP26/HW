<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Bulletin_Board_Writing</title>
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
        <div class="center">
            <h1>Bulletin Board > Writing</h1>
            <hr><br><br>
            <form id="writeForm">
                <table>
                    <tr>
                        <td><strong>Name</strong></td>
                        <td>
                            <input type="text" name="name" required style="width: 100%;">
                        </td>
                    </tr>
                    <tr>
                        <td><strong>Use Password</strong></td>
                        <td>
                            <input type="checkbox" id="use_pw" onclick="togglePasswordInput()">
                            Enable password
                        </td>
                    </tr>
                    <tr>
                        <td><strong>Password</strong></td>
                        <td>
                            <input type="password" name="password" id="password" style="width: 100%;" readonly>
                        </td>
                    </tr>
                    <tr>
                        <td><strong>Title</strong></td>
                        <td>
                            <input type="text" name="title" required style="width: 100%;">
                        </td>
                    </tr>
                    <tr>
                        <td><strong>Content</strong></td>
                        <td>
                            <textarea name="content" rows="10" required style="width: 100%;"></textarea>
                        </td>
                    </tr>
                </table>
                <br><br>
                <div class="btn-area">
                    <button type="submit">Save</button>
                    <button type="button" onclick="location.href='Bulletin_Board_list_view.php'">List</button>
                </div>
            </form>
        </div>

        <script>
            function togglePasswordInput() {
                const pwInput = document.getElementById('password');
                const checkbox = document.getElementById('use_pw');

                if (checkbox.checked == true) {
                    pwInput.readOnly = false;
                } else {
                    pwInput.readOnly = true;
                    pwInput.value = '';
                }
            }

            window.onload = function () {
                togglePasswordInput();
            };

            document.getElementById("writeForm").addEventListener("submit", function(event) {
                event.preventDefault();

                const form = document.getElementById("writeForm");
                const formData = new FormData(form);

                const Req = new XMLHttpRequest();
                Req.open("POST", "write_ajax.php", true);

                Req.onreadystatechange = function () {
                    if (Req.readyState == 4 && Req.status == 200) {
                        alert(Req.responseText);
                        if (Req.responseText.indexOf("successfully") >= 0) {
                            window.location.href = "Bulletin_Board_list_view.php";
                        }
                    }
                };

                Req.send(formData);
            });
        </script>
    </body>
</html>