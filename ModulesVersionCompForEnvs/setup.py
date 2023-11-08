
import yaml
import robot
import os
import getpass
import json
from prettytable import PrettyTable
from robot.api.deco import library, keyword
import os
import yaml
import paramiko
import time
import csv

from robot.libraries.BuiltIn import BuiltIn


# @library
# class setup:
#     @keyword   
def getdatafromjsonfile(jsonfilename):
    alljsondata=[]
    for j,i in enumerate(jsonfilename):
        openas="f"+str(j)
        filename="file"+str(j)
        # print(openas)
        with open(i, "r") as openas:
            
            filename = json.loads(openas.read())
        alljsondata.append(filename)

    findallenvname(alljsondata)

    
    


    
def allmodulesforcore(envnamelist,alljsondata):
     allmodulelist=[]
     for data in alljsondata:
          allmodules=list(data["modules"]["Cores"][0]["CORE_1_Amantya"].keys())
          allmodulelist+=allmodules
     allmodulelist=set(allmodulelist)
     allmodulelist.discard("OBR_USERNAME")
     allmodulelist.discard("OBR_HOST")
     return allmodulelist
def corecomparision(envnamelist,alljsondata,allmodulelist):
    envnamelist.insert(0,"Modules")
    t = PrettyTable(envnamelist)
    t.align = 'l'
    t.max_width = 20
    t.max_width['Title'] = t.max_width['Link'] = 60
    t.align['#User Comments'] = 'r'
    
    for modules in allmodulelist:
        newdata=[]
        for envname in envnamelist:
            for data in alljsondata:
                envnameinjson=list(data["modules"]["CLIs"][0].keys())
                if envname in envnameinjson:
                        # if modules=="OBR_USERNAME" or modules=="OBR_HOST":
                        #     pass
                        # else:
                            if modules in list(data["modules"]["Cores"][0]["CORE_1_Amantya"].keys()):
                                print(modules,data["modules"]["Cores"][0]["CORE_1_Amantya"][modules])
                                if modules in newdata:
                                    newdata.append(data["modules"]["Cores"][0]["CORE_1_Amantya"][modules])
                                else:
                                    newdata.append(modules)
                                    newdata.append(data["modules"]["Cores"][0]["CORE_1_Amantya"][modules])
                            else:
                                if modules in newdata:
                                    newdata.append("modules not found")
                                else:
                                    newdata.append(modules)
                                    newdata.append("modules not found")
        print("new data : ",newdata)
        t.add_row(newdata)

    # print(t)
    return t
                             
                        
               
     
     

def findallenvname(alljsondata):
    keysforallenv=[]
    envnamelist=[]
    for i in alljsondata:
        # clprint(i)
        env=list(i["modules"]["CLIs"][0].keys())
        
        envnamelist.append(env[0])
        keyss=list(i["modules"]["CLIs"][0][env[0]].keys())
        # print("env :",keyss)
        keysforallenv+=keyss
    keysforallenv=set(keysforallenv)
    # print("env :",keysforallenv)
    findallvaluesfromjson(alljsondata,keysforallenv,envnamelist)

def findallvaluesfromjson(alljsondata,keysforallenv,envnamelist):
    a=allmodulesforcore(envnamelist,alljsondata)
    
    t=corecomparision(envnamelist,alljsondata,a)
    # input()
    
    envdata={}
    for envname in envnamelist:
        envdata[envname]=[]
    # print(envdata)
    # input()
    for modules in keysforallenv:
        # print(i)
        for env in envnamelist:
            for k in alljsondata:
                if k["modules"]["CLIs"][0].get(env,"None")!="None":
                    if modules=="OBR_USERNAME" or modules=="OBR_HOST":
                        pass
                    else:
                        if modules in k["modules"]["CLIs"][0][env].keys():
                            # print(j,i,k["modules"]["CLIs"][0][j][i]["app_version"],"found")
                            envdata[env]+=[[modules,k["modules"]["CLIs"][0][env][modules]["app_version"]]]
                            break
                        else:
                            print(modules,env,"not found")
                            break


    # print(envdata)
    createtable(envdata,envnamelist,keysforallenv,t)


    
