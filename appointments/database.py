import sqlite3

ddl = {
	'clients':
		'''CREATE TABLE IF NOT EXISTS 'clients'(
		id INTEGER PRIMARY KEY,
		first_name TEXT NOT NULL,
		last_name TEXT NOT NULL,
		age INTEGER NOT NULL ,
		tel VARCHAR(12) NOT NULL UNIQUE
		);'''
	,
	'appointments':
		'''CREATE TABLE IF NOT EXISTS 'appointments'(
		id INTEGER PRIMARY KEY,
		time_from DATE DEFAULT (datetime('now','localtime')),
		time_to DATE DEFAULT (datetime('now','localtime')),
		client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE ON UPDATE NO ACTION 
		);'''
}

fake_data = {
	'clients': [
		'INSERT INTO clients VALUES(null, "Krisjanis", "Ivbulis", 99, "+37126616463")',
		'INSERT INTO clients VALUES(null, "Inokentijs", "Marpls", 18, "+37126316463")',
		'INSERT INTO clients VALUES(null, "Ainars", "Slesers", 55, "+37126614463")',
	],
	'appointments': [
		'INSERT INTO appointments VALUES(null, null, null, 1)'
	]
}

conn = sqlite3.connect('./database/appointments.dat')

def drop_and_create_db():
	c = conn.cursor()
	c.execute('DROP TABLE IF EXISTS appointments')
	c.execute('DROP TABLE IF EXISTS clients')
	c.execute(ddl['clients'])
	c.execute(ddl['appointments'])
	c.close()

def insert_db_data():
	c = conn.cursor()
	for insert in fake_data['clients']:
		c.execute(insert)
	for insert in fake_data['appointments']:
		c.execute(insert)
	c.close()

def get_appointments():
	c = conn.cursor()
	c.execute(
		'''SELECT 
			appointments.time_from,
		    appointments.time_to,
		    clients.first_name,
		    clients.last_name,
		    clients.age,
		    clients.tel
		FROM appointments 
		LEFT OUTER JOIN clients	ON appointments.id=clients.id'''
	)
	appointments = c.fetchall()
	c.close()
	return appointments

# def insert_appointment():
# 	c = conn.cursor()
# 	c.execute('INSERT INTO clients VALUES (null, :first_name, :last_name, :age, :tel)',
# 	          {'first_name': first_name,
# 	           'last_name': last_name,
# 	           'age': age,
# 	           'tel': telephone_number
# 	           })
# 	c.close(
#

def insert_client(first_name,last_name,age,telephone_number):
	c = conn.cursor()
	c.execute('INSERT INTO clients VALUES (null, :first_name, :last_name, :age, :tel)',
	          {'first_name': first_name,
	           'last_name': last_name,
	           'age': age,
	           'tel': telephone_number
	           })
	c.close()

def delete_clients(client_ids):
	c = conn.cursor()
	for client_id in client_ids:
		statement = f'DELETE FROM clients WHERE id = {client_id}'
		c.execute(statement)
	c.close()

def get_client_combobox():
	c = conn.cursor()
	c.execute('SELECT first_name, last_name FROM clients')
	combo_client = c.fetchall()
	c.close()


def get_client(client_id):
	c = conn.cursor()
	c.execute(f'SELECT * FROM clients WHERE id ={client_id}')
	client = c.fetchone()
	c.close()
	return client

def alter_client(id, first_name,last_name,age,tel):
	c = conn.cursor()
	c.execute('UPDATE clients SET first_name=:first_name,last_name=:last_name,age=:age,tel=:tel WHERE id=:id',
	          {'first_name': first_name,
	           'last_name': last_name,
	           'age': age,
	           'tel': tel,
	           'id': id
	           })
	# c.execute(f'UPDATE clients SET first_name={first_name},last_name={last_name},age={age},telephone_number={telephone_number} WHERE id={id}')
	c.close()
