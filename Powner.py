#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Powner.py
# Author             : Protyro
# Date created       : 05/12/2023

from neo4j import GraphDatabase, exceptions
import argparse

# ANSI escape sequence
GREEN = '\033[32m'
RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m'

def print_banner():
    print("\n" + BLUE + "Powner.py v1.1 - by @Protyro" + RESET + "\n")

def read_entries_file(file_path):
    entries_owned = []
    print('[>] Reading entries file')

    try:
        with open(file_path, 'r') as entries_file:
            for entry in entries_file:
                entries_owned.append(entry.strip())
        return entries_owned
    except FileNotFoundError:
        print(RED + f"[-] File not found: {file_path}" + RESET)
        exit(1)

def connect_to_neo4j():
    uri = "bolt://localhost:7687/"
    print('[>] Connecting to Neo4j')

    try:
        driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"), encrypted=False)
        return driver
    except exceptions.AuthError as e:
        print("[-] Provided Neo4J credentials are not valid. Change your username and password in the code.")
        exit(1)
    except exceptions.ServiceUnavailable as e:
        print(f"[-] Neo4J does not seem to be available on {uri}.")
        exit(1)
    except Exception as e:
        print("[-] Unexpected error with Neo4J")
        exit(1)

def execute_queries(tx, entries_owned, domain):
    print('[>] Executing queries')

    for entry in entries_owned:
        entry_upper = entry.upper() + "@" + domain
        result = tx.run(
            f'MATCH (c {{name:"{entry_upper}"}}) RETURN c'
        ).single()

        if result is not None and result["c"] is not None and result["c"].get("owned") in (False, None):
            result = tx.run(
                f'MATCH (c {{name:"{entry_upper}"}}) SET c.owned=True RETURN c.name AS name'
            )
            print(GREEN + f"   [+] Node {entry_upper} successfully set as owned in BloodHound" + RESET)
        else:
            print(RED + f"   [-] No result or already owned for entry {entry_upper}" + RESET)

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Easily set users and groups as owned in BloodHound 🐕")
    parser.add_argument("-d", "--domain", help="Specify the target domain", type=str, required=True)
    parser.add_argument("-f", "--file", help="Provide the path to the file containing the list of users and groups", type=str, required=True)
    args = parser.parse_args()

    domain = args.domain.upper()
    entries_file = args.file

    entries_owned = read_entries_file(entries_file)

    driver = connect_to_neo4j()

    with driver.session() as session:
        with session.begin_transaction() as tx:
            execute_queries(tx, entries_owned, domain)

    driver.close()

if __name__ == "__main__":
    main()
