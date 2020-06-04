from cryptography.fernet import Fernet
import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import getpass

import sqlite3

kdf = lambda salt : PBKDF2HMAC(
    algorithm = hashes.SHA256(),
    length = 32,
    salt = salt,
    iterations = 100000,
    backend = default_backend()
)

def create_db(name, master_password, SALT_SIZE):
    conn = sqlite3.connect(name)
    c = conn.cursor()

    salt = os.urandom(SALT_SIZE)

    c.execute('DROP TABLE IF EXISTS db_data')
    c.execute('CREATE TABLE db_data (salt BLOB, password BLOB)')

    f = Fernet(base64.urlsafe_b64encode(kdf(salt).derive(master_password)))

    c.execute('INSERT INTO db_data VALUES (?, ?)', [salt, f.encrypt(master_password)])
    c.execute('DROP TABLE IF EXISTS passwords')
    c.execute('CREATE TABLE passwords (service TEXT, username BLOB, password BLOB, comments BLOB)')

    conn.commit()
    conn.close()

def check_password(filename, password):
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute('SELECT * FROM db_data')
    data = c.fetchall()[0]
    f = Fernet(base64.urlsafe_b64encode(kdf(data[0]).derive(password)))

    try:
        f.decrypt(data[1])
    except:
        print("Invalid password.")
        return 0
    return 1

def add_password(filename, master_password, service, username, password, info=''):
    if service in list_of_services(filename,master_password):
        print('Service has already a password')
        return 0
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute('SELECT * FROM db_data')
    data = c.fetchall()[0]
    f = Fernet(base64.urlsafe_b64encode(kdf(data[0]).derive(master_password)))

    try:
        f.decrypt(data[1])
    except:
        print("Invalid password.")
        return 0

    c.execute('INSERT INTO passwords VALUES (?, ?, ?, ?)',[service, f.encrypt(username.encode('utf-8')),
                                                                    f.encrypt(password.encode('utf-8')),
                                                                    f.encrypt(info.encode('utf-8'))])

    conn.commit()
    conn.close()
    return 1

def edit_password(filename, master_password, service, username, password, info=''):
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute('SELECT * FROM db_data')
    data = c.fetchall()[0]
    f = Fernet(base64.urlsafe_b64encode(kdf(data[0]).derive(master_password)))

    try:
        f.decrypt(data[1])
    except:
        print("Invalid password.")
        return 0

    c.execute('DELETE FROM passwords WHERE service=(?)', [service])
    conn.commit()

    c.execute('INSERT INTO passwords VALUES (?, ?, ?, ?)',[service, f.encrypt(username.encode('utf-8')),
                                                                    f.encrypt(password.encode('utf-8')),
                                                                    f.encrypt(info.encode('utf-8'))])

    conn.commit()
    conn.close()

def remove_password(filename, master_password, service):
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute('SELECT * FROM db_data')
    data = c.fetchall()[0]

    f = Fernet(base64.urlsafe_b64encode(kdf(data[0]).derive(master_password)))

    try:
        f.decrypt(data[1])
    except:
        print("Invalid password.")
        return 0

    c.execute('DELETE FROM passwords WHERE service=(?)', [service])

    conn.commit()
    conn.close()
    return 1

def list_of_services(filename, master_password):
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute('SELECT * FROM db_data')
    data = c.fetchall()[0]
    f = Fernet(base64.urlsafe_b64encode(kdf(data[0]).derive(master_password)))

    try:
        f.decrypt(data[1])
    except:
        print("Invalid password.")
        return [0]

    c.execute('SELECT service FROM passwords')
    list = c.fetchall()

    conn.close()
    return [a[0] for a in list]

def retrieve_password(filename, master_password, service):
    if service not in list_of_services(filename,master_password):
        print('Service was not found')
        return [0]

    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute('SELECT * FROM db_data')
    data = c.fetchall()[0]
    f = Fernet(base64.urlsafe_b64encode(kdf(data[0]).derive(master_password)))

    try:
        f.decrypt(data[1])
    except:
        print("Invalid password.")
        return [0]

    c.execute('SELECT * FROM passwords WHERE service=(?)',[service])
    data2 = c.fetchall()[0]
    conn.close()
    return [data2[0]] + [f.decrypt(d).decode('utf-8') for d in data2[1:]]
