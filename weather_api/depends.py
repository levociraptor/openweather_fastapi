from fastapi import Depends, Header


def check_fast_sql_headers(fast_sql_headers: str = Header(None)):
    return fast_sql_headers is not None
