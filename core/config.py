import logging
import os
import configparser
from cryptography.fernet import Fernet
ENCRYPTION_KEY = b'pMTmYai-1UfQBuxLlx5XdNt5-ciu1pm2IQYRjfAP7As='

CONFIG_FILE = r'/home/ec2-user/config.ini'

def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def write_config(config):
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def read_flag(key, section='API_KEYS'):
    return read_config()[section][key]

def read_encrypted_flag(key, section='API_KEYS'):
    return decrypt(read_flag(key, section=section))

def write_flag(key, value, section='API_KEYS'):
    config = read_config()
    if section not in config: config[section] = {}
    config[section][key] = value
    write_config(config)

def write_encrypted_flag(key, value, section='API_KEYS'):
    write_flag(key, encrypt(value), section=section)

def encrypt(value):
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(value.encode()).decode()

def decrypt(value):
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(value.encode()).decode()

def raw_encrypt(value):
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(value)

def raw_decrypt(value):
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(value)