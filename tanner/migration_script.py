import asyncio
import json
import aioredis
import psycopg2
from tanner import redis_client, postgres_client, dbutils


async def main():
    r_client = await redis_client.RedisClient.get_redis_client()
    pg_client = await postgres_client.PostgresClient().get_pg_client()
    await dbutils.DBUtils.create_data_tables(pg_client)

    try:
        print("[INFO] Reading from Redis")
        keys = await r_client.keys("[0-9a-f]*")
    except (aioredis.ProtocolError, TypeError, ValueError) as error:
        logger.exception("Can't get session for analyze: %s", error)
    else:
        print("[INFO] Moving to Postgres")
        error = 0
        for key in keys:
            try:
                session = await r_client.zrange(key, encoding="utf-8")
                result = json.loads(session[0])

                if result["location"] == "NA":
                    result["location"] = dict(
                        country=None, country_code=None, city=None, zip_code=0,
                    )

                try:
                    await dbutils.DBUtils.add_analyzed_data(result, pg_client)
                    await r_client.delete(*[key])
                except psycopg2.ProgrammingError as pg_error:
                    print(
                        "Error with Postgres: %s. Session with session-id %s will not be added to postgres",
                        pg_error,
                        key,
                    )
                except aioredis.ProtocolError as redis_error:
                    print(
                        "Error with redis: %s. Session with session-id %s will not be removed from redis.",
                        redis_error,
                        key,
                    )
            except aioredis.errors.ReplyError:
                error += 1
                continue

    pg_client.close()
    await pg_client.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
