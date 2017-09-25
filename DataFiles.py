#!/usr/bin/python3
import os, subprocess

class DataFiles():
    def __init__(self, path):
        self.checksums = {}
        self.path  = path
    
    def accessPath(self):
        if os.getcwd() != self.path:
            try:
                os.chdir(self.path)
            except FileNotFoundError:
                print("Directory {} is not accessible!".format(self.path))

    def listFiles(self):
        self.checksums = {f:"" for f in os.listdir(self.path)} 
        return self.checksums

        
    def computeChecksums(self):
        currentDir = os.getcwd()
        self.accessPath()
        for f in self.listFiles():
            checksum, file = subprocess.check_output(["md5sum",f]).decode("utf-8").split()
            self.checksums[file] = checksum
        os.chdir(currentDir)    
    
