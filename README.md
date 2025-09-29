# README of the project HBnB

![Project Status](https://img.shields.io/badge/status-development-yellow)  ![License: Edu](https://img.shields.io/badge/license-Educational-lightgrey)  ![buil with](https://img.shields.io/badge/built_with-❤️‍🔥-df0000)

<p align="center"><img src="Picture/giphy.gif" alt="Ghost in the Shell (1995)" width="600"><!-- markdownlint-disable-line MD033 --></p>

## 📖 Description


## 🧭 Index

1 - [⚙️ Cloning and Compilation](#️-cloning-and-compilation)\
2 - [🚀 Features / Limitations](#-features--limitations)\
3 - [📚 Files in Repository](#-files-in-repository)\
4 - [📄 Man Page](#-man-page)\
5 - [🗺️ Flowchart](#%EF%B8%8F-flowchart)\
6 - [🧪 Tests and outputs](#-tests-and-outputs)\
7 - [📁 Project Structure](#-project-structure)\
8 - [👥 Authors](#-authors)\
9 - [📜 License](#-license)

## ⚙️ Cloning and Compilation

### ✅ Prerequisites

**GCC** installed on your system.\
**Ubuntu 20.04 LTS** (or equivalent).

### 📥 Clone and execution

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Clone repo` | `git clone https://github.com/CecileLAROCHE/holbertonschool-simple_shell.git` |
| `Compile` | `gcc -Wall -Werror -Wextra -pedantic -std=gnu89 *.c -o hsh` |
| `Run shell:` | `./hsh` |

## 🚀 Features / Limitations

### ✅ Features

* Displays a prompt and waits for user input.
* Executes commands found in the current directory or in the `$PATH`.
* Supports command arguments.
* Handles environment variables (custom `_getenv` and `print_env`).
* Man page available (`man ./man_1_simple_shell`).
* Interactive **and** non-interactive modes.

### ⚠️ Limitations

* 
* No shell scripting (`if`, `while`, `for`, etc.).
* Error handling is basic compared to full-featured shells.
* Limited set of built-in commands (only those implemented in this project).

## 📚 Files in Repository

### 🖥️ Source Code Files

| File                   | Description                                                                                         |
| ---------------------- | --------------------------------------------------------------------------------------------------- |
| `shell.h`              | Header file containing function prototypes, macros, and struct definitions used across the project. |
| `main.c`               | Entry point of the shell, initializes the program and starts the main loop.                         |
| `read_line.c`          | Handles user input by reading a line from standard input.                                           |
| `process_command.c`    | Parses the input line into tokens and prepares the command for execution.                           |
| `print_env.c`          | Prints the current environment variables.                                                           |
| `execute_command.c`    | Handles the execution of built-in and external commands.                                            |
| `_getenv.c`            | Custom implementation of `getenv`, retrieves environment variables.                                 |
| `_find_path_command.c` | Finds the absolute path of a command by searching in the `PATH` environment variable.               |

### 📑 Documentation Files

| File                 | Description                                                       |
| -------------------- | ----------------------------------------------------------------- |
| `` |  |
| `README.md`          | Main project documentation.                           |
| `AUTHORS`            | List of project contributors.                                     |

## 📋 Man page

This project contains a man page in the repository files. You can directly run it in the shell doing : `man ./man_1_simple_shell`

## 🗺️ Flowchart

## 🧪 Tests and Outputs

## 📁 Project Structure

| 📂 Directory / File | 📝 Description |
|---------------------|----------------|
| **Part 1** | |
| ├── **image** | Documentation assets  |
| ├──  |  |
| ├──  |  |
| ├──  |  |
| ├──  |  |
| ├──  |  |
| ├──  |  |
| ├──  |  |
| **AUTHORS** | List of contributors |
| **README.md** | Main project documentation |

## 👥 Authors

This project was developed by Holberton student as a programming exercise.\
\
**Cécile LAROCHE** [GitHub](https://github.com/CecileLAROCHE)

## 📜 License

This project is for educational purposes only as part of Holberton School.