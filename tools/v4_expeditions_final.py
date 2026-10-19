#!/usr/bin/env python3
"""
The expeditions page's final build, under the name the house rules give it.
The generator itself is tools/v4_expeditions.py (option C, "The atlas", with
the judges' grafts and fixes); this only runs it, so both names build the
same prototypes/v4/expeditions.html.

    python3 tools/v4_expeditions_final.py
"""
import os
import runpy

runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "v4_expeditions.py"), run_name="__main__")
