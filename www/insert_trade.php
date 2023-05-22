<!DOCTYPE html>
<html>
<head>
    <title>Neuer Eintrag</title>
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

        .headerSortUp:after,
        .headerSortDown:after {
            content: "";
            float: right;
            margin-top: 7px;
            margin-left: 5px;
            border-width: 0 4px 4px;
            border-style: solid;
            border-color: #ffffff transparent;
            visibility: hidden;
        }

        .headerSortUp:after {
            border-bottom-color: #ffffff;
        }

        .headerSortDown:after {
            border-top-color: #ffffff;
        }

        .headerSortUp,
        .headerSortDown {
            padding-right: 20px;
        }

        .headerSortDown:hover:after,
        .headerSortUp:hover:after {
            visibility: visible;
        }
    </style>
</head>
<body>
    <h1>Neuer Eintrag</h1>
    <form method="post" action="insert.php">
        <label for="symbol">Symbol:</label>
        <input type="text" name="symbol" id="symbol" required><br><br>
        
        <label for="price">Preis:</label>
        <input type="number" step="0.001" name="price" id="price" required><br><br>
        
        <label for="qty">Menge:</label>
        <input type="number" step="0.00001" name="qty" id="qty" required><br><br>
        
        <label for="qty">USDT:</label>
        <input type="number" step="0.01" name="usdt" id="usdt" required><br><br>

        <input type="submit" value="Eintrag hinzufügen">
    </form>
</body>
</html>
