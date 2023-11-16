from main import app
from mangum import Mangum
from mangum_extra_handlers import EventBridgeHandler, SNSHandler, SQSHandler

handler = Mangum(app, lifespan="off", custom_handlers=[SNSHandler, SQSHandler, EventBridgeHandler])
