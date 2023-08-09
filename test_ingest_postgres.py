import ingest_data_postgres as idp
from timer_decorator import timer
from icecream import ic

@timer
def test_get_secrets():
    secrets = idp.get_username_password()
    ic(secrets)


test_get_secrets()
