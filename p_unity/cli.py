#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

         _   _
        | | (_)
   ___  | |  _       _ __    _   _
  / __| | | | |     | '_ \  | | | |
 | (__  | | | |  _  | |_) | | |_| |
  \___| |_| |_| (_) | .__/   \__, |
                    | |       __/ |
                    |_|      |___/

)





""" # __banner__

class IDE:

    def __init__(self):

        self.e = FORTH.Engine()

    def stdio(self):

        e = self.e

        e.running = -1
        def exit(self, v):
            self.running = v
        e.exit = exit

        e.word("Q", lambda f: f.exit(f,0))
        e.word("BYE", lambda f: f.exit(f,0))
        e.word("QUIT", lambda f: f.exit(f,0))

        e.word("S", lambda f: f.exit(f,1))
        e.word("STOP", lambda f: f.exit(f,1))

        print("")

        p = e.TEST.p_count / (e.TEST.p_count + e.TEST.f_count)
        print(f"p-unity FORTH v42.01 ({p*100}% Sanity Tests OK)")

        while e.running == -1:

            print(" > ", end="")
            line = input("")
            line = line.strip()

            #try:
            e.execute(line.split(), rollback=True)
            #except Exception as ex:
            #    details = str(ic(ex))
            #    rich.print(f"[bold red]{details}[/]")

            print("=> ", end="")
            for object in e.stack:
                object = repr(object)
                print(f"{object}", end=" ")

            print("")

        print("")
        sys.exit(e.running)


import sys

from . import FORTH


