from main import app
from mangum import Mangum
from mangum_extra_handlers import EventBridgeHandler, SNSHandler, SQSHandler
from settings.project_settings import project_settings

handler = Mangum(
    app,
    api_gateway_base_path=project_settings.RootPath,
    lifespan="off",
    custom_handlers=[SNSHandler, SQSHandler, EventBridgeHandler],
)
