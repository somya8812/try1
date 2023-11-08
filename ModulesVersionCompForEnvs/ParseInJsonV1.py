
#Objective : With ParseInJson(a) function we convert log.txt in to predefined JSON format.
  # step 1
    # First we open log.txt file after that we extract require data on the basis of uppercase substring.
  # step 2
    # We write uppercase string in to new file.
  # step 3 
    # We open new file and remove extra line on the basis of "NAME AND HOST" keyword.
    # We split remaining data on the basis of space.
    # We update splited data into the Json_format(predefined format) as per the requirement
# from ctypes import LibraryLoader
# import keyword
# from robot.api.deco import library, keyword
from robot.api.deco import library, keyword
import json
import yaml
import os
import datetime
from robot.libraries.BuiltIn import BuiltIn
@library
class ParseInJsonV1:
    
    @keyword
    def parseInjson(self,environmentname,hostname,usrname,config_file_path,input_text_file,coredict,LogFilePathAfterRemovingExtraData,OutputJsonfilePath="file not pass"):
        envstatus=0
        newkeylist=[]
        oldkeylist=[]
        filexist=0
        Keyword_status="0"
        ErrorMessage="Error Message : "
        # jsonformat={"modules":{"Cores":[{}],"CLIs":[{}]}}
        
        try:
            conf_file_path=config_file_path+"/config.yaml"
            print("Config file path: ",conf_file_path)
            with open(conf_file_path) as f:
                config=yaml.load(f, Loader=yaml.FullLoader)
            # LogFilePathAfterRemovingExtraData=config["LogFilePathAfterRemovingExtraData"]

            if os.path.exists(OutputJsonfilePath):
                filexist=1
                os.remove(OutputJsonfilePath)
            #     with open(OutputJsonfilePath,"r") as f3:
            #         ouputfile=json.loads(f3.read())
            #         CLIEnv=list(ouputfile["modules"]["CLIs"][0].keys())
            #         # print("start......",CLIEnv,"end........\n")
            #     f3.close()
            #     if environmentname in CLIEnv:
            #         envstatus=1
            #         oldkeylist.append(list(ouputfile["modules"]["CLIs"][0][environmentname].keys()))
            #         print(oldkeylist)
          
            #     else:
            #         ouputfile["modules"]["CLIs"][0][environmentname]={"OBR_HOST":hostname,"OBR_USERNAME":usrname}
            #         print("This env not found in previous versionoutput.json")
            # else:
            CORE_OBR_HOST=config["Core_SSH_Variables"]["ServerIP"]
            CORE_OBR_USERNAME=config["Core_SSH_Variables"]["UserName"]
            ouputfile={"modules":{"Cores":[{"CORE_1_Amantya":{"OBR_HOST":CORE_OBR_HOST,"OBR_USERNAME":CORE_OBR_USERNAME}}],"CLIs":[{environmentname:{"OBR_HOST":hostname,"OBR_USERNAME":usrname}}]}}
        
            
            # with open("config.yaml") as f:
            #     config=yaml.load(f, Loader=yaml.FullLoader)
            # LogFilePathAfterRemovingExtraData=config["LogFilePathAfterRemovingExtraData"]

            
            
            related_data=""
            createjsonfile={"modules":{"Cores":[{}],"CLIs":[{environmentname:{"OBR_HOST":hostname,"OBR_USERNAME":usrname}}]}}
            if os.path.exists(input_text_file):
                file=input_text_file 
                ty=2
                # with open("input12.txt","w+") as files:
                with open(file,"r") as f:
                    for i,k in enumerate(f):
                        j=k.replace("[m","").replace("[1m","").replace("[m","").replace("[4m","")
                        # files.write(j)
                        data11="NUM  NAME               HOST                    CNTLR VERSION  APP VERSION"
                        data21="NAME               HOST                   VERSION"
                        start_point=j[:15]
                        uppercase=start_point.isupper()
                        if data11 in j or data21 in j:
                            ty=1
                            related_data+=j
                        
                        elif "------------" in j or len(j)==1 or "datacomplete" in j:
                            pass
                        elif uppercase==False:
                            ty=0
                        elif ty==1:
                            start_point1=j[:15]
                            if start_point1.isupper():
                                    related_data+=j
                
            else:
                print("input logfile not present at given path")
                ErrorMessage+="input logfile not present at given path"
                return ErrorMessage
            date_time=str(datetime.datetime.now())
            with open(LogFilePathAfterRemovingExtraData,"w") as f1:
                for i in related_data:
                    f1.write(i)
            f1.close()
            
            
            with open(LogFilePathAfterRemovingExtraData,"r") as f2:
                for line in f2:
                    # table = pd.DataFrame(columns = ['category', 'model','price'])
                    if len(line.strip())>1:
                        parse_data=line.strip().split()
                        if "NAME" and "HOST" in line:
                            continue
                        else:
                            print(parse_data)
                            if parse_data[0].isnumeric():
                                if "::" or "--" in parse_data:
                                    ouputfile["modules"]["CLIs"][0][environmentname][parse_data[1]]={"OBR_HOST": parse_data[2].split(":")[0],"app_version": " ".join(parse_data[4:len(parse_data)+1]),"ctlr_version": parse_data[3]}
                                else:
                                    ouputfile["modules"]["CLIs"][0][environmentname][parse_data[1]]={"OBR_HOST": parse_data[2].split(":")[0],"app_version": parse_data[4],"ctlr_version": parse_data[3]}
                                # ouputfile["modules"]["CLIs"][0][environmentname][parse_data[1]]={"OBR_HOST": parse_data[2].split(":")[0],"app_version": parse_data[4],"ctlr_version": parse_data[3]}
                                newkeylist.append(parse_data[1])
                        
                            else:
                                ouputfile["modules"]["CLIs"][0][environmentname][parse_data[0]]={"app_version": parse_data[2]}
                                newkeylist.append(parse_data[0])

            if envstatus==1:
                # print(oldkeylist,newkeylist)
                extradatafrompreviousfile=list(set(oldkeylist[0])-set(newkeylist))
                # print(extradatafrompreviousfile)
                if 'OBR_USERNAME' in extradatafrompreviousfile:
                    extradatafrompreviousfile.remove('OBR_USERNAME')
                elif 'OBR_HOST' in extradatafrompreviousfile:
                    extradatafrompreviousfile.remove('OBR_HOST')
                # print("new key",extradatafrompreviousfile,"\n\n") 
                for i in extradatafrompreviousfile:
                        del ouputfile["modules"]["CLIs"][0][environmentname][i]        
            
            for module,version in coredict.items():
                ouputfile["modules"]["Cores"][0]["CORE_1_Amantya"][module]=version
            
            outputjsonfile = json.dumps(ouputfile, indent=2)
            print(outputjsonfile)
            if OutputJsonfilePath=="file not pass":
                OutputJsonfilePath="VersionsOutput.json"
                with open(OutputJsonfilePath, "w") as outfile:
                
                    outfile.write(outputjsonfile)
                    Keyword_status="1"
                    return Keyword_status
            else:

                with open(OutputJsonfilePath, "w") as outfile:
                
                    outfile.write(outputjsonfile)
                    Keyword_status="1"
                    return  Keyword_status
           
            
        except Exception as error:
            print("\n\nError : ",error,"\n\n")
            ErrorMessage+=error
        return  ErrorMessage
    
    @keyword
    def getversioncore(self,logfile):
        try:
            coremoduledict={}
            modules=["AMF","SMF","UPF","AUSF","NRF","UDM","UDR","PCF"]
            with open(logfile) as f:
                
                    for i in f:
                        if "Image:" in i:
                            for j in modules:
                                if j in coremoduledict:
                                    continue
                                modulename="/"+j.lower()+":"
                                if modulename in i:
                                    print(i)
                                    version=i.split(modulename)
                                    version=version[len(version)-1]
                                    print(modulename,version)
                                    coremoduledict[str(j)+"_Version"]=version.strip()
                                    print(coremoduledict)
                                    break
        except Exception as error:
            print("Error from getversioncore func",error)
        print("core modele dict : ",coremoduledict)
        return coremoduledict


# ob=ParseInJson(json_format)
# print(json_format)






















































# with open("/home/amantya/Downloads/VersionsExtractorWorkPackage/extractVersionsInput.txt","r") as f:
#     # Skips text before the beginning of the interesting block:
#     lines = f.readlines()
    
# with open("/home/amantya/Downloads/VersionsExtractorWorkPackage/extractVersionsInput.txt","w") as input_data:
#     for line in lines:
#         a=line.isupper()
#         if  a==True:
#             input_data.write(line)

# # f.close()
# with open("/home/amantya/Downloads/VersionsExtractorWorkPackage/extractVersionsInput.txt", "r") as f:
#     print(f)
