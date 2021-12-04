#!/usr/bin/env python3
import sys
import time
from pathlib import Path
import yaml  # PyYAML
import os
import easygui
import requests
from bs4 import BeautifulSoup
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


def print_elements_list(elements_list_):
    i = 0
    for i in range(len(elements_list_)):
        element = elements_list_[i].find('a')
        if element['class'][1] == 'ass-group':
            print(f'📁 {i}: {element.text}')
        else:
            print(f'📄 {i}: {element.text}')
    print(f'◀️ {i + 1}: go back')
    return int(input("Insert Element :  "))


def submit_chosen(s, url):
    r = s.get(url)
    r = attempt_connection(s, 'get', url, '')
    soup = BeautifulSoup(r.text, 'html5lib')
    # get the form to submit the file
    try:
        request_url = main_url + soup.find('form')['action']
    except TypeError:
        try:
            div = soup.find('div', attrs={'class': ['ass-submit']})
            message = div.find('p').get_text(strip=True)
            print("Can not submit to this assignment")
            print(f'Themis says : {message}')
        except AttributeError or TypeError:
            print_warning('Your link is invalid')
        return
    payload, r, soup = send_submit_request(r, request_url, s, soup)
    if payload and r and soup is None:
        return
    r = send_judge_request(payload, r, s, soup)
    soup = await_results(r, s, soup)
    rows = soup.find_all('tr', {'class': True})
    rows_ = soup.find_all('tr', {'class': False})
    print_test_results(rows, rows_)

def is_link(the_string):
    if 'https' in the_string:
        return True
    else:
        return False

def is_arg(the_string):
    if '-y' in the_string:
        return True
    else:
        return False

def send_submit_request(r, request_url, s, soup):
    files = {}
    try:
        i = 1
        while not is_link(sys.argv[i]):
            global wants_to_print_files
            if not wants_to_print_files and is_arg(sys.argv[i]):
                wants_to_print_files = True
            else:
                files[f'upload-{i}'] = open(sys.argv[i], 'rb') 
            i += 1
    except IndexError:
        try:
            files = {'upload-0': open(easygui.fileopenbox(), 'rb')}
        except TypeError:
            print_warning('No file chosen')
            return None, None, None
    try:
        payload = {
            '_csrf': request_url.split('=')[1]
        }
    except IndexError:
        print_warning("Your link is invalid")
        exit_program()

    r = s.post(request_url, files=files, data=payload)
    soup = BeautifulSoup(r.text, 'html5lib')
    return payload, r, soup


def send_judge_request(payload, r, s, soup):
    # prepare for next request (judge)
    payload['_csrf'] = soup.find('input', attrs={'name': '_csrf'})['value']
    # get form & request url
    judge = soup.find_all('form')[3]
    judge_url = main_url + judge['action']
    # send judge request
    r = attempt_connection(s, 'post', judge_url, payload)
    return r


def await_results(r, s, soup):
    # parse the info
    soup = BeautifulSoup(r.text, 'html5lib')
    is_pending = soup.find('i', attrs={'class': 'pending'})
    url = r.url
    x = 1
    while is_pending is not None:
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        b = "Pending" + "." * x
        sys.stdout.write('\r' + b)
        time.sleep(0.5)
        x = x + 1
        is_pending = soup.find('i', attrs={'class': 'pending'})
    print('\n')
    return soup


def print_test_results(rows, rows_):
    # check for each test case
    j = 0
    l = 0
    for i in range(0, len(rows)):
        tr = rows[i]
        if 'sub-casetop' in tr['class']:
            l += 1
            if tr['class'][1] == 'passed':
                j += 1
                print(f'Test Case {i + 1}: PASSED ✅\n')
            else:
                print(f'Test Case {i + 1}:', end="")
                print_warning(f' FAILED ❌.')
                reason = tr.find("td", attrs={"class": "iconize"}).text
                if reason == '':
                    reason = 'Compile Error'
                
                print(f'Reason: {reason}. '
                      f'{rows_[i * 3].td.text.strip()}\n')
            if wants_to_print_files:
                # find files in, out, diff and err
                tr_ = rows_[i * 3 + 1].find_all('span', attrs={'class':'nowrap'})
                for f in tr_:
                    files_soup = attempt_connection(s, 'get', main_url + f.a['href'], '').text
                    sys.stdout.write(f'\n{f.a.text}:\n{files_soup.strip()}\n')

    global passed_all
    if j == l:
        passed_all = True
        print("Hacker Man!!")
    else:
        passed_all = False


