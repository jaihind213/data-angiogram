import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer
import json

# Api to ingest taxi ride data. For demonstration purposes only.
app = FastAPI()

# Kafka configuration
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', 'localhost:9092')
KAFKA_TOPIC = os.environ.get('TAXI_TOPIC', 'taxi_rides')

# Initialize Kafka producer
producer_conf = {
    'bootstrap.servers': KAFKA_BROKER_URL
}
producer = Producer(**producer_conf)

class Payload(BaseModel):
    taxi_id: Optional[str] = None
    pax_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    pickup_zipcode: Optional[str] = None
    dropoff_zipcode: Optional[str] = None
    tax_amount: Optional[float] = None
    fare_amount: Optional[float] = None
    currency: Optional[str] = None
    car_model: Optional[str] = None

def delivery_report(err, msg):
    if err is not None:
        logging.error(f'Message delivery failed: {err}')
    else:
        logging.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

@app.post("/taxis")
async def publish(payload: Payload):
    try:
        logging.info(f'Publishing payload: {payload.dict()}')
        producer.produce(KAFKA_TOPIC, value=json.dumps(payload.dict()), callback=delivery_report)
        producer.flush()
        return {"status": "success", "message": "Payload ingested.", "taxi_id" : payload.dict()["taxi_id"] }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # provide kafka broker url as env variable 'export KAFKA_BROKER_URL=localhost:9092'
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
