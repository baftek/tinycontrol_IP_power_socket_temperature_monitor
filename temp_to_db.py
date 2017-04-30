import mysql.connector
import requests
import datetime as dt

temp_name = 'Katowice'

conn = mysql.connector.connect(host='kamionka.cf', port='3306', user='tempinserter',
                                   password='Re1eJIXita8AlotAG5LukOFu5uMoJe', database='temps', autocommit=True)
sqlcursor = conn.cursor()
sqlcursor.execute('select term_id, name, url, term_key from Termometers')
locations = sqlcursor.fetchall()

for l in locations:
    # term_id = [l[0] for l in locations if l[1] == temp_name][0]
    # url = [l[2] for l in locations if l[1] == temp_name][0]
    # key = [l[3] for l in locations if l[1] == temp_name][0]
    print(l)
    term_id = l[0]
    name = l[1]
    url = l[2]
    key = l[3]
    print(term_id, url, key)

    if url and 'st0' in url and key:
        try:
            response = requests.get(url, auth=('admin', 'admin'))
            page = response.text.strip().split('>')
            # print(page, len(page))
            temp = [l for l in page if '/'+key in l][0]
            temp = float(temp[:temp.find('<')])
            print('temp', temp)
        except:
            continue # either url is not working or xml file is wrong
        try:
            sqlcursor.execute(r"insert ignore into Temperatures (timestamp, term_id, temp) VALUES ('{}', {}, {})".format(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), term_id, temp))
        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.DatabaseError):
            while not conn.is_connected():
                print('Connection to DB lost, reconnecting...')
                try:
                    conn.reconnect(attempts=20, delay=5)
                except:
                    continue

    else:
        print("omitting", name)
conn.close()