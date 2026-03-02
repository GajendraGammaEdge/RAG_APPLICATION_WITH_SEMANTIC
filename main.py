from fastapi import FastAPI
from db_configuration.pgdb_config import get_db, Base, engine
from router.chat_router import router as chatrouter
from router.document_router import router as documentrouter
from router.search_router import router as searchrouter
from router.userrouter import router as userorotuer
from router.otp_router import router as otprouter
from router.subscription_router import router as subscriptionrouter
from router.subscription_transaction_router import router as   subscritpiontransactionrouter
from router.conversation_router import router as coverstationrouter
from sqlalchemy import text
from pathlib import Path
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
app.include_router(subscriptionrouter)
app.include_router(subscritpiontransactionrouter)
app.include_router(coverstationrouter)

# Execute SQL initialization on startup using init.sql file
init_sql_path = Path(__file__).parent / "db_configuration" / "init.sql"
with engine.connect() as connection:
    # Read and execute init.sql file
    if init_sql_path.exists():
        init_sql = init_sql_path.read_text()
        if init_sql:
            connection.execute(text(init_sql))
            print("Init SQL executed: vector extension created")
    else:
        print(f"Warning: init.sql not found at {init_sql_path}")
    
    connection.commit()
    print("Database initialization completed")

# Base.metadata.create_all(bind=engine)  # Removed - Let Alembic handle schema

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
