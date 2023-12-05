# Powner

Powner is a tool designed to automate the process of updating the owned status in Neo4j BloodHound based on a list of users.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

BloodHound is a powerful tool used for analyzing and visualizing complex active directory environments. Powner simplifies the process of setting users as owned in BloodHound, making it more convenient for security professionals.

## Features

- Efficiently sets users as owned in BloodHound.
- Supports both User and Computer accounts.
- Command-line interface for easy integration into workflows.

## Requirements

- Python 3.x
- neo4j Python library

## Installation

1. Clone the repository:

```
git clone https://github.com/TheProtyro/Powner.git
```

2. Install the required Python packages:

```
cd Powner
pip install -r requirements.txt
```

3. Set up your Neo4j credentials in the Powner.py file. See line 37. Default credentials are neo4j/neo4j.

```
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"), encrypted=False)
```

## Usage

```
usage: Powner.py [-h] -d DOMAIN -f FILE

Easily set users as owned in BloodHound 🐕

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Specify the target domain
  -f FILE, --file FILE  Provide the path to the file containing the list of users
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
