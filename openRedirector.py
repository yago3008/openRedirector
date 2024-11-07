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
    parser.add_argument('-t', '--time', type=float, default=0.3, help='Time delay between requests.')
    parser.add_argument('-T','--threads', type=int, default=2, help='Number of threads to use.')
    parser.add_argument('-cc', '--check-code', type=int, default=300,
                        help="Expected initial response code (200 for manual, 300 for automatic, 300+ for custom)")
    parser.add_argument('--cookies', type=str, help='Cookies in the format "name=value; name2=value2".')
    parser.add_argument('--silent', action='store_true', help='Enable silent mode (no output).')
    args = parser.parse_args()
    return args


def add_domain_in_file(arg_domain, file='payloads.txt'):
    domain = arg_domain.replace("https://", "").replace("http://", "")
    domain = domain.split('/')[0]
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read().replace("FUZZ", domain)
        with open('payload_makeup', 'w+', encoding='utf-8') as f:
            f.write(content)
    except:
        pass


def get_payloads(arg_file=False, file='payload_makeup'):
    try:
        if not arg_file:
            with open(file, 'r', encoding='utf-8') as f:
                payloads = f.read().splitlines()
            return payloads
        with open(arg_file, 'r', encoding='utf-8') as f:
            payloads = f.read().splitlines()
        return payloads
    except FileNotFoundError:
        print(f"{RED}Error: File '{file}' not found.{DEFAULT}")
        exit(1)


def parse_cookies(cookie_string):
    cookies = {}
    if cookie_string:
        pairs = cookie_string.split('; ')
        for pair in pairs:
            name, value = pair.split('=', 1)
            cookies[name] = value
    return cookies


def print_redirect_status(found, full_url, status_code, silent):
    if found:
        print(f'{GREEN}[+] REDIRECT FOUND: {full_url}{DEFAULT}')
    elif not silent:
        print(f'{RED}[-] NO REDIRECT FOUND: {full_url} [{status_code}]{DEFAULT}')


def requester(urls, payloads, time, code, cookies, silent):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in urls:
        for payload in payloads:
            try:
                sleep(time)
                full_url = url + payload
                res = req.get(full_url, allow_redirects=True, headers=headers, cookies=cookies)

                if code == 200:
                    print_redirect_status(res.status_code == code, full_url, res.status_code, silent)

                elif code == res.status_code or (300 <= code < 400 and res.history and len(res.history) <= 1):
                    print_redirect_status(True, full_url, res.status_code, silent)
                else:
                    print_redirect_status(False, full_url, res.status_code, silent)

            except Exception as e:
                if not silent: print(f"{RED}Error: {e}{DEFAULT}")
                pass


def thread_requester(urls, payloads, time, num_threads, code, cookies, silent):
    chunk_size = len(urls) // num_threads
    threads = []
    
    for i in range(num_threads):
        start = i * chunk_size
        if i == num_threads - 1:
            end = len(urls)
        else:
            end = (i + 1) * chunk_size

        thread = threading.Thread(target=requester, args=(urls[start:end], payloads, time, code, cookies, silent))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    args = arg_parser()

    if args.url:
        urls = [args.url]
        add_domain_in_file(args.url)
    elif args.list:
        urls = get_payloads(args.list)
        add_domain_in_file(urls[0])
    else:
        if not sys.stdin.isatty():
            urls = [url.strip() for url in sys.stdin.readlines()]
            add_domain_in_file(urls[0])
        else:
            print(f"{RED}Error: you must provide a url/list or pipe the URLs via stdin.{DEFAULT}")
            exit(1)

    payloads = get_payloads(args.wordlist) if args.wordlist else get_payloads()
    cookies = parse_cookies(args.cookies) if args.cookies else {}
    thread_requester(urls, payloads, time=args.time, num_threads=args.threads, code=args.check_code, cookies=cookies, silent=args.silent)
