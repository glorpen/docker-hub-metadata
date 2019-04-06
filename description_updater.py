#!/usr/bin/env python3

"""
@author: Arkadiusz Dzięgiel <arkadiusz.dziegiel@glorpen.pl>
"""

import os
import sys
import json
import argparse
import requests
import subprocess

__version__ = "1.0.0"

class Updater(object):
    
    _headers = {
        "Content-Type": "application/json"
    }
    _host = "https://cloud.docker.com"
    
    def _req(self, method, url, data):
        response = getattr(requests, method)("%s/%s" % (_host, url), json.dumps(data), headers=self._headers)
        response.raise_for_status()
        return response.json()
    
    def login(self, username, password):
        response = self._req("post", "v2/users/login/", {
            "username": username,
            "password": password
        })
        self._headers["Authorization"] = "JWT %s" % response["token"]
    
    def logout(self):
        # not used, added for "api" completion
        del self._headers["Authorization"]
    
    def update_description(self, repository, description, full_description):
        data = {}
        
        if description is not None:
            data["description"] = description
        if full_description is not None:
            data["full_description"] = full_description
        
        self._req("patch", "v2/repositories/%s/" % repository, data)
    
    def convert_doc(self, source, args):
        if source.lower().endswith("md"):
            with open(source, "rt") as f:
                return f.read()
        
        my_args = ["pandoc", source, "-t", "markdown"]
        
        p = subprocess.Popen(my_args + args, stdout=subprocess.PIPE, stderr=sys.stderr)
        data = p.stdout.read().decode()
        if p.wait() != 0:
            raise Exception("Pandoc failed with %d" % p.returncode)
        
        return data

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        epilog="""
            Use "--" to add arguments to pandoc process, eg. changing output to 10 columns wide: %(prog)s -l README.rst -- --columns 10
        """,
        description="""
            Converts and sets repository description on Docker Hub.
        """
    )
    p.add_argument('--repository', '-r', default=os.environ.get("REPOSITORY"), help="repository name, eg. glorpen/hub-metadata", metavar="NAME")
    p.add_argument('--username', '-u', default=os.environ.get("USERNAME"), metavar="USER")
    p.add_argument('--password', '-p', default=os.environ.get("PASSWORD"), metavar="PASS")
    p.add_argument('--description', '-d', default=os.environ.get("DESCRIPTION"), metavar="DESC")
    p.add_argument('--long-description-file', '-l', default=os.environ.get("LONG_DESCRIPTION_FILE"), metavar="LONG_DESC", help="file with text to convert and send")
    p.add_argument('--print-only', action="store_true", default=False, help="generate and print text, do not send it to Docker Hub")
    
    try:
        args_split = sys.argv.index("--")
        pandoc_args = sys.argv[args_split+1:]
        my_args = sys.argv[1:args_split]
    except ValueError:
        pandoc_args = []
        my_args = sys.argv[1:]
    
    ns = p.parse_args(args=my_args)
    
    if ns.long_description_file is None and ns.description is None:
        p.error("No description nor long_description were provided.")
    
    if not ns.print_only:
        if ns.repository is None or ns.username is None or ns.password is None:
            p.error("Target repository, username or password were not provided.")
    
    u = Updater()
    
    if ns.long_description_file:
        long_description = u.convert_doc(ns.long_description_file, pandoc_args)
    else:
        long_description = None
    
    if ns.print_only:
        if ns.description is not None:
            print(ns.description)
        if long_description is not None:
            print(long_description)
    else:
        u.login(ns.username, ns.password)
        u.update_description(ns.repository, ns.description, long_description)
