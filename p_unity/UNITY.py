#!/usr/bin/env python3
# -*- encoding: utf-8
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 - 2021, Scott.McCallum@HQ.UrbaneINTER.NET

__banner__ = r""" (

     _      _    _   _   _   _____   _______  __     __
  /\| |/\  | |  | | | \ | | |_   _| |__   __| \ \   / /
  \ ` ' /  | |  | | |  \| |   | |      | |     \ \_/ /
 |_     _| | |  | | | . ` |   | |      | |      \   /
  / , . \  | |__| | | |\  |  _| |_     | |       | |
  \/|_|\/   \____/  |_| \_| |_____|    |_|       |_|



)







"""  # __banner__

class Engine:  # { The Reference Implementation of p-unity }

    def __init__(self, run=None, run_tests=1, **kwargs):
        self.engine = None
        self.guards = kwargs.get('guards', "```")

    def execute(self, lines):

        lines = lines.split("\n")

        guards = "```"
        gather = {}

        control = None

        include = False
        block = 0
        index = -1
        for line in lines:
            index += 1

            if line.lstrip()[0:3] == guards[0:3]:
                block += 1
                include = ~include
                language = line.lstrip()[3:].split(" ")[0].lower()
                language = "forth" if language == "" else language
                language = "scrpt" if language == "javascript" else language
                continue

            if not include: continue

            assert language in ["forth", "basic", "scrpt"]
            if not control: control = language
            by_lang = gather.get(language,[])
            by_lang.append((block,line))
            gather[language] = by_lang

        if control == "forth":
            from .FORTH import Engine as EngineFORTH
            self.engine = EngineFORTH()
            if "basic" in gather:
                if not self.engine.eBASIC:
                    from .BASIC import Engine as EngineBASIC
                    self.engine.eBASIC = EngineBASIC()
                for block, line in gather["basic"]:
                    self.engine.eBASIC.interpret(line)

            lines = []
            for block, line in gather["forth"]:
                lines.append(line)

            self.engine.execute(lines=lines, include=True)

        elif control == "basic":
            from .BASIC import Engine as EngineBASIC
            self.engine = EngineBASIC()
            if "forth" in gather:
                for block, line in gather["forth"]:
                    self.engine.eFORTH.interpret(line)

            for block, line in gather["basic"]:
                self.engine.interpret(line)

            self.engine.interpret("run")

