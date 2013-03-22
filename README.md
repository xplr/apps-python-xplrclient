XPLR API client and command-line interface
=============

Python module and application, clients for the XPLR API

XPLR dedicated [app page](https://xplr.com/apps/apps-python-xplrclient).

Browse [all software from XPLR](https://xplr.com/apps).

Description
-----------

XPLR client module (xplr_client.py):

* High level integration of API

* Management on dataset for learning

* Use of configuration file for storing preferences

XPLR Command Line Interface (xplr_cli.py):

* Provide Unix-Style CLI for interacting with XPLR API


Licence
-------

This application is released under the MIT licence

> 
> Copyright (c) 2012-2013 Xplr Software Inc
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
> 


Prerequisites
-------------

- Get an XPLR account and API key on https://www.xplr.com


Usage
-----

### Configuration

xplr_client module provides a function to access a ini-like configuration file. The CLI uses the $HOME/.xplrclient file as a default configuration file.

When used, the configuration file must contain an [xplr] section, with host, port, key, application declarations

### XPLR client module

The basic usage for the XPLR client module in python (2.7) is to instanciate an XPLR object, providing general config parameters (host, port, api key, app), and use this object to call XPLR api methods. Otherwise stated, the parameters are the same as [XPLR API](https://xplr.com/base_api/) parameters. 

Basic usage for predict:

import xplr_client

# read config file, defaults to ~/.xplrclient, alternate can be passed as alternatfile parameter
config = xplr_client.Config()

# instanciate xplr client object
xplr=xplr_client.XPLR(config.get('key'), config.get('host'), port = int(config.get('port')))

# call rpediction on a text buffer :
prediction = xplr.predict_content(buffer)

# prediction is a python dict reflecting the structure of the XPLR JSON response



### XPLR Command line interface

The command line interface is based on the python client modul and provides an easy access to the XPLR API with command line and shell tools.

* Read configuration from ini file

* Read content from unix pipes

* Manage datasets

* Complete coverage of XPLR API

*Usage*

$xplr_cli.py -h

usage: xplr_cli.py [-h] [-v] [-q] [-C FILE] [-H HOST] [-P PORT] [-K KEY]
                   {info,model,predict,search,dataset,learn,recommend} ...

XPLR Command line client

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         display detailed connection messages
  -q, --quiet           do ,ot display foprmatted answers from XPLR
  -C FILE, --config FILE
                        alternative config file
  -H HOST, --host HOST  XPLR API host
  -P PORT, --port PORT  XPLR API port
  -K KEY, --key KEY     XPLR API key

XPLR commands:
  {info,model,predict,search,dataset,learn,recommend}
    info                Get server info
    model               Create and manage models
    predict             Perform predictions
    search              Search XPLR topics index
    dataset             Create and manage datasets
    learn               Learn
    recommend           Recommend



#### info command

see: https://xplr.com/base_api/method_info

$xplr_cli.py info -h
usage: xplr_cli.py info [-h]

optional arguments:
  -h, --help  show this help message and exit

#### model command

see: https://xplr.com/base_api/method_model

$xplr_cli.py model -h
usage: xplr_cli.py model [-h] {info,create,update,delete} ...

optional arguments:
  -h, --help            show this help message and exit

XPLR models subcommands:
  {info,create,update,delete}
    info                Get model info
    create              Create new model
    update              Update model
    delete              Delete model

#### predict command

see: https://xplr.com/base_api/method_predict

$xplr_cli.py predict -h
usage: xplr_cli.py predict [-h] [-u URL | -f FILE | -d DATASET] [--uri URI]
                           [-m MODEL] [--topics_limit TOPICS_LIMIT]
                           [--elements_limit ELEMENTS_LIMIT] [--qualifiers]
                           [--content_extraction] [--index] [--recurrent]
                           [--labels] [--words] [--return_content]
                           [--return_title] [--return_content_type]
                           [--return_image] [--return_description]
                           [--return_excerpts] [--return_url]
                           [--remote_user_agent REMOTE_USER_AGENT]
                           [--idx_fields [IDX_FIELDS [IDX_FIELDS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     predict from url
  -f FILE, --file FILE  predict from file
  -d DATASET, --dataset DATASET
                        predict from dataset
  --uri URI             uri for indexation
  -m MODEL, --model MODEL
                        prediction model
  --topics_limit TOPICS_LIMIT
                        Number of topics predicted
  --elements_limit ELEMENTS_LIMIT
                        Number of elements within each topic
  --qualifiers          Use qualifiers on topics
  --content_extraction  Try to extract text content
  --index               Shall the document(s) be indexed by xplr
  --recurrent           Forces the creation of a new entry in XPLR index
  --labels              Index and/or return topic labels
  --words               Index and/or return topic words
  --return_content      Index and/or return text content
  --return_title        Index and/or return document title
  --return_content_type
                        Index and/or return mime content-type
  --return_image        Index and/or return relevant image
  --return_description  Index and/or return description
  --return_excerpts     Index and/or return excepts
  --return_url          Return document real url
  --remote_user_agent REMOTE_USER_AGENT
                        User agent string to be used by XPLR to fetch
                        resources
  --idx_fields [IDX_FIELDS [IDX_FIELDS ...]]
                        Extra indexation fields (sequence -x field value)


#### search command

see: https://xplr.com/base_api/method_search

$xplr_cli.py search -h
usage: xplr_cli.py search [-h]

optional arguments:
  -h, --help  show this help message and exit

NOTE : not yet implemented

#### dataset command

Prepares local datasets to be learned by XPLR

$xplr_cli.py dataset -h
usage: xplr_cli.py dataset [-h] {info,add,delete} ...

optional arguments:
  -h, --help         show this help message and exit

XPLR dataset subcommands:
  {info,add,delete}
    info             Get dataset info
    info             Get dataset info
    add              add a document to dataset
    delete           Delete dataset

#### learn command

see: https://xplr.com/base_api/method_learn

$xplr_cli.py learn -h
usage: xplr_cli.py learn [-h] -m MODEL -d DATASET [-c CHUNK_SIZE] [-x]
                         [--remote_user_agent REMOTE_USER_AGENT]

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
  -d DATASET, --dataset DATASET
  -c CHUNK_SIZE, --chunk_size CHUNK_SIZE
  -x, --content_extraction
  --remote_user_agent REMOTE_USER_AGENT
                        User agent string to be used by XPLR to fetch
                        resources


#### recommend command

see: https://xplr.com/base_api/method_recommend

$xplr_cli.py recommend -h
usage: xplr_cli.py recommend [-h] [-a APP]
                             [--remote_user_agent REMOTE_USER_AGENT]

optional arguments:
  -h, --help            show this help message and exit
  -a APP , --app  APP 
  --remote_user_agent REMOTE_USER_AGENT
                        User agent string to be used by XPLR to fetch
                        resources
