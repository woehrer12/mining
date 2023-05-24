<script>
    $(document).ready(function() {
        // Tabellen sortierbar machen
        $("#trades").tablesorter({
            theme: 'default',
            widgets: ['zebra'],
            headerTemplate: '{content}{icon}',
            headers: { 
                // Pfeilsymbole für die sortierten Spalten hinzufügen
                0: { sorter: false },
                1: { sorter: 'text' },
                2: { sorter: 'text' },
                3: { sorter: 'digit' },
                4: { sorter: 'digit' },
                5: { sorter: 'text' }
            }
        });
    });
</script>

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

        // SQL-Abfrage ausführen
        $sql = "SELECT * FROM Buys WHERE status = 'FILLED' AND sellId IS NULL";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            echo "<p>Trades</p>";

            // Tabellenkopf ausgeben
            echo "<table id='trades'>";
            echo "<thead>";
            echo "<tr>";
            echo "<th>ID</th>";
            echo "<th>Symbol</th>";
            echo "<th>transactTime</th>";
            echo "<th>Price</th>";
            echo "<th>Actual Price</th>";
            echo "<th>Trailing</th>";
            echo "<th>Percent</th>";
            echo "<th>Qty</th>";
            echo "<th>USDT</th>";
            echo "<th>Profitloss</th>";
            echo "<th>Kind</th>";
            echo "</tr>";
            echo "</thead>";
            echo "<tbody>";

            // Datensätze ausgeben
            while ($row = $result->fetch_assoc()) {

                // Generate the sell link with the trade ID as a parameter
                $sellLink = "http://localhost:5001/sell?Id=" . $row["trade_id"];

                // Binance API endpoint
                $endpoint = "https://api.binance.com/api/v3/ticker/price";

                // Create URL with symbol as a query parameter
                $url = $endpoint . "?symbol=" . $row["symbol"];

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
                if ($response !== false) {
                    $tickerData = json_decode($response, true);

                    // Check if the response contains valid data
                    if (isset($tickerData['symbol']) && isset($tickerData['price'])) {
                        $symbol = $tickerData['symbol'];
                        $price = $tickerData['price'];
                        $priceFormatted = rtrim($price, '0');

                    } else {
                        echo "Invalid response from the API\n";
                    }
                } else {
                    echo "Failed to make the API request\n";
                }
                

                // Convert the values to numeric format
                $currentPrice = floatval($price);
                $previousPrice = floatval($row["price"]);

                // Calculate the percentage difference
                $percentageDifference = (($currentPrice - $previousPrice) / $previousPrice) * 100;


                // Calculate the profit or loss in USDT
                $buyPrice = floatval($row["price"]);
                $qty = floatval($row["origQty"]);
                $cummulativeQuoteQty = floatval($row["cummulativeQuoteQty"]);
                $currentValue = $currentPrice * $qty;
                $profitLoss = $currentValue - $cummulativeQuoteQty;
                $profitLossrounded = round($profitLoss, 2);

                // Determine the color and arrow direction based on the percentage difference
                if ($percentageDifference > 0) {
                    $color = "green";
                    $arrow = "&#8593;"; // Upward arrow
                } elseif ($percentageDifference < 0) {
                    $color = "red";
                    $arrow = "&#8595;"; // Downward arrow
                } else {
                    $color = "gray";
                    $arrow = "&#8596;"; // Horizontal arrow
                }

                $epochTimeInSeconds = intval($row["transactTime"]/1000);

                // Datumsformat festlegen (z.B. "d.m.Y H:i:s")
                $dateFormat = "d.m.Y H:i:s";

                // Epoch-Zeit in Datumsformat umwandeln
                $convertedDate = date($dateFormat, $epochTimeInSeconds);

                echo "<tr>";
                echo "<td>" . $row["trade_id"] . "</td>";
                echo "<td>" . $row["symbol"] . "</td>";
                echo "<td>" . $convertedDate . "</td>";
                echo "<td>" . $row["price"] . "</td>";
                echo "<td>" . $priceFormatted . "</td>";
                echo "<td>". $row["trailingProfit"]. "</td>";
                echo "<td style='color: $color;'>" . round($percentageDifference, 2) . "% $arrow</td>";
                echo "<td>" . $row["origQty"] . "</td>";
                echo "<td>". $row["cummulativeQuoteQty"]. "</td>";
                echo "<td>" . $profitLossrounded . "</td>";
                echo "<td>" . $row["kind"] . "</td>";
                echo "<td><a href=\"$sellLink\">Sell</a></td>";
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