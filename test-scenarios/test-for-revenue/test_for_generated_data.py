import json
from datetime import datetime


def test_number_of_very_old_records():
    num_of1970_records = 0
    with open("taxi_rides.txt", "r") as file:
        for line in file:
            json_object = json.loads(line)
            s_time = datetime.fromisoformat(json_object["start_time"])
            if s_time.year <= 1970:
                num_of1970_records += 1
                assert "Jeep" == json_object["car_model"], "car model is Jeep for the trip with 1970 trip"
    assert 1 == num_of1970_records

def test_for_null_and_non_null_pax_ids():
    pax_ids = []
    num_trips_with_null_pax_id = 0
    with open("taxi_rides.txt", "r") as file:
        for line in file:
            json_object = json.loads(line)
            pax_id = json_object["pax_id"]
            pax_ids.append(pax_id)
            if pax_id is None:
                num_trips_with_null_pax_id += 1
                assert "Jeep" == json_object["car_model"], "car model is Jeep for the trip with null pax id"

    assert 1 == num_trips_with_null_pax_id, "one trip has null pax id"
    assert 12 == len(pax_ids), "we have 12 taxi rides in the file"
    pax_id_set = set(pax_ids)

    assert 4 == len(pax_id_set), "we have 4 unique pax ids"
    assert "batman" in pax_id_set
    assert "jerry" in pax_id_set
    assert "tom" in pax_id_set
    assert None in pax_id_set, "one pax id is null"

def test_for_trip_with_negative_amount():
    num_trips_with_negative_fare = 0
    with open("taxi_rides.txt", "r") as file:
        for line in file:
            json_object = json.loads(line)
            fare_amount = json_object["fare_amount"]
            if fare_amount < 0:
                num_trips_with_negative_fare += 1
                assert "Jeep" == json_object["car_model"], "car model is Jeep has the trip with -ive fare"

    assert 1 == num_trips_with_negative_fare, "one trip has negative fare"

def test_for_zipcode_for_jeep_trips():
    num_trips_with_10004_zipcode = 0
    with open("taxi_rides.txt", "r") as file:
        for line in file:
            json_object = json.loads(line)
            car_model = json_object["car_model"]
            if car_model != 'Jeep':
                continue
            assert "10004" == json_object["pickup_zipcode"], "Jeep trips are in 10004 zipcode"
            num_trips_with_10004_zipcode += 1

    assert 5 == num_trips_with_10004_zipcode, "5 trips with Jeep alll in 10004 zipcode"

def test_for_total_revenue_for_Jeep():
    total_fare_amount = 0
    total_tax_amount = 0
    total_fare_amount_excluding_dirty_data = 0
    total_tax_amount_excluding_dirty_data = 0
    num_jeep_trips = 0
    with open("taxi_rides.txt", "r") as file:
        for line in file:
            json_object = json.loads(line)
            car_model = json_object["car_model"]
            if car_model != 'Jeep':
                continue
            num_jeep_trips += 1
            fare_amount = json_object["fare_amount"]
            tax_amount = json_object["tax_amount"]
            pax_id = json_object["pax_id"]
            year = datetime.fromisoformat(json_object["start_time"]).year
            total_tax_amount += tax_amount
            total_fare_amount += fare_amount
            if not (fare_amount < 0 or tax_amount < 0 or pax_id is None or year <= 1970):
                total_tax_amount_excluding_dirty_data += tax_amount
                total_fare_amount_excluding_dirty_data += fare_amount

    assert 5 == num_jeep_trips, "5 trips with Jeep"
    assert round(10.1+10.1, 2) == round(total_fare_amount_excluding_dirty_data, 2) , "2 valid trips with Jeep each 10.1 fare"
    assert round(0.1+0.1, 2) == round(total_tax_amount_excluding_dirty_data, 2), "2 valid trips with Jeep each 0.1 tax"
    assert round(10.1+10.1+10.1+10.1-5.0, 2) == round(total_fare_amount, 2)
    assert round(0.1+0.1+0.1+0.1-0.5, 2) == round(total_tax_amount, 2)