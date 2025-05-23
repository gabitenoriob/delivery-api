from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base # <--- Alteração aqui
import urllib

# --- Configurações para SQL Server ---
DB_SERVER = "CGUAL42872042\\SQLEXPRESS01"
DB_DATABASE = "delivery"
DB_USER = None
DB_PASSWORD = None

ODBC_DRIVER = "ODBC Driver 17 for SQL Server"

if DB_USER:
    params = urllib.parse.quote_plus(
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        # Considere adicionar "TrustServerCertificate=yes;" se estiver em desenvolvimento
        # e encontrar erros de certificado SSL/TLS. Ex:
        # f"TrustServerCertificate=yes;"
    )
else:
    params = urllib.parse.quote_plus(
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        "Trusted_Connection=yes;"
        # Considere adicionar "TrustServerCertificate=yes;" se estiver em desenvolvimento
        # e encontrar erros de certificado SSL/TLS. Ex:
        f"TrustServerCertificate=yes;" # <--- ADICIONEI ISSO TEMPORARIAMENTE, PODE SER NECESSÁRIO
    )

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()