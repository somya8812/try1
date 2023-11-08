*** Settings ***
Documentation    Create the Log File of CLI Console Logs in .txt Format and Parse in to JSON File with SSH.

Library    ParseInJsonV1.py
Library    SSHLibrary
Library    BuiltIn
Library    String
Library    OperatingSystem
Variables  config.yaml

*** Variables ***
${config_file_path}=    ${EXECDIR}

*** Keywords ***
Create .txt file of modules version from CLI with SSH
    [Documentation]    This keyword is using for login to remote machine with SSH, login as a defined user,
    ...    Validate user, Validate Directory and binary file of CLI, Run the CLI on remote machine for version check
    ...    and create log file with "extractVersionsInput.txt" name.
    ...    It takes Three arguments 1.Server Ip, 2.UserName, 3.Password.  
    
    [Arguments]          ${server_ip}    ${UserName}    ${Password}    ${clilogfile}
    ssh login    ${server_ip}    ${UserName}    ${Password}
    Sleep    .3
    ${commandforchangeuser}=    Catenate    ${SSH_Variables.Command_For_ChangeUser}    ${SSH_Variables.UserName}    
    # Login As User In ssh    ${commandforchangeuser}    ${SSH_Variables.CLIUserName}    ${SSH_Variables.Password}  
    # Login As User In ssh    ${SSH_Variables.Command_For_ChangeUser}    ${SSH_Variables.CLIUserName}    ${SSH_Variables.Password}
    
    # commented below 2 lines for dev2
    ## Check Directory is Exist Or Not    ${SSH_Variables.CLI_Directory}  
    ## Check Binary File is Exist or Not    ${SSH_Variables.CLI_Binary_Path}
    Change Directory For Run CLI    ${SSH_Variables.Path_Of_CLI_Directory}
    Write Command With SSH    ${SSH_Variables.CLI_Run_Command}
    Sleep    1s
    Write Command With SSH    nand.kishor@amantyatech.com
    Sleep    1s
    Write Command With SSH    Nandk@8468
    Sleep    1s
    ${data}=    Read Output Of Command with SSH
    Sleep    5s
    Write Command With SSH    ${SSH_Variables.Modules_Version_Check_Command}
    Sleep    1s
    Write Command With SSH    sys
    Sleep    1s
    Write Command With SSH    ${SSH_Variables.Modules_Version_Check_Command}
    # ${data}=    Read Output Of Command with SSH
    Log To Console    ${data}
    # Sleep    10s
    Write Command With SSH    datacomplete
    ${data1}=    Read Until Regexp    Invalid command:
    # ${data1}=    Read Output Of Command with SSH
    Create File  ${clilogfile}    ${data1}    encoding=UTF-8
    Close All Connections
    Sleep    1s
    
    
Core Version
    Sleep    2s
    [Arguments]          ${Core_IP}    ${User_Name}    ${Core_Password}    ${Env}
    ssh login    ${Core_IP}    ${Core_Password}    ${User_Name}
    Sleep    .3
    Login As User In ssh    ${Core_SSH_Variables.Command_For_ChangeUser}    ${User_Name}    ${Core_Password}
    # Check Directory is Exist Or Not    ${Core_SSH_Variables.CLI_Directory}  
    # Check Binary File is Exist or Not    ${SSH_Variables.CLI_Binary_Path}
    # Change Directory For Run CLI    ${SSH_Variables.Path_Of_CLI_Directory}
    Write Command With SSH    cd cluster
    ${podsourcecommand}=    Catenate    SEPARATOR=    source np2-       ${Env}    .sh
    # Write Command With SSH    source np2-qa.sh
    Write Command With SSH    ${podsourcecommand}
    # Read Until    Switched to context
    ${podcommand}=    Catenate    SEPARATOR=    kubectl describe pods -n np2-    ${Env}
    # Write Command With SSH    kubectl describe pods np2-qa-core
    Write Command With SSH    ${podcommand}
    ${podslog}=    Read    delay=4s
    ${corelogfile}=    Catenate    ${EXECDIR}/${Env}coreversion.txt
    # ${corelogfile}=    ${EXECDIR}/${corelogfilename}
    Create File  ${corelogfile}    ${podslog}    encoding=UTF-8
    # ${corelogfile}=    Catenate    ${Env}    coreversion.txt
    ${coremoduledict}=    getversioncore    ${corelogfile} 
    # Create File  corepodslog.txt    ${podslog}    encoding=UTF-8
    # ${coremoduledict}=    getversioncore    corepodslog.txt 
    Log To Console    ${coremoduledict}
    [Return]    ${coremoduledict}   

