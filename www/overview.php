<?php

$ini = parse_ini_file('/mining/config/config.ini');

// Datenbankverbindung herstellen
$servername = $ini['MYSQL_HOST'];
$username = 'root';
$password = 'root';
$database = 'sqlalchemy';

$conn = new mysqli($servername, $username, $password, $database);

// Überprüfen der Verbindung
if ($conn->connect_error) {
    die("Verbindung fehlgeschlagen: " . $conn->connect_error);
}

// Binance API endpoint
$endpoint = "https://api.binance.com/api/v3/ticker/price";

// Create URL with symbol as a query parameter
$url = $endpoint;

// Initialize cURL session
$ch = curl_init();

// Set cURL options
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

// Execute the API request
$response = curl_exec($ch);

// Close cURL session
curl_close($ch);

// Process the response
$tickerData = json_decode($response, true);

// Create an associative array to store the prices for each symbol
$prices = array();
foreach ($tickerData as $ticker) {
    $symbol = $ticker['symbol'];
    $price = $ticker['price'];
    $prices[$symbol] = $price;
    $priceFormatted = rtrim($price, '0');
}

// SQL-Abfrage ausführen
$sql = "SELECT symbol, AVG(price) AS avg_price, AVG(origQty) AS avg_qty, SUM(origQty) AS total_qty FROM Buys WHERE status = 'FILLED' AND sellId IS NULL GROUP BY symbol";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<p>Trade-Auswertung</p>";

    // Tabellenkopf ausgeben
    echo "<table>";
    echo "<thead>";
    echo "<tr>";
    echo "<th>Symbol</th>";
    echo "<th>Aktueller Preis</th>";
    echo "<th>Durchschnittspreis</th>";
    echo "<th>Durchschnittliche Menge</th>";
    echo "<th>Gesamtmenge</th>";
    echo "<th>Durchschnittlicher Gewinn</th>";
    echo "</tr>";
    echo "</thead>";
    echo "<tbody>";

    // Datensätze ausgeben
    while ($row = $result->fetch_assoc()) {
        $symbol = $row["symbol"];
        $avgPrice = round($row["avg_price"], 3);
        $avgQty = round($row["avg_qty"], 3);
        $totalQty = round($row["total_qty"], 3);

        // Berechnung des durchschnittlichen Gewinns
        $averageProfit = ($prices[$symbol] - $avgPrice) * $avgQty;

        echo "<tr>";
        echo "<td>" . $symbol . "</td>";
        echo "<td>" . $prices[$symbol] . "</td>";
        echo "<td>" . $avgPrice . "</td>";
        echo "<td>" . $avgQty . "</td>";
        echo "<td>" . $totalQty . "</td>";
        echo "<td>" . $averageProfit . "</td>";
        echo "</tr>";
    }

    echo "</tbody>";
    echo "</table>";
} else {
    echo "Keine Ergebnisse gefunden.";
}

// Datenbankverbindung schließen
$conn->close();
?>
