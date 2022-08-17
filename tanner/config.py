import logging
import os
import sys

import yaml

LOGGER = logging.getLogger(__name__)


class TannerConfig():
    config = {'DATA': {'db_config': '/opt/tanner/db/db_config.json', 'dorks': '/opt/tanner/data/dorks.pickle', 'user_dorks': '/opt/tanner/data/user_dorks.pickle', 'crawler_stats': '/opt/tanner/data/crawler_user_agents.txt', 'geo_db': '/opt/tanner/db/GeoLite2-City.mmdb', 'tornado': '/opt/tanner/data/tornado.py', 'mako': '/opt/tanner/data/mako.py'}, 'TANNER': {'host': '0.0.0.0', 'port': 8090}, 'WEB': {'host': '0.0.0.0', 'port': 8091}, 'API': {'host': '0.0.0.0', 'port': 8092, 'auth': False, 'auth_signature': 'tanner_api_auth'}, 'PHPOX': {'host': '0.0.0.0', 'port': 8088}, 'REDIS': {'host': 'localhost', 'port': 6379, 'poolsize': 80, 'timeout': 1}, 'EMULATORS': {'root_dir': '/opt/tanner'}, 'EMULATOR_ENABLED': {'sqli': True, 'rfi': True, 'lfi': True, 'xss': True, 'cmd_exec': True, 'php_code_injection': True, 'php_object_injection': True, 'crlf': True, 'xxe_injection': True, 'template_injection': True}, 'SQLI': {'type': 'SQLITE', 'db_name': 'tanner_db', 'host': 'localhost', 'user': 'root', 'password': 'user_pass'}, 'POSTGRES': {'db_name': 'tanner', 'host': '0.0.0.0', 'port': 5432, 'user': 'user_name', 'password': 'user_password', 'poolsize': 80, 'timeout': 1}, 'XXE_INJECTION': {'OUT_OF_BAND': False}, 'RFI': {'allow_insecure': False}, 'DOCKER': {'host_image': 'busybox:latest'}, 'LOGGER': {'log_debug': '/opt/tanner/tanner.log', 'log_err': '/opt/tanner/tanner.err'}, 'MONGO': {'enabled': False, 'URI': 'mongodb://localhost'}, 'HPFEEDS': {'enabled': False, 'HOST': 'localhost', 'PORT': 10000, 'IDENT': '', 'SECRET': '', 'CHANNEL': 'tanner.events'}, 'LOCALLOG': {'enabled': False, 'PATH': '/tmp/tanner_report.json'}, 'CLEANLOG': {'enabled': False}, 'REMOTE_DOCKERFILE': {'GITHUB': 'https://raw.githubusercontent.com/mushorg/tanner/master/docker/tanner/template_injection/Dockerfile'}, 'SESSIONS': {'delete_timeout': 300}}


    @staticmethod
    def read_config(path):
        config_values = {}
        try:
            with open(path, 'r') as f:
                config_values = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.parser.ParserError as e:
            print("Couldn't properly parse the config file. Please use properly formatted YAML config.")
            sys.exit(1)
        return config_values

    @staticmethod
    def set_config(config_path):
        if not os.path.exists(config_path):
            print("Config file {} doesn't exist. Check the config path or use default".format(
                config_path))
            sys.exit(1)

        TannerConfig.config = TannerConfig.read_config(config_path)

    @staticmethod
    def get(section, value):
        try:
            print(TannerConfig.config)
            res = TannerConfig.config[section][value]
        except (KeyError, TypeError):
            res = DEFAULT_CONFIG[section][value]

        return res


DEFAULT_CONFIG = TannerConfig.read_config("/opt/tanner/data/config.yaml")
