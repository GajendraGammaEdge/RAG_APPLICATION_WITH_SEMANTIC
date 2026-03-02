from fastapi import FastAPI
from db_configuration.pgdb_config import get_db, Base, engine
from router.chat_router import router as chatrouter
from router.document_router import router as documentrouter
from router.search_router import router as searchrouter
from router.userrouter import router as userorotuer
from router.otp_router import router as otprouter
from sqlalchemy import text
import os 
from dotenv import load_dotenv
load_dotenv()

# import debugpy
# debugpy.listen(("0.0.0.0", 5680))  
# print("Waiting for debugger to attach...")
# debugpy.wait_for_client() 

db_name = os.getenv("POSTGRES_DB")


app = FastAPI(title="GAMMA RAG API")

# Include routers
app.include_router(otprouter, tags=["ForgotPassword"])
app.include_router(chatrouter, tags=["Chat"])
app.include_router(documentrouter, tags=["Document"])
app.include_router(searchrouter, tags=["Search"])
app.include_router(userorotuer)


# Create the vector extension on startup
with engine.connect() as connection:
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    # connection.execute(text("ALTER DATABASE {db_name} REFRESH COLLATION VERSION;"))
    connection.commit()
    print("Extension of the pgvector is completed") 

Base.metadata.create_all(bind=engine)

@app.post("/healthcheck")
async def health():
    return {
        "message": "GAMMA RAG is working fine ]"
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


#this is the  debugging  command 
# uvicorn main:app --reload --host 127.0.0.1 --port 8000 --log-level debug