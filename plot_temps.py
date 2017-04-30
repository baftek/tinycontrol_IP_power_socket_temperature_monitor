# -*- coding: utf-8 -*-
from matplotlib import use
use('Agg')
import matplotlib.pyplot as plt
import mysql.connector

conn = mysql.connector.connect(host='kamionka.cf', port='3306', user='tempinserter',
                               password='Re1eJIXita8AlotAG5LukOFu5uMoJe', database='temps', autocommit=True)
sqlcursor = conn.cursor()
sqlcursor.execute('select t.timestamp, t.temp, term.name, term.color from Temperatures t join Termometers term '
                  'USING (term_id) WHERE t.timestamp > date_sub(now(), INTERVAL 9 HOUR)')
data = sqlcursor.fetchall()
sqlcursor.execute('select term_id, name, url, color from Termometers')
locations = sqlcursor.fetchall()
fig = plt.figure(figsize=(10, 4), facecolor='white')
fig.patch.set_alpha(0.0)
ax = fig.add_subplot(111)

for l in locations:
    if l[2]:
        x = [i[0] for i in data if i[2] == l[1]]
        y = [i[1] for i in data if i[2] == l[1]]
        ax.plot(x, y, '-', color=l[3], label=l[1]+' '+str(y[-1])+u'°C')

plt.title(u'Temperatury z listw zarządzalnych')
plt.xlabel('Czas')
plt.ylabel(u'Temp °C')
plt.ylim(-1, 35)
plt.grid(which='both', alpha=0.4)
plt.legend(loc='lower left')
from matplotlib.dates import DateFormatter, HourLocator, MinuteLocator
ax.xaxis.set_major_locator(HourLocator())
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(MinuteLocator(byminute=(30, )))
plt.savefig('/www/tempKato.png')
plt.close()
