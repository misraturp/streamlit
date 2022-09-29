#!/usr/bin/env python

# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Translates the GH Actions matrix into file names to pass to run_e2e_tests.py"""
import math
import os
import sys

# Directory for cypress test specs
CYPRESS_DIR = "e2e/specs"


def create_file_list():
    """Create the list of files for a given matrix input"""

    spec_dir = os.path.abspath(CYPRESS_DIR)
    sorted_files = sorted(os.listdir(spec_dir))
    # ultimately need the files in e2e/specs/<file_name>.js format to run tests
    all_files = [os.path.join(CYPRESS_DIR, file_name) for file_name in sorted_files]
    file_count = len(all_files)

    # calculate how many specs in each run
    total_runs = int(sys.argv[1])
    current_run = int(sys.argv[2])

    raw_interval = (file_count + total_runs - 1) / total_runs
    interval = math.ceil(raw_interval)

    # calculate the start & stop index for current run
    start_index = (current_run - 1) * interval
    stop_index = start_index + interval

    current_files = all_files[start_index:stop_index]

    file_list = " ".join(current_files)

    return current_files


def main():
    """Run main loop."""

    files = create_file_list()
    print(files)


if __name__ == "__main__":
    main()
