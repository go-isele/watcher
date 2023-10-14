import aiomysql
import yaml

# Load database configuration from config.yml
with open("../config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)["database"]


async def log_request_to_db(method, path, body, headers):
    try:
        pool = await aiomysql.create_pool(**config, autocommit=True)
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = "INSERT INTO request_logs (method, path, body, headers) VALUES (%s, %s, %s, %s)"
                values = (method, path, body.decode("utf-8"), str(headers))
                await cur.execute(query, values)
    except Exception as e:
        print(f"Error logging request: {e}")
