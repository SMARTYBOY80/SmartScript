<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $new_value = $_POST["new_value"] ?? "";

    if (!empty($new_value)) {
        $_SESSION["username"] = $new_value;
        echo "Session updated: " . $_SESSION["username"];
    } else {
        echo "Error: Value cannot be empty.";
    }
}
?>
