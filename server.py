import psycopg2
from flask import Flask

app = Flask(__name__)


@app.route('/')
def show_data():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        user="postgres",
        password="heslo",
        host="localhost",
        port="5432",
        database="postgres"
    )

    # Create a cursor to execute SQL queries
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve the first row from your table
    cursor.execute("SELECT * FROM flats")

    # Fetch the first row from the query result
    rows = cursor.fetchall()

    # Construct the HTML response content
    response_content = "<html><body><style>.title { font-weight: bold; width: 200px; } .image { max-width: 220px; margin: 5px; }</style><table>"
    for row in rows:
        title, images = row[1], row[2]
        response_content += "<tr>"
        response_content += f"<td class='title'>{title}</td>"
        response_content += "<td>"
        images = images[2:-2].split('","')
        for image in images:
            response_content += f"<img class='image' src='{image}' />"
        response_content += "</td>"
        response_content += "</tr>"
    response_content += "</table></body></html>"

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return response_content


if __name__ == '__main__':
    # Run the Flask application
    app.run(host='127.0.0.1', port=8080)
