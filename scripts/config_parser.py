
import yaml
import json
import argparse


config_data = {}

def load_json_config(json_file):
    # TODO error checking
    with open(json_file, 'r') as fp:
        return json.load(fp)

def load_yaml_config(yaml_file):
    with open(yaml_file, 'r') as fp:
        return yaml.safe_load(fp)

def write_json(json_file, config_data):
    json_string = json.dumps(config_data, indent=4, sort_keys=True)
    with open(json_file, 'w') as fp:
        fp.write(json_string)

def write_yaml(yaml_file, config_data):
    with open(yaml_file, 'w') as fp:
        yaml.dump(config_data, fp)

parse = argparse.ArgumentParser()

parse.add_argument("-j", "--json-file", help="JSON config file")
parse.add_argument("-y", "--yaml-file", help="YAML config file")
parse.add_argument("--to-json", action="store_true", help="Generate JSON file from YAML")
parse.add_argument("--to-yaml", action="store_true", help="Generate YAML file from JSON")

args = parse.parse_args()

if args.to_yaml:
    config_data = load_json_config(args.json_file)
    write_yaml(args.yaml_file, config_data)
elif args.to_json:
    config_data = load_yaml_config(args.yaml_file)
    write_json(args.json_file, config_data)
else:
    print("Wrong argument")