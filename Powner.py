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
    print("\n" + BLUE + "Powner.py v1.0 - by @Protyro" + RESET + "\n")

def read_users_file(file_path):
    users_owned = []
    print('[>] Reading users file')
    
    try:
        with open(file_path, 'r') as usersfile:
            for user in usersfile:
                users_owned.append(user.strip())
        return users_owned
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

def execute_queries(tx, users_owned, domain):
    print('[>] Executing queries')
    
    for user in users_owned:
        if user[-1] == "$":
            user_owned = user[:-1].upper() + "." + domain
            account_type = "Computer"
        else:
            user_owned = user.upper() + "@" + domain
            account_type = "User"

        result = tx.run(
            f'MATCH (c:{account_type} {{name:"{user_owned}"}}) RETURN c'
        ).single()

        if result is not None and result["c"] is not None and result["c"].get("owned") in (False, None):
            result = tx.run(
                f'MATCH (c:{account_type} {{name:"{user_owned}"}}) SET c.owned=True RETURN c.name AS name'
            )
            print(GREEN + f"   [+] Node {user_owned} successfully set as owned in BloodHound" + RESET)
        else:
            print(RED + f"   [-] No result or already owned for user {user_owned}" + RESET)

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Easily set users as owned in BloodHound 🐕")
    parser.add_argument("-d", "--domain", help="Specify the target domain", type=str, required=True)
    parser.add_argument("-f", "--file", help="Provide the path to the file containing the list of users", type=str, required=True)
    args = parser.parse_args()

    domain = args.domain.upper()
    users_file = args.file

    users_owned = read_users_file(users_file)

    driver = connect_to_neo4j()

    with driver.session() as session:
        with session.begin_transaction() as tx:
            execute_queries(tx, users_owned, domain)

    driver.close()

if __name__ == "__main__":
    main()
