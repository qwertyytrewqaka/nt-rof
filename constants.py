import telegram
import os

token = '1919459086:AAHV3bLxPUOiJwdfB3rqh365LLcCSYrwqZc'
chat_id = "-1001584449609"
bot = telegram.Bot(token=token)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
history = ["", "", "", "", "", ""]
server_state = 0
errorcount = 0
latest_number = 0
k_number = 0
