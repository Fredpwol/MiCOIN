with open('index.html',mode = 'w') as b :
    b.write(
        """<html>
        <head>
        <title>stuffs</title>
        </head>
        <style>
        div{
            background-color : red;
            border-raduis :20px;
            height : 80px;
            width : 100%;
        }
        </style>
        <body>
        <div>
        <p>"Hello i am fred.....</p>
        </div>
        </body>
        </html>
        """
    )