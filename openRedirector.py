#!/usr/bin/env python3

import sys
import requests as req
import argparse
import os
from time import sleep
import threading

RED = '\033[91m'
GREEN = '\033[92m'
DEFAULT = '\033[0m'

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='URL.')
    parser.add_argument('-l', '--list', type=str, help='List of URLs.')
    parser.add_argument('-w', '--wordlist', type=str, help='Path to wordlist.')
    parser.add_argument('-t', '--time', type=float, default=0.5, help='Time delay between requests.')
    parser.add_argument('-T','--threads', type=int, default=2, help='Number of threads to use.')
    args = parser.parse_args()
    return args

def get_payloads(file='payloads.txt'):
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
                    if len(response.history) <= 1:
                        print(f'{GREEN}[+] REDIRECT FOUND: {full_url}{DEFAULT}')
                else:
                    print(f'{RED}[-] NO REDIRECT FOUND: {full_url}{DEFAULT}')
            except Exception as e:
                print(f"{RED}Error: {e}{DEFAULT}")
                pass

def thread_requester(urls, payloads, time, num_threads):
    chunk_size = len(urls) // num_threads
    threads = []
    
    for i in range(num_threads):
        start = i * chunk_size
        if i == num_threads - 1:
            end = len(urls)
        else:
            end = (i + 1) * chunk_size

        thread = threading.Thread(target=requester, args=(urls[start:end], payloads, time))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    args = arg_parser()

    if args.url:
        urls = [args.url]
    elif args.list:
        urls = load_urls(args.list)
    else:
        if not sys.stdin.isatty():
            urls = [url.strip() for url in sys.stdin.readlines()]
        else:
            print(f"{RED}Error: you must provide a url/list or pipe the URLs via stdin.{DEFAULT}")
            exit(1)

    payloads = get_payloads(args.wordlist)  if args.wordlist else get_payloads()
    thread_requester(urls, payloads, time=args.time, num_threads=args.threads)
