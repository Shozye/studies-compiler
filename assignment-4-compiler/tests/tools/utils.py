import json
from .config import Config
from .stats import Statistics
import re
import os

def read_test_config(dir_path: str) -> dict[str, str]:
    config_path = os.path.join(dir_path, Config.TEST_CONFIG)
    with open(config_path, encoding='utf-8') as file:
        test_config = json.loads(file.read())
    
    for testcase in test_config:
        testcase['translated'] = testcase.get('translated', Config.DEFAULT_TRANSLATED)
        testcase['compilation'] = testcase.get("compilation", Config.DEFAULT_COMPILATION)
        if testcase['compilation'] == "ERROR":
            testcase['runtime'] = "ERROR"
        else:
            testcase['runtime'] = testcase.get("runtime", Config.DEFAULT_RUNTIME)
        testcase['stdin'] = testcase.get("stdin", Config.DEFAULT_STDIN)
        testcase['stdout'] = testcase.get("stdout", Config.DEFAULT_STDOUT)
        testcase['description'] = testcase.get("description", Config.DEFAULT_DESCRIPTION)
    
    return test_config

def listdir(path: str, regex: str):
    p = re.compile(regex)
    return [ name for name in os.listdir(path) if p.match(name) ]

def run_test(testcase_path: str, stdin: str, stdout: str) -> dict[str, int]:
    """Here we run testcase with subprocess by using compiler and running virtual machine"""

def run_tests(dir_path: str, stats: Statistics):
    test_config = read_test_config(dir_path)
    for test in test_config:
        run_test(os.path.join(dir_path, test['filename']), test['stdin'], test['stdout'])
    
    


    
    