import yaml
import json

def run_conf():
    with open('userconf.yaml') as f:
        userconf = yaml.load(f)

    print(userconf)


run_conf()

