import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    dbname="PhoneBook",
    user="postgres",
    password="12345678910",
    port=5432
)

cur = conn.cursor()

with open(r"C:\Users\user\Desktop\lab1\lab10\task1\data.csv", 'r') as f:
    next(f) 
    cur.copy_from(f, 'contacts', sep=',', columns=('first_name', 'second_name', 'phone'))

conn.commit()
conn.close()