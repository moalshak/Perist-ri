#!/usr/bin/env python3
import os
import requests
import yaml  # PyYAML
from bs4 import BeautifulSoup
from pathlib import Path
from termcolor import colored

login_url = 'https://themis.housing.rug.nl/log/in'
main_url = 'https://themis.housing.rug.nl'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

exit_signal = 69
passed_all = False

wants_to_print_files = False


def print_warning(text):
    print(colored(text, 'red'))


def print_green(text):
    print(colored(text, 'green'))


def exit_program():
    print("Bye!")
    exit(0)


def data_config(write_path):
    try:
        s_number = str(input("Student number: "))
        pass_word = str(input("Your Password: "))
        data = {
            '_csrf': '',
            'user': s_number,
            'password': pass_word
        }
        with open(write_path, "w") as stream:
            try:
                yaml.dump(data, stream, default_flow_style=False, allow_unicode=True)
            except yaml.YAMLError as event:
                print(event)
    except KeyboardInterrupt:
        print('\nAborting...')
        # os.path.remove(Path(str(Path.home()) + '/.themisSubmitter/data.yaml'))
        exit(1)


def attempt_connection(session, request_type, url, data):
    try:
        if request_type == 'get':
            r = session.get(url, headers=headers)
        elif request_type == 'post':
            r = session.post(url, data=data, headers=headers)

        return r
    except requests.exceptions.ConnectionError:
        print_warning("Connection Error. Please make sure you are connected to the internet and try again")
        exit_program()


def attempt_login(r, s, data):
    try:
        soup = BeautifulSoup(r.text, 'html5lib')
        data['_csrf'] = soup.find('input', attrs={'name': '_csrf'})['value']
        r = attempt_connection(s, 'post', login_url, data)
        if r.status_code != (200 or 302):
            print("Login Failed ❌.\nYour password or student number is/are incorrect\nstarting the data updater...")
            return False
        print("Login successful ✅")
        return True
    except NameError or TypeError:
        return False


def create_data_tree():
    was_there = True
    write_path = str(Path.home()) + '/.themisSubmitter'
    if not os.path.exists(write_path):
        Path(write_path).mkdir(parents=True, exist_ok=True)
    write_path += '/data.yaml'
    if not os.path.exists(write_path):
        was_there = False
        Path(write_path).touch(exist_ok=True)
    return write_path, was_there


def read_data(write_path):
    data = {}
    try:
        with open(write_path, 'r') as stream:
            print('Reading your data (username & password)')
            data1 = yaml.safe_load(stream)
            data['user'] = data1['user']
            data['password'] = data1['password']
            data['_csrf'] = data1['_csrf']
            print('Reading successful')
            return data
    except TypeError:
        print('Invalid data found')
        return data


def main():
    with requests.session() as s:
        print("Welcome, to the Themis submitter by Mohammad Al Shakoush")

        write_path, was_there = create_data_tree()

        print(write_path)

        if not was_there:
            print("Welcome, this is a first time and one time configuration process."
                  "To be able to log you into themis you need:")
            data_config(write_path)

        data = read_data(write_path)
        while data == {}:
            data_config(write_path)
            data = read_data(write_path)

        url = 'https://themis.housing.rug.nl/file/2021-2022/cs-SS/lab3/ex6/@tests/1.in'

        r = attempt_connection(s, 'get', url, '')
        while not attempt_login(r, s, data):
            data_config(write_path)
            data = read_data(write_path)

        for i in range(1, 11):
            url = f'https://themis.housing.rug.nl/file/2021-2022/cs-SS/lab3/ex6/@tests/{i}.in'
            r = attempt_connection(s, 'get', url, '')
            open(f'tests/{i}.in', 'wb').write(r.content)
            url = f'https://themis.housing.rug.nl/file/2021-2022/cs-SS/lab3/ex6/@tests/{i}.out'
            r = attempt_connection(s, 'get', url, '')
            open(f'tests/{i}.out', 'wb').write(r.content)

        # subprocess.Popen(f'gcc -O2 -std=c99 -pedantic -Wall -o 4a.out 4.c -lm', shell=True)
        # for i in range(1, 11):
        #     subprocess.Popen(f'diff <(./4a.out < tests/{i}.in) tests/{i}.out', shell=True)


if __name__ == "__main__":
    main()
