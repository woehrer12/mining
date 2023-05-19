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
    </style>
</head>
<body>
    <h1>Aktuelles Datum und Uhrzeit</h1>

    <?php
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
        $sql = "SELECT * FROM Buys";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            // Datensätze ausgeben
            while ($row = $result->fetch_assoc()) {
                echo "<p>ID: " . $row["trade_id"] . "</p>";
                echo "<p>Name: " . $row["symbol"] . "</p>";
                // Weitere gewünschte Spalten ausgeben
            }
        } else {
            echo "Keine Ergebnisse gefunden.";
        }

        // Datenbankverbindung schließen
        $conn->close();

        // Aktuelles Datum und Uhrzeit ermitteln
        $aktuellesDatum = date('d.m.Y');
        $aktuelleUhrzeit = date('H:i:s');

        // Ausgabe des aktuellen Datum und Uhrzeit
        echo "<p>Datum: $aktuellesDatum</p>";
        echo "<p>Uhrzeit: $aktuelleUhrzeit</p>";
    ?>

    <p>
        Weitere Informationen:
        <a href="info.php">Hier klicken</a>
    </p>
</body>
</html>
