import requests as req
import argparse
import os
from time import sleep

RED = '\033[91m'
GREEN = '\033[92m'
DEFAULT = '\033[0m'

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='URL.')
    parser.add_argument('-l', '--list', type=str, help='List of URLs.')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Path to wordlist.')
    parser.add_argument('-t', '--time', type=float, default=0, help='Time delay between requests.')
    args = parser.parse_args()
    return args

def get_payloads(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            payloads = f.read().splitlines()
        return payloads
    except FileNotFoundError:
        print(f"{RED}Error: File '{file}' not found.{DEFAULT}")
        exit(1)

def load_urls(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            urls = f.read().splitlines()
        return urls
    except FileNotFoundError:
        print(f"{RED}Error: File '{file}' not found.{DEFAULT}")
        exit(1)

def requester(urls, payloads, time):
    for url in urls:
        for payload in payloads:
            try:
                sleep(time)
                full_url = url + payload
                response = req.get(full_url, allow_redirects=True)
                if response.history:
                    print(f'{GREEN}[+] REDIRECT FOUND: {full_url}{DEFAULT}')
                else:
                    print(f'{RED}[-] NO REDIRECT FOUND: {full_url}{DEFAULT}')
            except:
                pass

if __name__ == '__main__':
    args = arg_parser()
    if args.url:
        urls = [args.url]
    elif args.list:
        urls = load_urls(args.list)
    else:
        print(f"{RED}Error: you may to give a url/list.{DEFAULT}")
        exit(1)

    payloads = get_payloads(args.wordlist)
    requester(urls, payloads, time=args.time)
