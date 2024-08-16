import json
from datetime import datetime


def test_number_of_very_old_records():
    num_of1970_records = 0
    with open("taxi_rides.txt", "r") as file:
        for line in file:
            json_object = json.loads(line)
            print(json_object)
            s_time = datetime.fromisoformat(json_object["start_time"])
            if s_time.year <= 1970:
                num_of1970_records += 1
    assert 1 == num_of1970_records

def test_for_null_and_non_null_pax_ids():
    pids = []
    num_trips_with_null_pax_id = 0
    with open("taxi_rides.txt", "r") as file:
        for line in file:
            json_object = json.loads(line)
            pax_id = json_object["pax_id"]
            pids.append(pax_id)
            if pax_id is None:
                num_trips_with_null_pax_id += 1

    assert 1 == num_trips_with_null_pax_id, "one trip has null pax id"
    assert 12 == len(pids), "we have 12 taxi rides in the file"
    pids_set = set(pids)

    assert 4 == len(pids_set), "we have 4 unique pax ids"
    assert "batman" in pids_set
    assert "jerry" in pids_set
    assert "tom" in pids_set
    assert None in pids_set, "one pax id is null"

def test_for_trip_with_negative_amount():
    num_trips_with_negative_fare = 0
    with open("taxi_rides.txt", "r") as file:
        for line in file:
            json_object = json.loads(line)
            fare_amount = json_object["fare_amount"]
            if fare_amount < 0:
                num_trips_with_negative_fare += 1

    assert 1 == num_trips_with_negative_fare, "one trip has negative fare"

def test_for_proper_total_fare():
    # exclude negative amount or dirty records
    total_fare_amount = 0
    with open("taxi_rides.txt", "r") as file:
        for line in file:
            json_object = json.loads(line)
            fare_amount = json_object["fare_amount"]
            pax_id = json_object["pax_id"]
            year = datetime.fromisoformat(json_object["start_time"]).year
            if fare_amount >= 0 and pax_id is not None and year != 1970:
                total_fare_amount += fare_amount

    assert round(total_fare_amount, 2) == round(20.2 + 5.1*7, 2), "2 trips with Jeep each 10.1 and 7 trips with random car models each 5.1"