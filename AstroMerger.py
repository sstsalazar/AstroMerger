#! /usr/bin/python3
import os, shutil, json, time,sys
from  DataFiles import DataFiles

class AstroMerger():
    def __init__(self,origin, destination):
        self.origin      = DataFiles(origin)
        self.destination = DataFiles(destination)
        self.changes = []
        self.move = []
        self.origin.computeChecksums()
        self.destination.computeChecksums()
    
    #def compareFiles(self):
        #o = self.origin.checksums
        #d = self.destination.checksums
        #for file in o.keys():
            #if file not in d:
                #self.newFiles.append(file)
            #else:
                #if o[file] != d[file]:
                    #self.newVersions.append(file)
    
    
    def compareFiles(self):
        o = self.origin.checksums
        d = self.destination.checksums
        oldVersions = self.destination.checksums.keys()
        for file in o.keys():
            if file not in d or  o[file] != d[file]:
                    self.move.append(file)
                    entry = {"Date": time.asctime( time.localtime(time.time()) ) }
                    entry["File"] = file
                    if file in oldVersions:
                        entry["Status"] = "ALTERED"
                    else:
                        entry["Status"] = "NEW"
                    self.changes.append(entry)
                    
    def migrateFiles(self):
        currentDir = os.getcwd()
        self.origin.accessPath
        oldVersions = self.destination.checksums.keys()
        self.origin.accessPath()
        for f in os.listdir("."):
            if f in self.move:
                shutil.copy(f, self.destination.path)
            os.remove(f)
        os.chdir(currentDir)
                
                
    def registerChanges(self, logname="log.json"):
        with open(logname, 'w') as f:
            json.dump(self.changes, f, sort_keys=True,indent=4, ensure_ascii=False)


if __name__=="__main__":
    if len(sys.argv) != 2:
        print("It's necessary to pass a single JSON configuration file.")
        sys.exit(-1)
    with open( sys.argv[-1] ) as configFile:
        config = json.load(configFile)
        for d in config["directories"]:
            am = AstroMerger( d["input"], d["output"])
            am.compareFiles()
            am.migrateFiles()
            am.registerChanges("{}-{}.json".format(config["source"]["name"], time.strftime("%Y%m%d", time.localtime())))
