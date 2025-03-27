<?php
session_start();
require "db.php";

if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_FILES["profile_pic"])) {
    $user_id = $_SESSION["user_id"];
    $upload_dir = "uploads/";

    // Ensure the upload directory exists
    if (!is_dir($upload_dir)) {
        mkdir($upload_dir, 0777, true);
    }

    $file_name = basename($_FILES["profile_pic"]["name"]);
    $file_tmp = $_FILES["profile_pic"]["tmp_name"];
    $file_ext = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));
    $new_file_name = "profile_" . $user_id . "." . $file_ext;
    $target_path = $upload_dir . $new_file_name;

    // Allowed file types
    $allowed_types = ["jpg", "jpeg", "png", "gif"];

    if (in_array($file_ext, $allowed_types)) {
        if (move_uploaded_file($file_tmp, $target_path)) {
            // Update the database with the new profile picture
            $stmt = $conn->prepare("UPDATE users SET profile_pic = ? WHERE id = ?");
            $stmt->bind_param("si", $new_file_name, $user_id);
            $stmt->execute();
            echo "Profile picture updated successfully!";
        } else {
            echo "Error uploading file.";
        }
    } else {
        echo "Invalid file type! Only JPG, PNG, and GIF are allowed.";
    }
}
?>
