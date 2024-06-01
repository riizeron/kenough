import yaml

from src.utils.read_data import ReadData


with open("config.yml") as f:
    config = yaml.safe_load(f)

logpath = config.get("logpath", "logs")

tmp_path = config.get("tmp")

app_port = config["app"]["port"]

prefixes_to_remove = config["prefixes_to_remove"]

max_unpacked_size = config["max_unpacked_size"]

bb_creds = config["secrets"]["bb-http"]

reader = ReadData(config=config)
postgres_config = reader.get_postgres_config()
kafka_config = reader.get_kafka_config()