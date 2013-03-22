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
<pre>
import xplr_client

# read config file, defaults to ~/.xplrclient, alternate can be passed as alternatfile parameter
config = xplr_client.Config()

# instanciate xplr client object
xplr=xplr_client.XPLR(config.get('key'), config.get('host'), port = int(config.get('port')))

# call prediction on a text buffer :
prediction = xplr.predict_content(buffer)

# prediction is a python dict reflecting the structure of the XPLR JSON response
</pre>


### XPLR Command line interface

The command line interface is based on the python client modul and provides an easy access to the XPLR API with command line and shell tools.

* Read configuration from ini file
* Read content from unix pipes
* Manage datasets
* Complete coverage of XPLR API

*Usage*
<pre>
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
</pre>


#### info command

see: https://xplr.com/base_api/method_info

Usage
<pre>
$xplr_cli.py info -h
usage: xplr_cli.py info [-h]

optional arguments:
  -h, --help  show this help message and exit
</pre>

#### model command

see: https://xplr.com/base_api/method_model

Usage
<pre>
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
</pre>

#### predict command

see: https://xplr.com/base_api/method_predict

Usage
<pre>
$xplr_cli.py predict -h
usage: xplr_cli.py predict [-h] [-u URL | -f FILE] [--uri URI] [-m MODEL]
                           [--topics_limit TOPICS_LIMIT]
                           [--elements_limit ELEMENTS_LIMIT] [--qualifiers]
                           [--index] [--index_override] [--recurrent]
                           [--labels] [--words]
                           [--filters_in [FILTERS_IN [FILTERS_IN ...]]]
                           [--filters_out [FILTERS_OUT [FILTERS_OUT ...]]]
                           [--remote_user_agent REMOTE_USER_AGENT]
                           [--idx_fields [IDX_FIELDS [IDX_FIELDS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     predict from url
  -f FILE, --file FILE  predict from file
  --uri URI             uri for indexation
  -m MODEL, --model MODEL
                        prediction model
  --topics_limit TOPICS_LIMIT
                        Number of topics predicted
  --elements_limit ELEMENTS_LIMIT
                        Number of elements within each topic
  --qualifiers          Use qualifiers on topics
  --index               Shall the document(s) be indexed by xplr
  --index_override      Whether to override the current document when indexing
  --recurrent           Forces the creation of a new entry in XPLR index
  --labels              Index and/or return topic labels
  --words               Index and/or return topic words
  --filters_in [FILTERS_IN [FILTERS_IN ...]]
                        Preprocessing filters
  --filters_out [FILTERS_OUT [FILTERS_OUT ...]]
                        Postprocessing filters
  --remote_user_agent REMOTE_USER_AGENT
                        User agent string to be used by XPLR to fetch
                        resources
  --idx_fields [IDX_FIELDS [IDX_FIELDS ...]]
                        Extra indexation fields (sequence -x field value)

</pre>

#### search command

see: https://xplr.com/base_api/method_search

Usage
<pre>
$xplr_cli.py search -h
usage: xplr_cli.py search [-h] [-q QUERY] [--documents_limit DOCUMENTS_LIMIT]
                          [--document_topics_limit DOCUMENT_TOPICS_LIMIT]
                          [--found_topics_limit FOUND_TOPICS_LIMIT]
                          [--related_topics_limit RELATED_TOPICS_LIMIT]
                          [--elements_limit ELEMENTS_LIMIT] [--use_fields]
                          [--labels] [--words] [--exact_match]
                          [--date_from DATE_FROM] [--date_to DATE_TO]
                          [--extra_parameters EXTRA_PARAMETERS]

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Search query
  --documents_limit DOCUMENTS_LIMIT
                        Maximum number of documents expected
  --document_topics_limit DOCUMENT_TOPICS_LIMIT
                        Maximum number of topics expected per document
  --found_topics_limit FOUND_TOPICS_LIMIT
                        Maximum number of topics expected
  --related_topics_limit RELATED_TOPICS_LIMIT
                        Maximum number of related topics expected
  --elements_limit ELEMENTS_LIMIT
                        Number of elements within each topic
  --use_fields          shall the search be performed on extra index fields
  --labels              Shall XPLR show topic labels
  --words               Shall XPLR show topic words
  --exact_match         Shall the match be an exact label or word
  --date_from DATE_FROM
                        search in topics newer than
  --date_to DATE_TO     search in topics older than
  --extra_parameters EXTRA_PARAMETERS
                        appended to the query string to underlying search
                        system

</pre>

#### dataset command

Prepares local datasets to be learned by XPLR

Usage
<pre>
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
</pre>

#### learn command

see: https://xplr.com/base_api/method_learn

Usage
<pre>
$xplr_cli.py learn -h
usage: xplr_cli.py learn [-h] -m MODEL -d DATASET [-c CHUNK_SIZE]
                         [--filters_in [FILTERS_IN [FILTERS_IN ...]]]
                         [--remote_user_agent REMOTE_USER_AGENT]

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        selection of the model learned
  -d DATASET, --dataset DATASET
                        XPLRclient dataset
  -c CHUNK_SIZE, --chunk_size CHUNK_SIZE
                        number of document in the dataset sent for each learn
                        query
  --filters_in [FILTERS_IN [FILTERS_IN ...]]
                        preprocessing filters
  --remote_user_agent REMOTE_USER_AGENT
                        User agent string to be used by XPLR to fetch
                        resources
</pre>

#### recommend command

see: https://xplr.com/base_api/method_recommend

Usage
<pre>
$xplr_cli.py recommend -h
usage: xplr_cli.py recommend [-h] [-u URL | -f FILE] [-m MODEL]
                             [--documents_limit DOCUMENTS_LIMIT]
                             [--documents_topics_limit DOCUMENTS_TOPICS_LIMIT]
                             [--found_topics_limit FOUND_TOPICS_LIMIT]
                             [--related_topics_limit RELATED_TOPICS_LIMIT]
                             [--elements_limit ELEMENTS_LIMIT] [--qualifiers]
                             [--labels] [--words] [--date_from DATE_FROM]
                             [--date_to DATE_TO] [--in_index]
                             [--filters_in [FILTERS_IN [FILTERS_IN ...]]]
                             [--remote_user_agent REMOTE_USER_AGENT]
                             [--extra_parameters EXTRA_PARAMETERS]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     predict from url
  -f FILE, --file FILE  predict from file
  -m MODEL, --model MODEL
                        prediction model
  --documents_limit DOCUMENTS_LIMIT
                        Max number of documents expected
  --documents_topics_limit DOCUMENTS_TOPICS_LIMIT
                        Maximum number of topics expected per document
  --found_topics_limit FOUND_TOPICS_LIMIT
                        Maximum number of topics expected
  --related_topics_limit RELATED_TOPICS_LIMIT
                        Maximum number of related topics expected
  --elements_limit ELEMENTS_LIMIT
                        Number of elements within each topic
  --qualifiers          Use qualifiers on topics
  --labels              Index and/or return topic labels
  --words               Index and/or return topic words
  --date_from DATE_FROM
                        recommend in topics newer than
  --date_to DATE_TO     recommend in topics older than
  --in_index            Look up uri in application index
  --filters_in [FILTERS_IN [FILTERS_IN ...]]
                        Preprocessing filters
  --remote_user_agent REMOTE_USER_AGENT
                        User agent string to be used by XPLR to fetch
                        resources
  --extra_parameters EXTRA_PARAMETERS
                        appended to the query string to underlying search
                        system

</pre>
