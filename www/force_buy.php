<!DOCTYPE html>
<html>
<head>
    <title>Buy Form</title>
</head>
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
<body>
    <h1>Buy Form</h1>

    <form action="http://172.30.0.2:5001/buy" method="GET">
        <label for="pair">Pair:</label>
        <input type="text" name="Pair" id="pair" required><br>

        <label for="size">Size:</label>
        <input type="number" name="Size" id="size" required><br>

        <input type="submit" value="Buy">
    </form>
</body>
</html>