def createtable(envdata,envnamelist,keysforallenv,t):
        
        newdata1=[]
        # envnamelist.insert(0,"Modules")
        # print("EEENVVVVVVVVVVV",envnamelist)
        # t = PrettyTable(envnamelist)
        # t.align = 'l'
        # t.max_width = 20
        # t.max_width['Title'] = t.max_width['Link'] = 60
        # t.align['#User Comments'] = 'r'
        # print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
        for modules in keysforallenv:
            # print("\n\n modulesssssssssssssssssssss:",modules,"\n\n")
            if modules=="OBR_USERNAME" or modules=="OBR_HOST":
                        pass
            else:
                newdata=[]
                for env in envnamelist[1:len(envnamelist)]:
                    # print("envnamelist[1:len(envnamelist)] ",envnamelist[1:len(envnamelist)])
                    print("\n Searching "+modules+ " in " +env,"Environment")
                    modulefound=True
                    for moduleswithversion in envdata[env]:
                        # print("\n\n moduleswithversionnnnnnnn : ",moduleswithversion,"\n\n")
                        if modules in moduleswithversion:
                            print(modules+"  Found in "+env)
                            # print("\n\n modulessssss",modules,"\n\n")
                            modulefound=False
                            print("data list",newdata)
                            if modules in newdata:
                                newdata.append(moduleswithversion[1])
                                break
                            else:
                                newdata.append(modules)
                                newdata.append(moduleswithversion[1])
                                break
                
                    if modulefound==True:
                        print(modules+" Not Found in given env......")
                        # print("newtata0000",newdata)
                        if modules in newdata:
                                newdata.append("module not found in "+env)
                                
                        else:
                            # print("ooooooooooooo")
                            newdata.append(modules)
                            newdata.append("module not found in "+env)
                    print("Updated list : ",newdata)
                # print("new data2 : ",newdata)
                t.add_row(newdata)
                # newdata1.append(newdata)
        print(t)
        f = open("ModulesVerionInTabular.txt", "w")
        f.write(str(t))
        # return t
    
    
def Create_CSV_file(jsonfile):
    allenvdata=[]
    for i in jsonfile:
          with open(i, "r") as filename:
            Jsondata1=json.load(filename)
            allenvdata.append(Jsondata1)
    ExtractmodulesfromJsonaslist(allenvdata)
def ExtractmodulesfromJsonaslist(allenvdata):
            allenvmodulesdata=[]
            envname="qa"
            for env in allenvdata:
                
                for i,j in env.items():
                    # print(j["Cores"][0]["CORE_1_Amantya"])
                    for modules,version in j["Cores"][0]["CORE_1_Amantya"].items():
                       allenvmodulesdata.append(modules)
            # print(set(allenvmodulesdata))
            searchmodulesinenvs(allenvmodulesdata,allenvdata)

def searchmodulesinenvs(allenvmodulesdata,allenvdata):
     fields=["Modules","qa1","qa2"]
     
     rows=[]
     
     for k in set(allenvmodulesdata):
        versiondata=[]
        versiondata.append(k)
        for env in allenvdata:

            for i,j in env.items():
                        # print(j["Cores"][0]["CORE_1_Amantya"])
                        
                            if k in j["Cores"][0]["CORE_1_Amantya"]:
                                print(k,j["Cores"][0]["CORE_1_Amantya"][k])
                                versiondata.append(j["Cores"][0]["CORE_1_Amantya"][k])
                                
                            else:
                                print("module not found")
                                versiondata.append("module not found")
        rows.append(versiondata)                      
          
     filename = "university_records.csv"
     with open(filename, 'w') as csvfile:  
      
        csvwriter = csv.writer(csvfile)  
            
        
        csvwriter.writerow(fields)  
            
        csvwriter.writerows(rows) 
     

Create_CSV_file(["qaVersionsOutput.json","qa2VersionsOutput.json"])