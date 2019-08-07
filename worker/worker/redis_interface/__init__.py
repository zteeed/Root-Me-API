import redis
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

session = Session()
retry = Retry(
    total=10,
    backoff_factor=1,
    status_forcelist=[429],
)
adapter = HTTPAdapter(max_retries=retry, pool_maxsize=100, pool_block=True)
session.mount('http://', adapter)
session.mount('https://', adapter)

redis_app = redis.Redis(host='localhost', port=6379, db=0)
