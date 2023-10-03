import sys
sys.path.append(
    "/Users/itech88/Desktop/Projects/Palmdale/Python/revolution_report_transform/"
)
import ingest_data_postgres as idp
from icecream import icecream as ic, install
install() # this installs ic project wise to other modules




def test_get_secrets():
    secrets = idp.get_username_password()
    ic.ic(secrets)


test_get_secrets()


