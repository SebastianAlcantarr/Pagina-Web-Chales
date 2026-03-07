from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import psycopg2.extras

from twilio.rest import Client

# algo de twilio    VT17EPMF5CEBLX4Q7PDAF1ZH


#client = Client("TU_ACCOUNT_SID", "TU_AUTH_TOKEN")

#client.messages.create(
#    from_='whatsapp:+14155238886',
#    to='whatsapp:+521234567890',
#    body=''
#)

def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d6k8imh5pdvs73ae2u40-a.oregon-postgres.render.com",
        port=5432,
        database="bd_chales",
        user="bd_chales_user",
        password="VJ4zwNSn68hbeZsH6gT9HRQgP3QVU7r1"
    )
    return conn

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Dupla(BaseModel):
    nombre_equipo: str
    nombre_jugador_uno:str
    nombre_jugador_dos:str
    num_telefono :int

@app.post("/guardar_dupla", status_code=201)
async def add_dupla(dupla: Dupla):
    if dupla.nombre_jugador_dos.strip().lower() == dupla.nombre_jugador_uno.strip().lower():
        raise HTTPException(status_code=400, detail="Los jugadores deben de ser distintos.")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Duplas (nombre_dupla, jugador_uno, jugador_dos, telefono)
            VALUES (%s, %s, %s, %s)
            """,
            (dupla.nombre_equipo, dupla.nombre_jugador_uno, dupla.nombre_jugador_dos, dupla.num_telefono),
        )
        conn.commit()
        return {"message": "Dupla registrada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)