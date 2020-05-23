import psycopg2
import json

jsonFD = open("/Users/krijojo/Desktop/comuni-italiani-short.json", "r")
jsonObLst = json.load(jsonFD)

listRegioni = list(set(map(lambda jsonOb: jsonOb['Regione'], jsonObLst)))

try:
    connection = psycopg2.connect(
                                  host="127.0.0.1",
                                  port="5432",
                                  database="comuni",
                                  user="postgres")
    print("Connection with DB opened")
    cursor = connection.cursor()

    try:
        for i in range(len(listRegioni)):
            cursor.execute("SELECT name FROM regioni WHERE name = %s", (listRegioni[i],))
            if cursor.rowcount == 0:
                cursor.execute("""INSERT INTO regioni (name) VALUES (%s);""", (listRegioni[i],))
                connection.commit()
                print("Transaction Committed")
            else:
                print("Regione", listRegioni[i], "already in DB")

            cursor.execute("SELECT id FROM regioni WHERE name = %s", (listRegioni[i],))
            regionID = cursor.fetchone()[0]

            # Get all provinces of region X
            listProvince = list(set(map(
                lambda jsonOb: jsonOb['Provincia'],
                list(filter(lambda jsonOb: jsonOb['Regione'] == listRegioni[i], jsonObLst)))))

            for j in range(len(listProvince)):
                cursor.execute("SELECT name FROM province WHERE name = %s AND regione = %s", (listProvince[j], regionID))
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO province (name, regione) VALUES (%s, %s)", (listProvince[j], regionID))
                    connection.commit()
                    print("Transaction Committed")
                else:
                    print("Provincia", listProvince[j], "already in DB")

                cursor.execute("SELECT id FROM province WHERE name = %s AND regione = %s", (listProvince[j], regionID))
                provinceID = cursor.fetchone()[0]
                # Get all comuni of province X
                listComuni = list(map(
                    lambda jsonOb: {'name': jsonOb['Comune'], 'codice': jsonOb['Codice Catastale']},
                    list(filter(lambda jsonOb: jsonOb['Provincia'] == listProvince[j], jsonObLst))))

                for k in range(len(listComuni)):
                    cursor.execute("SELECT name FROM comuni WHERE name = %s AND provincia = %s", (listComuni[k]['name'], provinceID))
                    if cursor.rowcount == 0:
                        cursor.execute("INSERT INTO comuni (name, provincia, codice) VALUES (%s, %s, %s)", (listComuni[k]['name'], provinceID, listComuni[k]['codice']))
                        connection.commit()
                        print("Transaction Committed")
                    else:
                        print("Comune", listComuni[k]['name'], "already in DB")

    except TypeError as error:
        print("Error occurred: ", error)
        connection.rollback()
        print("Transtaction rollback \n")

except (Exception, psycopg2.Error) as error:
    print("Error occurred: ", type(error).__name__)
    print("Error while connecting to PostgreSQL:", error)
finally:
    #closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")