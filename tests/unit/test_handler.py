import lambda_handler


def test_sqs(sqs_event):
    response = lambda_handler.handler(sqs_event, None)
    assert response["statusCode"] == 200, response


def test_sns(sns_event):
    response = lambda_handler.handler(sns_event, None)
    assert response["statusCode"] == 200, response


def test_eventbridge(eventbridge_event):
    response = lambda_handler.handler(eventbridge_event, None)
    assert response["statusCode"] == 200, response
