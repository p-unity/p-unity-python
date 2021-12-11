#!/usr/bin/env python3
# -*- encoding: utf-8


__banner__ = """ ( Copyright Intermine.com.au Pty Ltd. or its affiliates.
                   SPDX-License-Identifier: Programming-Unity-10.42

  _       _
 (_)     | |
  _    __| |   ___       _ __    _   _
 | |  / _` |  / _ \     | '_ \  | | | |
 | | | (_| | |  __/  _  | |_) | | |_| |
 |_|  \__,_|  \___| (_) | .__/   \__, |
                        | |       __/ |
                        |_|      |___/

)




""" # __banner__


import sys, click; sys.path.insert(0,'depends')
import p_unity.cli_BASIC

@click.command()
@click.option("-f", "--file", default=None)
@click.option("--debug", is_flag=True)
def run(file,debug):
    if file:
        file = open(file, "rt").read()
    p_unity.cli_BASIC.ide_stdio(run=file,debug=debug)

if __name__ == "__main__":
    run()

