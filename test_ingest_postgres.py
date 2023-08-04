import ingest_data_postgres as idp


def test_get_secrets():
    secrets = idp.get_username_password()
    print(secrets)


test_get_secrets()
