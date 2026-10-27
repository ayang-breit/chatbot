import core.config as config

USER = config.read_flag('sql_chatbot_user')
PASSWORD = config.read_flag('sql_chatbot_password')
SERVER = 'chendb.cubwcay8e5cp.us-east-1.rds.amazonaws.com,8443'
DATABASE = 'production'
URI = f"mssql+pyodbc://{USER}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"