def submit_loop(s, selected_element):
    while True:
        print("0 : Submit")
        print("1 : Go Back")
        choice = int(input("Choose :  "))
        if choice == 0:
            # go to link of a submittable
            url = main_url + selected_element['href']
            submit_chosen(s, url)
        elif choice == 1:
            break
        elif choice == exit_signal:
            exit_program()
        else:
            print_warning(f"Invalid choice")


def get_prev(link):
    prev = main_url
    sec = link.split('/')[3:-1]
    prev += '/'
    for i in range(0, len(sec)):
        prev += sec[i] + '/'
    return prev[0:-1]


def exit_program():
    print("Bye!")
    exit(0)


def command_line_input(s, url):
    print(f'Submitting to {url}')
    submit_chosen(s, url)
    if passed_all:
        print('You passed all test cases, exiting..')
        exit_program()
    else:
        print('You did not pass all test cases :(')
        print('Go ahead and edit your file. Come back when you think you got it.')
    return str(input("\nWanna resubmit ? (Y/n)  "))


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
        os.path.remove(Path(str(Path.home()) + '/.themisSubmitter/data.yaml'))
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
    
def attempt_login(s, data):
    try:
        global r
        soup = BeautifulSoup(r.text, 'html5lib')
        data['_csrf'] = soup.find('input', attrs={'name': '_csrf'})['value']
        # r = s.post(login_url, data=data, headers=headers)
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
        exit_program()


with requests.session() as s:
    print("Welcome, to the Themis submitter by Mohammad Al Shakoush")

    write_path, was_there = create_data_tree()

    if not was_there:
        print("Welcome, this is a first time and one time configuration process."
            "To be able to log you into themis you need:")
        data_config(write_path)
    data = read_data(write_path)

    try:
        i = 1
        while not is_link(sys.argv[i]):
            i += 1
        
        url = sys.argv[i].strip()
        
        r = attempt_connection(s, 'get', url, '')
        while not attempt_login(s, data):
            data_config(write_path)
            data = read_data()
        resubmit = command_line_input(s, url)
        while resubmit != 'n':
            resubmit = command_line_input(s, url)
        exit_program()

    except IndexError:
        url = 'https://themis.housing.rug.nl/course/2021-2022'
        r = attempt_connection(s, 'get', url, '')
        print("You can exit at any time by entering the number 69 or CTRL+Z\n")
        
        while not attempt_login(s, data):
            data_config(write_path)
            data = read_data()
            attempt_login(s, data)
        selected_course_url = url
        
        while True:
            soup1 = BeautifulSoup(r.text, 'html5lib')
            elements_list = soup1.find_all('li', class_='large')
            index = print_elements_list(elements_list)
            if index < len(elements_list):
                selected_element = elements_list[index].find('a')
                # check if the selected is a file
                if selected_element['class'][1] == 'ass-submitable':
                    submit_loop(s, selected_element)
                    selected_course_url = get_prev(selected_course_url)
                    r = attempt_connection(s, 'get', selected_course_url, '')
                else:
                    selected_course_url = main_url + selected_element['href']
                    r = attempt_connection(s, 'get', selected_course_url, '')
            elif index == len(elements_list):
                selected_course_url = get_prev(selected_course_url)
                r = attempt_connection(s, 'get', selected_course_url, '')
            elif index == exit_signal:
                exit_program()
            else:
                print_warning(f'\nNot a valid index\n')