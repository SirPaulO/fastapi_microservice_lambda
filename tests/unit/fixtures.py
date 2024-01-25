import json

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture()
def sqs_event():
    f = open("tests/events/internal/aws/sqs-example.json")
    event = json.load(f)
    f.close()
    return event


@pytest.fixture()
def sns_event():
    f = open("tests/events/internal/aws/sns-example.json")
    event = json.load(f)
    f.close()
    return event


@pytest.fixture()
def eventbridge_event():
    f = open("tests/events/internal/aws/eventbridge-example.json")
    event = json.load(f)
    f.close()
    return event
