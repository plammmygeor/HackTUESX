<?php
// Database connection
$servername = "your_mysql_server";
$username = "your_mysql_username";
$password = "your_mysql_password";
$dbname = "your_database_name";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

// Get state value from POST request
if(isset($_POST['state'])) {
  $state = $_POST['state'];
  
  // Insert state value into the database
  $sql = "INSERT INTO smart_home_state (state_value) VALUES ($state)";
  if ($conn->query($sql) === TRUE) {
    echo "State inserted successfully";
  } else {
    echo "Error: " . $sql . "<br>" . $conn->error;
  }
}

$conn->close();
?>
