import asyncio
from fastapi import FastAPI, Header, Request, Depends
import aiomysql
import yaml
from fastapi.responses import JSONResponse

app = FastAPI()

# Load database configuration from config.yml
with open("../config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)["database"]


# Dependency to get database connection from the connection pool
async def get_db_conn():
    try:
        pool = await aiomysql.create_pool(**config, autocommit=True)
        async with pool.acquire() as conn:
            yield conn
    except Exception as e:
        print(f"Error creating database connection pool: {e}")
        raise


# Endpoint to log requests to the database (GET request)
@app.get("/logger")
async def log_request(
        request: Request,
        db: aiomysql.connection = Depends(get_db_conn),
):
    try:
        method = request.method
        path = request.url.path
        body = await request.body()
        headers = dict(request.headers)

        async with db.cursor() as cur:
            query = "INSERT INTO request_logs (method, path, body, headers) VALUES (%s, %s, %s, %s)"
            values = (method, path, body.decode("utf-8"), str(headers))
            await cur.execute(query, values)

        return {"message": "Request logged successfully"}
    except Exception as e:
        print(f"Error logging request: {e}")
        return JSONResponse(content={"message": "Internal Server Error"}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
