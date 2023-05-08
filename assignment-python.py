import requests
import csv
import psycopg2

# stahujeme data z URLhaus a získáváme URL
urlhaus_data = requests.get('https://urlhaus.abuse.ch/downloads/csv_recent/').text
url_reader = csv.reader(urlhaus_data.splitlines())
url_list = []
for row in url_reader:
    if len(row) > 2:
        url = row[2]
        url_list.append(url)

# stahujeme data z AlienVault a získáváme IP adresy
alienvault_data = requests.get('http://reputation.alienvault.com/reputation.data').text
ip_list = []
for line in alienvault_data.splitlines():
    if not line.startswith('#'):
        ip = line.split('#')[0].strip()
        ip_list.append(ip)

# stahujeme data z OpenPhish a získáváme URL
openphish_data = requests.get('https://openphish.com/feed.txt').text
openphish_list = openphish_data.splitlines()

# vytisknout seznamy URL a IP adres
print("URL List:", url_list)
print("IP List:", ip_list)

#propojení python kodu a postgreSQL - vloží se údaje z naší databáze
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_user",
    password="your_password"
)

#vytvoření cursoru
cursor = conn.cursor()

#vkládní URL do databáze
for url in url_list:
    cursor.execute("INSERT INTO URLs (URL, source) VALUES (%s, %s)", (url,))

#vkládání IP adres do databáze
for ip in ip_list:
    cursor.execute("INSERT INTO IPs (IP, source) VALUES (%s, %s)", (ip,))

# v SQL jsou vytvořené 2 tabulky, URLs, IPs, každá obsahuje columns Id, source + url/ip

#ukončení propojení
cursor.close()
conn.close()
