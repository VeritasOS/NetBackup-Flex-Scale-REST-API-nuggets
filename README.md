# NetBackup-Flex-Scale-REST-API-nuggets
This repo will provide sample scripts to execute REST APIs on NetBackupFlexScale cluster

* [Disclaimer](#Disc)
* [Introduction](#intro)


<a name="Disc"></a>
## Disclaimer:

> These samples are only meant to be used as a reference. Please do not use these in production.


<a name="intro"></a>

## Introduction:

> Driver Node pre-requisites:

- Python version to be 3.6 or higher

- Python modules needed: urllib3, requests

- source env_config before running a script. Example : . env_config

    TestDriver script usage:

    >python3 <script_name>
    - Each script requires environment variables for execution.
    - Each script contains doc string at the begining of file, which mentions required enviroment variables for the script execution.
    - Please refer env_config file for sample inputs

- Please execute these scripts after NBFS cluster is configured.
