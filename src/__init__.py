import src.config
from src.dependencies.sqs import SqsPoller
import json

def run():
        sqsPoller = SqsPoller()
        sqsPoller.startPoller()
