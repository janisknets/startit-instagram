import os
import psycopg2
import csv
import time


# Iegūstam DB informāciju no vides mainīgajiem
# lai nebūtu jāglabā parole publiski pieejama
ELEPHANT_HOST = "balarama.db.elephantsql.com" #os.getenv("ELEPHANT_HOST")
ELEPHANT_NAME = "shenbpsi" #os.getenv("ELEPHANT_NAME")
ELEPHANT_PASSWORD = "8kWplGUh9Mz3oRLbb5PJvmeLJ3EFz6AF"#os.getenv("ELEPHANT_PASSWORD")
print(ELEPHANT_HOST, ELEPHANT_NAME, ELEPHANT_PASSWORD)

# Pieslēgums datubāzei izveidots un pieejams globāli
dsn = "host={} dbname={} user={} password={}".format(ELEPHANT_HOST, ELEPHANT_NAME, ELEPHANT_NAME, ELEPHANT_PASSWORD)


def parbauda_db_savienojumu():
    """Pārbauda pieslēgumu datubāzei
    
    Returns:
        string -- tekstu ar datubāzes versiju
    """
    # saformatē pieslēgšanās parametrus
    dsn = "host={} dbname={} user={} password={}".format(ELEPHANT_HOST, ELEPHANT_NAME, ELEPHANT_NAME, ELEPHANT_PASSWORD)
    # izveido pieslēgumu
    conn = psycopg2.connect(dsn)
    # izveido kursoru
    cur = conn.cursor()
    # aizsūta kursoram SQL vaicājumu
    cur.execute("SELECT version();")
    # pieprasa no kursora atbildi
    record = cur.fetchone()
    result = "You are connected to - " + str(record)
    # aizver kursoru
    cur.close()
    # aizver peislēgumu daubāzei
    conn.close()
    return result


def veido_vd_tabulu():
    """ 
    Izveido vārdadienu tabulu ar indeksiem uz visām kolonnām meklēšanai
    """
    conn = psycopg2.connect(dsn)
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS vardadienas;""")
    c.execute("""CREATE TABLE vardadienas
                (vards TEXT COLLATE "lv-x-icu" PRIMARY KEY, diena INT NOT NULL, menesis INT NOT NULL);""")
    c.execute("""CREATE INDEX d1 ON vardadienas(diena);""")
    c.execute("""CREATE INDEX m1 ON vardadienas(menesis);""")
    c.close()
    conn.commit()
    conn.close()
    return "OK"


def piepilda_vd_tabulu(datne):
    conn = psycopg2.connect(dsn)
    c = conn.cursor()
    sql = "INSERT INTO vardadienas VALUES(%s, %s, %s)"
    
    vardu_dati = []

    with open(datne, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        for line in reader:
            vardu_dati.append(line)
    
    c.executemany(sql, vardu_dati)
    skaits = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return skaits


def vaicajuma_parbaude(sql):
    try:
        conn = psycopg2.connect(dsn)
        c = conn.cursor()
        c.execute(sql)
        print(sql)
        c.close()
        conn.commit()
        return c.rowcount
    except:
        return False


print(parbauda_db_savienojumu())

print("Izveido tabulu")
print(veido_vd_tabulu())

t1 = time.perf_counter()
print("Piepilda tabulu")
print(piepilda_vd_tabulu("dati/vardadienas.txt"))
t2 = time.perf_counter()
print(f"Datu importēšana aizņēma {t2 - t1:0.4f} sekundes")

print("Ierakstu skaits tabulā:")
print(vaicajuma_parbaude("SELECT vards FROM vardadienas;"))