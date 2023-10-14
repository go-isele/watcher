import uvicorn
from fastapi import FastAPI, Request, HTTPException
from request_logger import log_request_to_db
from server_health import get_system_metrics

app = FastAPI()


# Endpoint to log requests to the database (GET request)
@app.get("/logger")
async def log_request_handler(
        request: Request
):
    try:
        method = request.method
        path = request.url.path
        body = await request.body()
        headers = dict(request.headers)

        # Log request to database
        await log_request_to_db(method, path, body, headers)

        return {"message": "Request logged successfully"}
    except Exception as e:
        print(f"Error logging request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Endpoint to get server metrics and statistics
@app.get("/metrics")
async def get_metrics_handler():
    try:
        # Collect server metrics
        metrics = get_system_metrics()

        return metrics
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4040)
