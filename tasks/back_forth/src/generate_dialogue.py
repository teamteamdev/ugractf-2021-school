#!/usr/bin/env python3

a = open("alice.h", "w")
b = open("bob.h", "w")

alice_now = True

with open("dialog.txt") as dialog:
    for line in dialog:
        line = line.strip()
        if line == "":
            continue
        sender, recver = (a, b) if alice_now else (b, a)
        if line == "FLAG":
            sender.write("send_line(fd, get_flag());\n")
        else:
            sender.write(f"send_line(fd, \"{line}\");\n")
        recver.write("receive_line(fd);\n")
        alice_now = not alice_now

a.close()
b.close()
