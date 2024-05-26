from trino.dbapi import connect
from trino.auth import BasicAuthentication, JWTAuthentication
import pytz, requests
timezone = pytz.timezone("UTC")
def execute_sql_on_trino(sql, conn):
    # Get a cursor from the connection object
    cur = conn.cursor()
    # Execute sql statement
    cur.execute(sql)
    # Get the results from the cluster
    rows = cur.fetchall()
    # Return the results
    return rows
token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI0MUVRLS11SElzcFlkanhIMU9wbWI5QUVSZ05fdlhfTE1BUGNwdGJPeTJFIn0.eyJleHAiOjE3MTY1NzAzNDIsImlhdCI6MTcxNjU3MDA0MiwiYXV0aF90aW1lIjoxNzE2NTY4MDA2LCJqdGkiOiJiNDdjYzdkNS01YjQ5LTRlMjAtODAwOC0xMDY2M2ExNzM4N2YiLCJpc3MiOiJodHRwczovL2lkbS5kaWdpdGFsLWVuYWJsZXIuZW5nLml0L2F1dGgvcmVhbG1zL21lc2NvYnJhZCIsImF1ZCI6WyJob21lLWFwcCIsImFjY291bnQiXSwic3ViIjoiZWZmMDg1ZWYtNzJlZC00YTUyLTk3YTQtYWRjMTNjNGNjZjY1IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZXhwZXJ0LXN5c3RlbS1hcHAiLCJzZXNzaW9uX3N0YXRlIjoiZmRiMzNlYTUtOWFmYy00YmQ5LWExYTgtOGNkYzk2NWE3MzhiIiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLW1lc2NvYnJhZCIsIk1FUy1Db0JyYUQiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiaG9tZS1hcHAiOnsicm9sZXMiOlsiTUVTLUNvQnJhRCJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInNpZCI6ImZkYjMzZWE1LTlhZmMtNGJkOS1hMWE4LThjZGM5NjVhNzM4YiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiRXZhbmdlbG9zIEtvbGFpdGlzIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZWtvbGFpdGlzQGV2b2x1dGlvbnByb2plY3RzLmdyIiwiZ2l2ZW5fbmFtZSI6IkV2YW5nZWxvcyIsImZhbWlseV9uYW1lIjoiS29sYWl0aXMiLCJlbWFpbCI6ImVrb2xhaXRpc0Bldm9sdXRpb25wcm9qZWN0cy5nciJ9.dPT5xFeUYMCd6xHCXUqpQfDQD7oegdraiaKfIOeZyoCiXBFT_T8bys1Cgbn43owu4zQ4LVxhrT_wwSMHLb5Eoq7-FQxmURNvdQfJcDZ2eStshPi_JM5we-dmMN86FkFHN6wHBlyBKPNiXph6Dvo8Ja9ryXUNoJZc76RJk-w55fUir1Dkwl73yIpBZA97HjVm6hfDk3BZt6xa02_GBslGR1me5J7GepBe-0cAh_e5jtxM8JpfVwIxzDwjGRW7b7b4zV6PO6mpUK384CEx4psaVpyHRRaclfDqRiyJTPrKb7i_XVMZ_xCPokRl1x2PVSx8BxgEG_cFAi0xSoWzVjbQHw"
conn = connect(
    host="trino.mescobrad.digital-enabler.eng.it",
    port=443,
    http_scheme="https",
    auth=JWTAuthentication(token),
    timezone=str(timezone),
    # verify=False,
)
print(execute_sql_on_trino(sql="SHOW CATALOGS", conn=conn))