ssh login
    [Documentation]    This keyword takes three arguments Server Ip, UserName, Password. This is Used for login remote machine with SSH.  
    [Arguments]          ${server_ip1}    ${UserName1}    ${Password1}
    Open Connection    ${server_ip1}
    Login                ${UserName1}    ${Password1}    allow_agent=False    look_for_keys=False
    Set Client Configuration    timeout=2 min

Login As User In ssh
    [Documentation]    With the help of this keyword  we login remote machine as user like root , vzqa etc. after this its validate the user also after login.
    ...    It takes two arguments 1.UserName, 2. Command for validate user
    
    [Arguments]          ${command for enter as user}    ${UserName}     ${Password}
    Write Command With SSH   ${command for enter as user}
    Log To Console    ${command for enter as user}
    ${userdata}=  Read Output Of Command with SSH
    Log To Console    ${userdata}
    ${userdata1}    Set Variable    ${userdata}
    ${ad}=    Run Keyword And Return Status    Should Contain    ${userdata1}    Password:
    
    IF    $ad    
        Write Command With SSH   ${Password}
    END  
    # Write Command With SSH    ${command for validate user}
    # Log To Console   ${command for validate user} 
    ## ${output of whoami }=    Read Until Regexp    ${SSH_Variables.CLIUserName} 
    # ${output of whoami }=    Read    delay=3s
    # Log To Console    ${output of whoami }
    # Should Contain    ${output of whoami }    ${UserName}    You login As ${output of whoami } user but in config file you set CLIuser as ${UserName}    values=${False}

Write Command With SSH
    [Documentation]    This Keyword is using for write any command on remote machine console with SSh.
    ...    It takes One argument 1.Command
    
    [Arguments]          ${command}
    Write   ${command}
    Sleep    .1s
Read Output Of Command with SSH
    [Documentation]    This Keyword is using for read the any command output or console log of remote machine with SSH.
    ${output}=    Read    delay=.2s
    [Return]    ${output} 
Validate command output
    [Documentation]    This Keyword is a combination of "Write Command With SSH" and "Read Output Of Command with SSH" keywords.
    ...    after write any command on remote machine's console its read the output of that command and search expected keyword or string in ouput of the command.
    ...    If expected keyword or string found in output its return TRUE.
    ...    It takes two arguments 1. command ,2. Expected output or keyword .    
    
    [Arguments]          ${command for validation}    ${Expected Output}
    Write Command With SSH    ${command for validation}
    ${data}=    Read Output Of Command with SSH
    Should Contain    ${data}    ${Expected Output}    Log of command ${command for validation}

Check Binary File is Exist or Not
    [Documentation]    This Keyword is using for check file is exists or not in remote machine. If exists its return True.
    ...    It takes One argument 1.Path of the File
    
    [Arguments]    ${CLI Binary Path}
    SSHLibrary.File Should Exist    ${CLI Binary Path}

Check Directory is Exist Or Not
    [Documentation]    This Keyword is using for directory is exists or not in remote machine. If exists its return True.
    ...    It takes One argument 1.Path of the directory.
    [Arguments]    ${CLI Directory}
    
    SSHLibrary.Directory Should Exist    ${CLI Directory}

