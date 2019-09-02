#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import configparser
import os

root = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    mdfilename = os.path.join(root, "../SUPPORTED_APPLICATIONS.md")
    with open(mdfilename, "w+") as mdfile:
        applications = sorted(glob.glob("applications/*cfg"))
        mdfile.write("# Supported Applications ({})\n\n".format(len(applications)))
        for cfg_file in applications:
            # https://stackoverflow.com/a/52306763
            config = configparser.ConfigParser(
                comment_prefixes="/", allow_no_value=True
            )
            config.optionxform = str
            config.read(cfg_file)
            mdfile.write(
                "- [{}]({})\n".format(
                    config["application"]["name"], config["application"]["homepage"]
                )
            )
