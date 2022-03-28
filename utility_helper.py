import json
from kafka import KafkaConsumer
from kafka import TopicPartition
import time
import statistics


OPERATION_MAX = "MAX"
OPERATION_MIN = "MIN"
INPUT_FILENAME = "output_file.txt"
RESULTS_FILENAME = "results_file.txt"
MINUTE = "MINUTE"
DISTANCE = "DISTANCE"
CAR_ID = "CAR_ID"
TOPIC_NAME = "messages-3dsignals"
BOOTSTRAP_SERVERS = "localhost:9092"
AUTO_OFFSET_RESET = "earliest"
TIME_DELTA = 60


def manage_consumer(partition, operation):

    consumer = KafkaConsumer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset=AUTO_OFFSET_RESET
    )
    consumer.assign([TopicPartition(TOPIC_NAME, partition)])
    start = time.time()
    values_lst = []
    minute = 0
    for message in consumer:
        current_message = json.loads(message.value)
        values_lst.append(float(current_message.get('distance')))
        end = time.time()
        if end - start >= TIME_DELTA:
            with open(INPUT_FILENAME, "a") as myfile:
                if operation == OPERATION_MAX:
                    myfile.write(f"{max(values_lst)} {current_message.get('car_id')} {minute}")
                elif operation == OPERATION_MIN:
                    myfile.write(f"{min(values_lst)} {current_message.get('car_id')} {minute}")
                else:
                    myfile.write(f"{statistics.fmean(values_lst)} {current_message.get('car_id')} {minute}")
                myfile.write("\n")
            start = time.time()
            minute += 1
            values_lst = []


def aggregate_results_to_file():

    result_dict = {}
    with open(INPUT_FILENAME) as file:
        for line in file:
            splitted_line = line.rstrip().split()
            if splitted_line[2] in result_dict:
                result_dict[splitted_line[2]][0].append(float(splitted_line[0]))
            else:
                result_dict[splitted_line[2]] = ([float(splitted_line[0])], splitted_line[1])
        file.close()
    with open(RESULTS_FILENAME, "a") as file:
        file.write(f"{MINUTE} {DISTANCE} {CAR_ID}")
        file.write("\n")
        for key in result_dict:
            file.write(f"{int(key)}       {min(result_dict[key][0])}    {result_dict[key][1]}")
            file.write("\n")


if __name__ == '__main__':

    aggregate_results_to_file()