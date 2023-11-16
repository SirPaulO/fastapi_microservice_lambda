import json

import pytest
from dotenv import load_dotenv

import lambda_handler


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture()
def sqs_event():
    f = open("events/internal/aws/sqs-example.json")
    event = json.load(f)
    f.close()
    return event


@pytest.fixture()
def sns_event():
    f = open("events/internal/aws/sns-example.json")
    event = json.load(f)
    f.close()
    return event


@pytest.fixture()
def eventbridge_event():
    f = open("events/internal/aws/eventbridge-example.json")
    event = json.load(f)
    f.close()
    return event


def test_sqs(sqs_event):
    response = lambda_handler.handler(sqs_event, None)
    assert response["statusCode"] == 200, response


def test_sns(sns_event):
    response = lambda_handler.handler(sns_event, None)
    assert response["statusCode"] == 200, response


def test_eventbridge(eventbridge_event):
    response = lambda_handler.handler(eventbridge_event, None)
    assert response["statusCode"] == 200, response
