from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib # Necessário para formatar a string de conexão corretamente

# --- Configurações para SQL Server ---
DB_SERVER = "CGUAL42872042\SQLEXPRESS01"  
DB_DATABASE = "delivery" 
DB_USER = None # Deixe como None se usar Autenticação do Windows
DB_PASSWORD = None # Deixe como None se usar Autenticação do Windows


# Driver ODBC 
ODBC_DRIVER = "ODBC Driver 17 for SQL Server" # Pode variar, verifique os drivers instalados!

# Construção da DATABASE_URL para SQL Server com pyodbc
if DB_USER: # Autenticação SQL Server
    params = urllib.parse.quote_plus(
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
     
    )
else: # Autenticação Windows
    params = urllib.parse.quote_plus(
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        "Trusted_Connection=yes;" # Essencial para Autenticação do Windows
        # "TrustServerCertificate=yes;" # Adicione se necessário
    )

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Crie a engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crie uma fábrica de sessões (SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para seus modelos ORM
Base = declarative_base()
Session = sessionmaker()

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()