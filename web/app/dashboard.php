<?php
session_start();
require "db.php";

if (!isset($_SESSION["user_id"])) {
    header("Location: login.php");
    exit;
}

// Fetch user info from DB
$user_id = $_SESSION["user_id"];
$stmt = $conn->prepare("SELECT username, profile_pic FROM users WHERE id = ?");
$stmt->bind_param("i", $user_id);
$stmt->execute();
$stmt->bind_result($username, $profile_pic);
$stmt->fetch();
$stmt->close();

$profile_pic_url = "uploads/" . ($profile_pic ?: "default.png");
?>

<h1>Welcome, <?php echo $username; ?>!</h1>

<!-- Display Profile Picture -->
<img id="profilePic" src="<?php echo $profile_pic_url; ?>" alt="Profile Picture" width="150" height="150">

<!-- File Input for Uploading a New Profile Picture -->
<form id="uploadForm" enctype="multipart/form-data">
    <input type="file" name="profile_pic" id="profileInput">
    <button type="submit">Upload</button>
</form>

<p id="uploadMessage"></p> <!-- Display upload message -->

<a href="logout.php">Logout</a>

<!-- Include jQuery -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

<!-- AJAX Script for Uploading Profile Picture -->
<script>
    $(document).ready(function () {
        $("#uploadForm").submit(function (event) {
            event.preventDefault(); // Prevent form from reloading

            var formData = new FormData(this);

            $.ajax({
                type: "POST",
                url: "upload_profile_pic.php",
                data: formData,
                contentType: false,
                processData: false,
                success: function (response) {
                    $("#uploadMessage").text(response); // Show message
                    $("#profilePic").attr("src", $("#profilePic").attr("src") + "?" + new Date().getTime()); // Refresh profile picture
                },
                error: function () {
                    $("#uploadMessage").text("Error uploading profile picture.");
                }
            });
        });
    });
</script>
