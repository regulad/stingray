#!/usr/bin/python3
"""
Stingray Server Startup Script
"""
from argparse import ArgumentParser
from os import environ, remove
from sys import stdin, stderr, stdout
from os.path import exists, join
from subprocess import run, Popen, DEVNULL

parser = ArgumentParser(description="Stingray Server Script")
parser.add_argument("--distro", dest="distro", type=str)
parser.add_argument("--desktop", dest="desktop", type=str)

args = parser.parse_args()

print("                                                                                ")
print("                    .;,                                                         ")
print("                    ;ol.                                                        ")
print("                   ,lol;                                                        ")
print("                 .;lolol,                                                       ")
print("                .:llollll,                                                      ")
print("               .cololoolll;.                                                    ")
print("               ;ollolllolll:,..                                 ...             ")
print("              'lollllllllllloll:'.                          ...                 ")
print("             'lollllllllllllllllll:;'..                 ....                    ")
print("            .collllllllllllllllollllolc:;,.         ....                        ")
print("        .,;:lolllllllllllllllllollollllloolc;''',;'..                           ")
print("      .:lolllllolllllllllllllllllllolllllllloooooc.                             ")
print("      ,ollolloollllllllllllllllllllllllllllllllllo:.                            ")
print("      .:olllloolllllllllllllllllllllllllllllllllol,                             ")
print("       'loloolollllllllllllllllllllllllllllllolol:.                             ")
print("        ,looollllollllllllllllllllllllllollololol.                              ")
print("         .',;:cclollolllllllllllllllllllllollolo;                               ")
print("               ..':lolllllllllllllllllllllollloc.                               ")
print("                   .;lllllllllllllllllllllollol'                                ")
print("                     'coollollllllllllllolollol.                                ")
print("                      .':looolllllllllllllollol.                                ")
print("                         .:lolllllllllloooollol.                                ")
print("                           .;lolllllllloollolol'                                ")
print("                             .,coloollloollllloc.                               ")
print("                               .,collollllllllloc.                              ")
print("                                 .:lolloollolollol'                             ")
print("                                   .;looollolllllol'                            ")
print("                                     .,:lloollolllol,.                          ")
print("                                        ..,:loollllolc'                         ")
print("                                            .',:ccloooc'                        ")
print("                                                 ..';:c:.                       ")
print("                                                      ..                        ")

print(" ______    _______     __     __   __     ______      __ __       _____      __  __   ")
print("/ ____/\ /\_______)\  /\_\   /_/\ /\_\   /_/\___\    /_/\__/\    /\___/\   /\  /\  /\ ")
print(") ) __\/ \(___  __\/  \/_/   ) ) \ ( (   ) ) ___/    ) ) ) ) )  / / _ \ \  \ \ \/ / / ")
print(" \ \ \     / / /       /\_\ /_/   \ \_\ /_/ /  ___  /_/ /_/_/   \ \(_)/ /   \ \__/ /  ")
print(" _\ \ \   ( ( (       / / / \ \ \   / / \ \ \_/\__\ \ \ \ \ \   / / _ \ \    \__/ /   ")
print(")____) )   \ \ \     ( (_(   )_) \ (_(   )_)  \/ _/  )_) ) \ \ ( (_( )_) )   / / /    ")
print("\____\/    /_/_/      \/_/   \_\/ \/_/   \_\____/    \_\/ \_\/  \/_/ \_\/    \/_/     ")

print("Starting Stingray server...")
print(args.desktop + " on " + args.distro)

print()

# Some code taken from https://github.com/novnc/noVNC/blob/master/utils/novnc_proxy

if exists(join(environ["PATH"], ".vnc", "passwd")):
    remove(join(environ["PATH"], ".vnc", "passwd"))
# Delete the password file if it exists.

run(["vncpasswd"], input=bytes(f"{environ['VNC_PASSWORD']}\n{environ['VNC_PASSWORD']}\n\n", encoding="UTF-8"))

print()

run(["vncserver", ":1", "-geometry", f"{environ['VNC_WIDTH']}x{environ['VNC_HEIGHT']}", "-depth", "24", "-name", f"Stringray-{environ['P_SERVER_UUID']}"])

print()

shell_env = {}

if args.distro == "debian":
    shell_env["DEBIAN_FRONTEND"] = "dialog"

shell_path = environ.get("SHELL")

if shell_path is None:
    if args.distro == "debian":
        shell_path = "/bin/bash"
    elif args.distro == "alpine":
        shell_path = "/bin/ash"
    elif exists(join("bin", "sh")):
        shell_path = "/bin/sh"
        
if shell_path is not None:
    print("Will attempt to open shell " + shell_path)

try:
    with Popen([f"/opt/websockify/websockify-{environ['WEBSOCKIFY_VERSION']}/run", environ["SERVER_PORT"], "localhost:5901"], stdin=DEVNULL) as websockify:
        print()
        print("Ready for connection!")
        if shell_path is not None:
            with Popen([shell_path], stdin=stdin, stderr=stderr, stdout=stdout) as shell:
                print()
                print("Shell opened!")
                print()
                return_code = shell.wait()
                print()
                print("Shell process returned exit code " + return_code)
        else:
            websockify.wait()
except KeyboardInterrupt:
    websockify.terminate()
    print()
    print("Websockify process returned exit code " + websockify.returncode)
    run(["vncserver", "-clean", "-kill", ":1"], stdin=DEVNULL)
