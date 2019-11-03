import random
import string

URL = 'https://www.root-me.org'
REDIS_STREAM_USERS = 'update_users'
REDIS_STREAM_CHALLENGES = 'update_challenges'
CG_NAME = 'rootme'
CONSUMER_NAME = ''.join(random.choice(string.ascii_lowercase) for _ in range(25))
