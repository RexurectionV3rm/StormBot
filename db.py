import sqlite3

connect = sqlite3.connect("db.db")
cursor = connect.cursor()

def uniform_number(numero):
    if numero[0] != "+":
        numero = f"+{numero}"
    numero = numero.replace(" ", "")
    return(numero)

def initialize_db():
  queries = [
    "CREATE TABLE IF NOT EXISTS voip (numero varchar NOT NULL PRIMARY KEY, string_session varchar(255))"
  ]
  for i in queries:
    cursor.execute(i)

def add(numero, session):
    numero = uniform_number(numero)
    cursor.execute(f"INSERT INTO voip(numero, string_session) VALUES ('{numero}', '{session}')")
    connect.commit()

def remove(numero):
    numero = uniform_number(numero)
    cursor.execute(f"DELETE FROM voip WHERE numero = '{numero}'")
    connect.commit()

def get_session():
    cursor.execute("SELECT string_session FROM voip")
    result = cursor.fetchall()
    session = []
    for i in result:
       session.append(i[0])
    return session
    

def get_number():
    cursor.execute("SELECT numero FROM voip")
    result = cursor.fetchall()
    num = []
    for i in result:
       num.append(i[0])
    return num


def banned_user(session):
    cursor.execute(f"DELETE FROM voip WHERE string_session='{session}'")
    connect.commit()