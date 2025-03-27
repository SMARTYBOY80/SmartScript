<?php
session_start();
require "db.php";


// Default profile picture
$profile_pic_url = "uploads/default.png";

// Check if user is logged in
$is_logged_in = isset($_SESSION["user_id"]);

if ($is_logged_in) {
    $user_id = $_SESSION["user_id"];
    $stmt = $conn->prepare("SELECT profile_pic FROM users WHERE id = ?");
    $stmt->bind_param("i", $user_id);
    $stmt->execute();
    $stmt->bind_result($profile_pic);
    $stmt->fetch();
    $stmt->close();

    if ($profile_pic) {
        $profile_pic_url = "uploads/" . $profile_pic;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Code Editor</title>
</head>
<body class="bg-black text-white flex flex-col items-center p-5">
<div class="w-full">
    <form id="codeForm" method="post">
        <!-- Navigation Bar -->
        <div class="w-full flex justify-between items-center p-4">
            <div class="flex justify-start w-1/3">
                <!-- Profile Picture -->
                <img src="<?php echo $profile_pic_url; ?>" alt="Profile Picture" width="50" height="50" class="rounded-full border-2 border-white">
            </div>
            <div class="flex justify-center w-1/3">
                <button type="submit" class="bg-green-500 text-white text-xl px-8 py-2 rounded-lg">RUN</button>
            </div>
            <div class="flex justify-end w-1/3">
                <?php if ($is_logged_in): ?>
                    <a href="dashboard.php" class="bg-blue-500 text-white px-4 py-1 rounded">Dashboard</a>
                    <a href="logout.php" class="bg-red-500 text-white px-4 py-1 rounded ml-2">Logout</a>
                <?php else: ?>
                    <a href="login.php" class="bg-blue-500 text-white px-4 py-1 rounded">Login</a>
                <?php endif; ?>
            </div>
        </div>

        <!-- Code Editor -->
        <div class="w-full h-auto bg-gray-700 p-8 flex space-x-4 mt-5 grid grid-cols-2 gap-4">
            <div class="w-full bg-black">
                <label for="input">Input:</label>
                <textarea class="bg-black text-white overflow-auto p-4 w-full" id="input" name="user_input" rows="30" cols="75" placeholder="Enter your code here"></textarea>
            </div>
            <div class="w-full bg-black">
                <label for="output">Output:</label>
                <textarea id="output" class="bg-black text-white overflow-auto p-4 w-full" rows="30" cols="75" readonly></textarea>
            </div>
        </div>
    </form>
</div>

<script>
    $(document).ready(function () {
        $("#codeForm").submit(function (event) {
            event.preventDefault(); // Prevent default form submission

            var formData = $(this).serialize(); // Serialize form data

            $.ajax({
                type: "POST",
                url: "code.php", // Ensure this is correct
                data: formData,
                success: function (response) {
                    $("#output").val(response); // Update textarea with response
                },
                error: function () {
                    $("#output").val("Error processing request.");
                }
            });
        });
    });
</script>
</body>
</html>
