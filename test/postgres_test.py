import sys

sys.path.append(
    "Users/itech88/Desktop/Projects/Palmdale/Python/revolution_report_transform/"
)
import ingest_data_postgres as idp


def test_get_secrets():
    secrets = idp.get_username_password()
    print(secrets)


test_get_secrets()
