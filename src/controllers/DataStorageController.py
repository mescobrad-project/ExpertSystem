from trino.dbapi import Connection
from src.clients.trino import client


class BaseController:
    def __init__(self, client: Connection):
        self.client = client

    def __exec(self, sql: str, params: any = None):
        cur = self.client.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        return rows

    def list_catalogs(self):
        return {"data": self.__exec("SHOW CATALOGS")}

    def list_catalog_schemas(self, catalog: str):
        return {"catalog": catalog, "data": self.__exec(f"SHOW SCHEMAS in {catalog}")}

    def list_catalog_tables(self, catalog: str, schema: str):
        return {
            "catalog": catalog,
            "schema": schema,
            "data": self.__exec(f"SHOW TABLES FROM {catalog}.{schema}"),
        }

    def describe_catalog_tables(self, catalog: str, schema: str, table: str):
        return {
            "catalog": catalog,
            "schema": schema,
            "table": table,
            "data": self.__exec(f"DESCRIBE {catalog}.{schema}.{table}"),
        }

    def list_catalog_table_sources(self, catalog: str, schema: str, table: str):
        data = []

        try:
            data = self.__exec(
                f"SELECT DISTINCT source FROM {catalog}.{schema}.{table}"
            )
        except:
            data = []

        return {
            "catalog": catalog,
            "schema": schema,
            "table": table,
            "data": data,
        }


DataStorageController = BaseController(client)
