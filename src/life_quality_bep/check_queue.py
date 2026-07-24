import subprocess
import numpy as np
from rich import print
from .lq_utilities import on_wendian, ssh_modify_command, get_wendian_username


def get_queue_vals() -> str:
    command = ["squeue", '--format="%.18i %.30u %.8t"']
    if not on_wendian():
        command = ssh_modify_command(command)
    data = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    my_data = data.stdout
    if on_wendian():
        my_data = "\n".join([i.strip("\"") for i in my_data.split("\n")])
    return my_data.strip()


def count_queue_lines(data) -> int:
    return len(data.split("\n"))


def collect_queue_names(data) -> int:
    name_index = 1

    return np.array([i.strip().split()[name_index] for i in data])


def collect_queue_running(data) -> int:
    status_index = 2
    return np.array([i.strip().split()[status_index] == "R" for i in data])


def chkq():
    data = get_queue_vals()
    split_data = data.split("\n")[1:-1]
    names = collect_queue_names(split_data)
    running = collect_queue_running(split_data)
    name_counts = np.unique_counts(names)
    running_vals = [sum(running[names == i]) for i in name_counts[0]]
    sorted_indeces = name_counts[1].argsort()
    users_name = get_wendian_username()
    user_string = "user"
    print(f"[green]{user_string:.<25}running/total ")
    for i in sorted_indeces:
        print_string = f"[white]{str(name_counts[0][i]):.<25}{running_vals[i]}/{str(name_counts[1][i])} "
        if users_name in print_string:
            print_string = "[bold][reverse]" + print_string

        print(print_string)
