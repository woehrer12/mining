<!DOCTYPE html>
<html>
<head>
    <title>Aktuelles Datum und Uhrzeit</title>
    <style>
        body {
            background-color: #1c1c1e;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }

        h1 {
            color: #ffffff;
        }

        p {
            color: #ffffff;
        }

        a {
            color: #3897f0;
        }

        table {
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            border: 1px solid #ffffff;
            padding: 8px;
            text-align: left;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/js/jquery.tablesorter.min.js"></script>
    <script>
        $(document).ready(function() {
            // Tabellen sortierbar machen
            $("#myTable").tablesorter();
        });
    </script>
</head>
<body>
    <h1>Aktuelles Datum und Uhrzeit</h1>

    <?php
        // Aktuelles Datum und Uhrzeit ermitteln
        $aktuellesDatum = date('d.m.Y');
        $aktuelleUhrzeit = date('H:i:s');

        // Ausgabe des aktuellen Datum und Uhrzeit
        echo "<p>Datum: $aktuellesDatum</p>";
        echo "<p>Uhrzeit: $aktuelleUhrzeit</p>";

        // Datenbankverbindung herstellen
        $servername = '172.30.0.2';
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
            echo "<table id='myTable'>";
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

    <p>
        Weitere Informationen:
        <a href="info.php">Hier klicken</a>
    </p>
</body>
</html>
