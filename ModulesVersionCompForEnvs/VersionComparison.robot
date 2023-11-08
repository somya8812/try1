*** Settings ***
Documentation    Modules Version In Json Format
Library         Collections
Resource    resource.robot
Library    BuiltIn
Library    OperatingSystem
Library    String
Library    setup.py
Variables    userinput.yaml
Variables   config.yaml
# Variables    userinput.yaml

*** Variables ***
@{jsonfilenamelist}    

*** Test Cases ***
Extract Modules Version From CLI And Convert In JSON
    Version_Comparision_Of_Modules_For_Envs
    
    
        



*** Keywords ***

Version_Comparision_Of_Modules_For_Envs
    FOR     ${sutdetails}     IN     @{SUT_INPUT}
                # Set Log Level    NONE
                # ${subsytem_dict}=  get from dictionary  ${data}  ${key_1}
                ${SUT_IP}=     Evaluate  ${sutdetails}.get("Sut_IP","SUT_IP NOT FOUND")
                # ${SUT_User_Name}=    Evaluate  ${sutdetails}.get("SUT_User_Name","SUT_User_Name NOT FOUND")
                ${Core_IP}=     Evaluate  ${sutdetails}.get("Core_IP","Core_IP NOT FOUND")
               
                ${User_Name}=    Evaluate  ${sutdetails}.get("User_Name","User_Name NOT FOUND")
                ${Password}=     Evaluate  ${sutdetails}.get("Password","SUT_Password NOT FOUND")
                # ${Core_Password}=     Evaluate  ${sutdetails}.get("Core_Password","Core_Password NOT FOUND")
                
                ${Env}=     Evaluate  ${sutdetails}.get("Env","Env Name NOT FOUND")
                # ${SUT_Env}=     Evaluate  ${sutdetails}.get("SUT_Env","SUT_Env Name NOT FOUND")
                # Log To Console   ${Env}
                # Set Log Level    INFO
                ${clilogfile}=    Catenate    ${EXECDIR}/${Env}extractVersionsInput.txt
                # ${clilogfile}=    ${EXECDIR}/${clilogfilepath}
                Create .txt file of modules version from CLI with SSH    ${SUT_IP}    ${User_Name}    ${Password}    ${clilogfile}
                ${Core_data}=    Core Version    ${Core_IP}    ${Password}    ${User_Name}    ${Env}
                ${jsonfilename}=    Catenate    ${EXECDIR}/${Env}VersionsOutput.json  
                # ${jsonfilename}=    ${EXECDIR}/${jsonfilenamePath} 
                Convert From Txt To JSON    ${Env}    ${SUT_IP}    ${User_Name}    ${clilogfile}    ${jsonfilename}    ${Core_data}
                
                Append To List    ${jsonfilenamelist}    ${jsonfilename}      
        END
        Log To Console    @{jsonfilenamelist}   
        getdatafromjsonfile    ${jsonfilenamelist} 
    