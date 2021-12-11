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
import p_unity.cli_UNITY

@click.command()
@click.option("-f", "--file", default=None)
@click.option("-d", "--debug", default=False)
def run(file,debug=False):
    if file:
        file = open(file, "rt").read()
    p_unity.cli_UNITY.ide_stdio(run=file,debug=debug)

if __name__ == "__main__":
    run()

