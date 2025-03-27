<?php

$userInput = '';
$output = shell_exec('python3 -m app test.jjs');
$python = '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the input from the textarea
    $userInput = $_POST['user_input'] ?? '';

    // Generate a unique file name with a .jjs extension
    $filePath = uniqid("smartScript_", true) . ".jjs";

    // Save user input to the file
    file_put_contents($filePath, $userInput);

    // Construct the command to run the Python script with the created file as input
    $escapedFilePath = escapeshellarg($filePath);

    $command = $python . ' -m app '. $filePath; // Run user code through Python interpreter

    // Execute the command and capture output
    $output = shell_exec($command. " 2>&1");

    // Check for errors
    if ($output === null) {
        $output = "Error executing the command.";
    }

    // Clean up the temporary file
    if (file_exists($filePath)) {
        unlink($filePath);
    }
}
echo $output;
return $output;
?>

