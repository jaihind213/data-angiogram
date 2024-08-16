import logging
import sys
import time

from confluent_kafka import Consumer, KafkaError


class KafkaException(Exception):
    def __init__(self, *args, **kwargs):
        self.msg = kwargs.get("msg", "")
        self.response_status = kwargs.get("response_status", -1)

    def __str__(self):
        details = "" if self.__cause__ is None else repr(self.__cause__)
        return (
            f"error: msg {self.msg}, "
            f"response_status: {self.response_status}. "
            f"details: {details}"
        )


def consume(
    time_to_run_sec,
    bootstrap_servers,
    group_id,
    topics,
    offset_reset: str = "earliest",  # noqa: E501
):
    """
    consume messages from topic hosted on bootstrap_servers
    :param time_to_run_sec: the total time in seconds the consumer will run to consume messages.  # noqa: E501
    :param bootstrap_servers:
    :param group_id:
    :param topic:
    :return: num of msgs consumed
    """
    conf = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": group_id,
        "auto.offset.reset": offset_reset,
    }

    # Create Kafka consumer
    consumer = Consumer(conf)

    # Subscribe to topic
    consumer.subscribe(topics)

    # Consume messages for specified time
    end_time = time.time() + time_to_run_sec
    num_msg_received = 0

    try:
        while time.time() < end_time:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition
                    print(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Process the received message
                logging.debug("Received message: {}".format(msg.value()))
                num_msg_received += 1
    except KeyboardInterrupt:
        pass
    finally:
        # Close the consumer
        consumer.close()

    print(f"Total messages received: {num_msg_received}")
    return num_msg_received


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: python kafka_check.py <time_to_run_sec> <bootstrap_servers>"  # noqa: E501
            " <group_id> <topics> <min_msg_received> (topics are comma seperated ie. a,b,c)"
        )
        sys.exit(1)

    time_to_run = int(sys.argv[1])
    bootstrap_servers = sys.argv[2]
    group_id = sys.argv[3]
    topics = sys.argv[4].split(",")
    min_msg_expected = int(sys.argv[5])

    num_msg_received = consume(time_to_run, bootstrap_servers, group_id, topics)

    print(
        "min_msg_expected=",
        min_msg_expected,
        ", num_msg_received=",
        num_msg_received,  # noqa: E501
    )
    if num_msg_received < min_msg_expected:
        exit(123)
