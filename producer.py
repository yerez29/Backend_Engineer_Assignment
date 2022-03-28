from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json
from kafka import KafkaProducer
from utility_helper import TOPIC_NAME


class Item(BaseModel):
    car_id: str
    sensor_id: str
    distance: int
    timestamp: int


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:63342"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serializer(message):
    return json.dumps(message).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)


@app.post("/")
async def root(item: Item):
    message = {
        'car_id': item.car_id,
        'sensor_id': item.sensor_id,
        'distance': item.distance,
        'timestamp': item.timestamp
    }
    partition = int(message.get('sensor_id')[-1]) - 1
    producer.send(TOPIC_NAME, message, partition=partition)
    return message


if __name__ == '__main__':

    uvicorn.run(app, host="127.0.0.1", port=8000)