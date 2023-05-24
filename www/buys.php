<script>
    $(document).ready(function() {
        // Tabellen sortierbar machen
        $("#buys").tablesorter({
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
        $sql = "SELECT * FROM Buys WHERE status = 'NEW'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            echo "<p>Buys</p>";

            // Tabellenkopf ausgeben
            echo "<table id='buys'>";
            echo "<thead>";
            echo "<tr>";
            echo "<th>ID</th>";
            echo "<th>Symbol</th>";
            echo "<th>transactTime</th>";
            echo "<th>Price</th>";
            echo "<th>Qty</th>";
            echo "<th>Kind</th>";
            echo "</tr>";
            echo "</thead>";
            echo "<tbody>";

            // Datensätze ausgeben
            while ($row = $result->fetch_assoc()) {

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
                echo "<td>" . $row["origQty"] . "</td>";
                echo "<td>" . $row["kind"] . "</td>";
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