Change Directory For Run CLI
    [Documentation]    This Keyword is using change the directory on remote machine. Its Validate also Directory is changed or not.
    ...    If directory changed it returns True
    ...    It takes One argument 1.Path of the Directory.
    [Arguments]    ${Path Of CLI Directory}
    
    Write Command With SSH    ${Path Of CLI Directory}
    # Write Command With SSH    pwd
    # ${outofcommand}=    Read Output Of Command with SSH
    # Should Contain    ${outofcommand}    ${SSH_Variables.CLI_Directory}    Present working directory ${outofcommand} and changed directory ${SSH_Variables.CLI_Directory} are different or not able to change ${SSH_Variables.CLI_Directory} directory    values=${False}

Convert From Txt To JSON
    [Documentation]    This Keyword is using for Parse data and convert from txt to JSON. Create JSON file with name "VersionsOutput.JSON" in current directory.
    ...    It is a Userdefined Keyword.
    ...    It takes Five argument 1.Env Name., 2.HostName, 3.UserName, 4.Input Log File Path, 5.Output Json file Path
    
    [Arguments]          ${EnvName}    ${HostName}    ${UserName}    ${input_text_file_path}    ${output_Json_file_path}    ${coremoduledict}
    # ${LogFilePathAfterRemovingExtraData}=    Catenate    ${EnvName}    FilteredCliLog.txt 
    ${LogFilePathAfterRemovingExtraData}=    Catenate    ${EXECDIR}/${EnvName}FilteredCliLog.txt
    # ${LogFilePathAfterRemovingExtraData}=    ${EXECDIR}/${LogFilePathAfterRemovingExtraDataPath}
    
    IF    ${coremoduledict} == {}
        Log To Console    Actual data : ${coremoduledict} No data found from "Kubectl describe pods" command 
        Fail    *HTML*    Actual data : ${coremoduledict} No data found from "Kubectl describe pods" command
    ELSE
        ${PassFailStatus}=    parseInjson          ${EnvName}    ${HostName}    ${UserName}    ${config_file_path}    ${input_text_file_path}    ${coremoduledict}    ${LogFilePathAfterRemovingExtraData}    ${output_Json_file_path}
        ${ValidatePassFailStatus}=    Run Keyword And Return Status    Should Contain    ${PassFailStatus}    1
        IF   ${ValidatePassFailStatus}==False
            Fail    *HTML*${PassFailStatus}   
        END
        
    END  
    # ${PassFailStatus}=    parseInjson          ${EnvName}    ${HostName}    ${UserName}    ${input_text_file_path}    ${coremoduledict}    ${output_Json_file_path}
    # ${ValidatePassFailStatus}=    Run Keyword And Return Status    Should Contain    ${PassFailStatus}    1
    # IF   ${ValidatePassFailStatus}==False
    #     Fail    *HTML*${PassFailStatus}   
    # END


Create CLI LOG File Of Modules Version
    [Documentation]    This Keyword is using for Capture Version of Modules From CLI and Create 
    ...    .txt file name as "ModulesVersion.txt in current directory".
    ...    It takes Three arguments 1.Server IP, 2.UserName, 3.Password.
    
    [Arguments]          ${server_ip}    ${UserName}    ${Password}
    ssh login    ${server_ip}    ${UserName}    ${Password}
    Change Directory For Run CLI    ${SSH_Variables.Path_Of_CLI_Directory}
    Write Command With SSH    ${SSH_Variables.CLI_Run_Command}
    Write Command With SSH    ${SSH_Variables.Modules_Version_Check_Command}
    Write Command With SSH    sys
    Write Command With SSH    ${SSH_Variables.Modules_Version_Check_Command}
    Write Command With SSH    q
    ${data1}=    Read Until Regexp    /home/stackuser$ 
    ${DataAfterRemovingExtraValues}=    Remove String    ${data1}    [m    [1m    [m    [4m
    Create File  /robot/results/ModulesVersion.txt    ${DataAfterRemovingExtraValues}    encoding=UTF-8
    Sleep    .3s
    Close All Connections