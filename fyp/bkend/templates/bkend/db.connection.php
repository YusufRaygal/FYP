<?php
$servername = "localhost";
$username = "yusuf";
$password = "yusuf";
$dbname = "aiu_admission";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve form data
$first_name = $_POST['first_name'];
$last_name = $_POST['last_name'];
$country_code = $_POST['country_code'];
$contact_number = $_POST['contact_number'];
$primary_email = $_POST['primary_email'];
$secondary_email = $_POST['secondary_email'];
$password = password_hash($_POST['password'], PASSWORD_DEFAULT); // Hash password
$identity_card = $_POST['identity_card'];
$applicant_type = $_POST['applicant_type'];

// Insert data into the database
$sql = "INSERT INTO applicants (first_name, last_name, country_code, contact_number, primary_email, secondary_email, password, identity_card, applicant_type) 
        VALUES ('$first_name', '$last_name', '$country_code', '$contact_number', '$primary_email', '$secondary_email', '$password', '$identity_card', '$applicant_type')";

if ($conn->query($sql) === TRUE) {
    echo "Registration successful!";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

// Close connection
$conn->close();
?>
