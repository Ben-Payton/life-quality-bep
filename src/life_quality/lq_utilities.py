import socket
import os
import subprocess


def on_wendian() -> bool:
    """Checks whether or not user is on wendian

    Returns:
        bool: True if the user is on wendian.
    """
    return "wendian" in socket.gethostname()


def ssh_modify_command(command: list[str], ssh_target: str = "wendian") -> list[str]:
    """Generates a modified list to ssh to a target for a command.

    Args:
        command (list[str]): The list of strings to be passed to subprocess
        ssh_target (str, optional): The ssh target. Defaults to "wendian".

    Raises:
        ValueError: command must be of type list

    Returns:
        list[str]: The modified list
    """
    if type(command) is not list:
        raise ValueError("command must be of type list")
    new_command = ["ssh", ssh_target]
    for command_piece in command:
        new_command.append(command_piece)
    return new_command


def get_wendian_username(ssh_target: str = "wendian") -> str:
    """Gets the user's name on wendian

    Args:
        ssh_target (str, optional): The ssh target name Defaults to "wendian".

    Returns:
        str: The users user name on wendian.
    """

    if on_wendian():
        return os.getlogin()
    my_name_output = subprocess.run(
        ssh_modify_command(["whoami"], ssh_target),
        capture_output=True,
        encoding="utf-8",
    )
    return my_name_output.stdout.strip()
