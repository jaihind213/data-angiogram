import json
import os
import random
from datetime import datetime, timedelta

def generate_old_datetime():
    return datetime(1970, 1, 1).isoformat()

def generate_payloads():
    num_random = 10
    passenger_ids = ['tom', 'batman']
    car_models = ['Toyota', 'Benz', 'Ford']
    zipcodes = ['10001', '10002', '10003']

    payloads = []
    current_time = datetime.now()
    for _ in range(num_random - 3):
        start_time = current_time
        end_time = start_time + timedelta(minutes=random.randint(1, 60))
        fare_amount = round(random.uniform(2.5, 7.5), 2)

        payload = {
            "taxi_id": f"taxi_{random.randint(1, 100)}",
            "pax_id": random.choice(passenger_ids[:3]),  # Exclude None for most cases
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "pickup_zipcode": random.choice(zipcodes),
            "dropoff_zipcode": random.choice(zipcodes),
            "tax_amount": round(fare_amount * 0.1, 2),  # Assuming tax amount is 10% of fare
            "fare_amount": fare_amount,
            "currency": 'USD',
            "car_model": random.choice(car_models)
        }
        payloads.append(payload)

    # Add specific cases. for -ive fare,null pax, 1970 trip - with jeep car model
    payloads.append({
        "taxi_id": f"taxi_jeep_1",
        "pax_id": "jerry",
        "start_time": (datetime.now() + timedelta(minutes=random.randint(1, 3))).isoformat(),
        "end_time": (datetime.now() + timedelta(minutes=random.randint(4, 6))).isoformat(),
        "pickup_zipcode": "10004",
        "dropoff_zipcode": random.choice(zipcodes),
        "tax_amount": 0.1,
        "fare_amount": 10.1,
        "currency": 'USD',
        "car_model": 'Jeep'
    })
    payloads.append({
        "taxi_id": f"taxi_jeep_2",
        "pax_id": "jerry",
        "start_time": (datetime.now() + timedelta(minutes=random.randint(7, 8))).isoformat(),
        "end_time": (datetime.now() + timedelta(minutes=random.randint(9, 10))).isoformat(),
        "pickup_zipcode": "10004",
        "dropoff_zipcode": random.choice(zipcodes),
        "tax_amount": 0.1,
        "fare_amount": 10.1,
        "currency": 'USD',
        "car_model": 'Jeep'
    })

    # very old data
    payloads.append({
        "taxi_id": f"taxi_jeep_3",
        "pax_id": random.choice(passenger_ids[:3]),  # Random valid passenger ID
        "start_time": generate_old_datetime(),
        "end_time": (datetime(1970, 1, 1) + timedelta(minutes=30)).isoformat(),
        "pickup_zipcode": "10004",
        "dropoff_zipcode": random.choice(zipcodes),
        "tax_amount": 0.1,
        "fare_amount": 10.1,
        "currency": 'USD',
        "car_model": 'Jeep'
    })

    # pax id is null
    payloads.append({
        "taxi_id": f"taxi_jeep_4",
        "pax_id": None,  # Passenger ID is null
        "start_time": current_time.isoformat(),
        "end_time": (current_time + timedelta(minutes=30)).isoformat(),
        "pickup_zipcode": "10004",
        "dropoff_zipcode": random.choice(zipcodes),
        "tax_amount": 0.1,
        "fare_amount": 10.1,
        "currency": 'USD',
        "car_model": 'Jeep'
    })

    # negative payload
    payloads.append({
        "taxi_id": f"taxi_Jeep5",
        "pax_id": random.choice(passenger_ids[:3]),  # Random valid passenger ID
        "start_time": current_time.isoformat(),
        "end_time": (current_time + timedelta(minutes=30)).isoformat(),
        "pickup_zipcode": "10004",
        "dropoff_zipcode": random.choice(zipcodes),
        "tax_amount": -0.5,  # Negative tax amount
        "fare_amount": -5.0,
        "currency": 'USD',
        "car_model": 'Jeep'
    })

    return payloads


if __name__ == "__main__":
    payloads = generate_payloads()
    os.remove("taxi_rides.txt")
    with open('taxi_rides.txt', 'w') as file:
        for payload in payloads:
            print(payload)
            file.write(json.dumps(payload) + '\n')
