<?php
$host = "localhost";
$user = "root"; // Default for XAMPP/MAMP
$password = ""; // Default is empty for XAMPP
$dbname = "user_db";

$conn = new mysqli($host, $user, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    dd("Connection failed: \n\n\n\n\n\n\n\n\n\n\n  " . $conn->connect_error);
}

?>
