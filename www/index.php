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
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.3/js/jquery.tablesorter.min.js"></script>
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
    <script>
        $(document).ready(function() {
            // Tabellen sortierbar machen
            $("#sells").tablesorter({
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
    <script>
        function aktualisiereUhrzeit() {
            var aktuelleZeit = new Date();
            var stunden = aktuelleZeit.getHours();
            var minuten = aktuelleZeit.getMinutes();
            var sekunden = aktuelleZeit.getSeconds();

            // Führende Nullen hinzufügen
            stunden = (stunden < 10 ? "0" : "") + stunden;
            minuten = (minuten < 10 ? "0" : "") + minuten;
            sekunden = (sekunden < 10 ? "0" : "") + sekunden;

            var uhrzeitAnzeige = stunden + ":" + minuten + ":" + sekunden;

            // Uhrzeit in das Element mit der ID "uhrzeit" einfügen
            document.getElementById("uhrzeit").innerHTML = uhrzeitAnzeige;

            // Funktion alle 1 Sekunde aufrufen
            setTimeout(aktualisiereUhrzeit, 1000);
        }
        
        // Function to reload included files every 5 seconds
        function reloadIncludes() {
            $("#includedContent").load("buys.php");
            $("#includedTrades").load("trades.php");
            $("#includedSells").load("sells.php");

        }

        // After the document has loaded, initialize the functions
        $(document).ready(function() {
            aktualisiereUhrzeit();
            setInterval(reloadIncludes, 5000); // Reload included files every 5 seconds
        });
    </script>
</head>
<body>
    <h1>Aktuelles Datum und Uhrzeit</h1>
    <p>Datum: <?php echo date('d.m.Y'); ?></p>
    <p>Uhrzeit: <span id="uhrzeit"></span></p>

    <?php
        include('buys.php');
        include('trades.php');
        include('sells.php');
    ?>

    <p>
        Weitere Informationen:
        <a href="info.php">Hier klicken</a>
    </p>
</body>
</html>
