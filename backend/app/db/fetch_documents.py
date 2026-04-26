import mysql.connector


def fetch_documents():
    """
    Fetch documents from MySQL database.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sss080816##",
        database="search_engine_db"
    )

    cursor = connection.cursor()

    cursor.execute("SELECT id, content FROM documents")
    rows = cursor.fetchall()

    documents = []
    for row in rows:
        documents.append({
            "id": row[0],
            "text": row[1]
        })

    cursor.close()
    connection.close()

    return documents