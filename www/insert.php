<?php
$ini = parse_ini_file('/mining/config/config.ini');

// Datenbankverbindung herstellen
$servername = $ini['MYSQL_HOST'];
$username = 'root';
$password = 'root';
$database = 'sqlalchemy';

$conn = new mysqli($servername, $username, $password, $database);

if ($conn->connect_error) {
    die("Verbindung fehlgeschlagen: " . $conn->connect_error);
}

// Eingabewerte aus dem Formular abrufen
$symbol = $_POST['symbol'];
$price = $_POST['price'];
$qty = $_POST['qty'];
$transactTime = round(microtime(true) * 1000);
$status = "FILLED";
$kind = "Slow";
$USDT = $_POST['usdt'];

// SQL-Abfrage zum Einfügen des neuen Eintrags
$sql = "INSERT INTO Buys (symbol, price, origQty, executedQty, transactTime, status, kind, cummulativeQuoteQty) VALUES ('$symbol', '$price', '$qty', '$qty', '$transactTime', '$status', '$kind', '$USDT')";

if ($conn->query($sql) === TRUE) {
    echo "Neuer Eintrag erfolgreich hinzugefügt.";
    sleep(2);
    header("Location: index.php");
    exit();
} else {
    echo "Fehler beim Hinzufügen des Eintrags: " . $conn->error;
}

$conn->close();
?>
