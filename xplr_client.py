"""
XPLR Client Module.

Povides:

Config function: to get config directionnary from default or provided config file,
dictonnary may be feed up with values from specific application sections.

XPLR class: a pythonic proxy to the XPLR api.

XPLRDataset class: a manager for preparing datasets for xplr learn.

Licence :

Copyright (c) 2013 Xplr Software Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

import ConfigParser
import urllib2
import httplib
import os.path
import json
import uuid

VERBOSE=False

def LOG(msg):
    """Output a log message."""

    # TODO : use python log manager classes instead of this stupid print
    if VERBOSE:
        print msg


def Config(appspec = None, alternatefile = None):
    """Read the XPLR config file.
    
    Keywords arguments:
    appspec -- application name(s) to read config sections from
    alternatefile -- a alternative config file to ~/.xplrclient

    Returns:
    A dictionnary containing the xplr config and additional config values
    from appspec

    """
    
    config = ConfigParser.SafeConfigParser()
    # shall we read the alternate or default config file
    if alternatefile is not None:
        config.read(alternatefile)
    else:
        config.read(os.path.expanduser('~/.xplrclient'))
    res={}
    # add xplr config
    res.update({'xplr':dict(config.items("xplr"))})
    # add additional config sections
    if not isinstance(appspec, list):
        appspec=[appspec]
    for sect in appspec:
        try:
            res.update({sect:dict(config.items(sect))})
        except ConfigParser.NoSectionError:
            res.update({sect:{}})
    return res


### Exception classes :

class XPLRCommunicationError(Exception):
    def __init__(self, url, http_method,  headers, body, response=None):
        self.msg = """XPLR Communication Error"""
        self.http_method = http_method
        self.req_headers = headers
        self.req_body = body
        self.url = url
        self.res_headers = None
        if response is not None:
            self.res_headers = response.get_info()
            

    def __str__(self):
        msg = "%s %s\n"%(str(self.http_method),str(self.url))
        for h,v in self.req_headers.iteritems():
            msg += "%s:%s\n"%(h,v)
        msg += "\n"
        if self.req_body is not None:
            msg += str(self.req_body)[:100]
        msg += "\n"
        msg += "--\n"
        msg += str(self.res_headers)
        msg += "\n"
        return str



class XPLRDataError(Exception):
    def __init__(self, url, http_method,  headers, body, data=None):
        self.msg = "XPLR Data Error"
        self.http_method = http_method
        self.req_headers = headers
        self.req_body = body
        self.url = url
        self.data = data

    def __str__(self):
        msg = "%s %s\n"%(str(self.http_method),str(self.url))
        if self.data is not None:
            msg += str(self.data)[:100]
        msg += "\n"
        return msg
        for h,v in self.req_headers.iteritems():
            msg += "%s:%s\n"%(h,v)
        msg += "\n"
        if self.req_body is not None:
            msg += str(self.req_body)
        msg += "\n"
        msg += "--\n"
        msg += str(self.data)
        msg += "\n"
        return str


API_METHODS_URL = {
    "1.15e" : {
        "info":"/topics/info",
        "model":"/topics/models",
        "learn":"/topics/learn",
        "predict":"/topics/predict",
        "search":"/topics/search",
        "recommend":"/topics/recommend",
        },
    "1.15f" : {
        "info":"/info",
        "model":"/models",
        "learn":"/learn",
        "predict":"/predict",
        "search":"/search",
        "recommend":"/recommend",
        }
}


class XPLR(object):
    """Handle http requests to the XPLR server.

    Public Methods:
    info: get info from the XPLR node, list avalaible models.
    get_model: get info from a model, list topics.
    create_model: create a new model in the userspace.
    delete_model: delete a model from the userspace.
    update_model: add topics to a model
    learn: learns a dataset
    predict_uri: makes a prediction from a url, fetching content in XPLR side
    predict_content: makes prediction from a provided text
    
    """

    __HTTP=0
    __HTTPS=1
    
    def __init__(self, key=None, host="api.xplr.com", port=443, app=None, proto=1, apiversion='1.15f'):
        """XPLR class constructor

        Parameters:
        key -- the XPLR api key
        host -- the XPLR api host
        port -- the tcp port on which XPLR API is responding
        app -- the XPLR application id to be used for indexing/search operations
        proto -- use https (1, default) or http connexion
        """
        self.apiversion = apiversion
        self.__urls = API_METHODS_URL[apiversion]
        self.__key=key
        self.__host=host
        self.__port=port
        self.__app=app
        self.__proto=proto
        if proto == self.__HTTP:
            self.__xplrurl='http://%s:%d'%(host,port)
        else:
            self.__xplrurl='https://%s:%d'%(host,port)

    def __get(self, method, args=None):
        """Perform a GET request to xplr."""

        u = self.__xplrurl
        u += method
        if args is not None:
            sep = "?"
            for arg,argv in args.iteritems():
                u += sep
                sep = "&"
                u += urllib2.quote(arg)
                u += '='
                if argv is not None:
                    u += urllib2.quote(argv)
                    
        LOG("GET %s"%u)
        response = None
        headers = {}
        try:
            req = urllib2.Request(u)
            req.add_header('XPLR-Api-Key',self.__key)
            headers.update({'XPLR-Api-Key':self.__key})
            if self.__app is not None:
                req.add_header('XPLR-App-id',self.__app)
                headers.update({'XPLR-App-id':self.__app})
            response = urllib2.urlopen(req)
            jsonresponse=response.read()
        except:
            raise XPLRCommunicationError(u,"GET",headers,None,response)
        LOG(jsonresponse)
        try:
            return json.loads(jsonresponse)
        except:
            raise XPLRDataError(u,"GET",headers,None,jsonresponse)

    def __put(self, method, body):
        """Perform a PUT request to xplr."""

        LOG("PUT %s\n%s"%(method,body))
        r = None
        u = ""
        headers = {}
        try:
            if self.__proto == self.__HTTP:
                u = "http://%s:%s%s"%(self.__host,self.__port,method)
                c=httplib.HTTPConnection(self.__host,self.__port)
            else:
                u = "https://%s:%s%s"%(self.__host,self.__port,method)
                c=httplib.HTTPSConnection(self.__host,self.__port)
            headers.update({'XPLR-Api-Key':self.__key})
            if self.__app is not None:
                headers.update({'XPLR-App-id':self.__app})
            c.request('PUT',method,body,headers)
            r = c.getresponse()
            data = r.read()
        except:
            raise XPLRCommunicationError(u,"PUT",headers,body,r)

        LOG(data)
        try:
            return json.loads(data)
        except:
            raise XPLRDataError(u,"PUT",headers,body,data)
    
    def __post(self, method, body):
        """Perform a POST request to xplr."""

        r = None
        u = ""
        headers = {}
        try:
            if self.__proto == self.__HTTP:
                LOG("curl -X POST 'http://%s:%s%s' -H 'XPLR-Api-Key:%s' -H 'XPLR-App-id:%s' -d '%s'"%(self.__host,
                                                                                                       self.__port,
                                                                                                       method,
                                                                                                       self.__key,
                                                                                                       self.__app,
                                                                                                       body))
                u = "http://%s:%s%s"%(self.__host,self.__port,method)
                c=httplib.HTTPConnection(self.__host,self.__port)
            else:
                LOG("curl -k -X POST 'https://%s:%s%s' -H 'XPLR-Api-Key:%s' -H 'XPLR-App-id:%s' -d '%s'"%(self.__host,
                                                                                                           self.__port,
                                                                                                           method,
                                                                                                           self.__key,
                                                                                                           self.__app,
                                                                                                           body))
                u = "http://%s:%s%s"%(self.__host,self.__port,method)
                c=httplib.HTTPSConnection(self.__host,self.__port)

            headers.update({'XPLR-Api-Key':self.__key})
            if self.__app is not None:
                headers.update({'XPLR-App-id':self.__app})
            c.request('POST',method,body,headers)
            r = c.getresponse()
            data = r.read()
            
        except:
            raise XPLRCommunicationError(u,"POST",headers,body,r)

        LOG(data)
        try:
            return json.loads(data)
        except:
            raise XPLRDataError(u,"POST",headers,body,data)
 
    def __delete(self, method):
        """Perform a DELETE request to xplr."""

        LOG("DELETE %s"%(method))
        r = None
        u = ""
        headers = {}
        try:
            if self.__proto == self.__HTTP:
                u = "http://%s:%s%s"%(self.__host,self.__port,method)
                c=httplib.HTTPConnection(self.__host,self.__port)
            else:
                u = "https://%s:%s%s"%(self.__host,self.__port,method)
                c=httplib.HTTPSConnection(self.__host,self.__port)
            headers.update({'XPLR-Api-Key':self.__key})
            if self.__app is not None:
                headers.update({'XPLR-App-id':self.__app})
            c.request('DELETE',method,body,headers)
            r = c.getresponse()
            data = r.read()
        except:
            raise XPLRCommunicationError(u,"DELETE",headers,None,r)

        LOG(data)
        try:
            return json.loads(data)
        except:
            raise XPLRDataError(u,"DELETE",headers,None,data)

    
    # Public methods

    def info(self):
        """Get information on the XPLR API server : avaliable model"""
        return self.__get(self.__urls["info"])


    # models
    
    def get_model(self, model,topic_ids=True,labels=True,words=True,elements_limit=None):
        """Get detailed information on a model.

        Parameters:
        model -- model identifier
        topic_ids -- include identifiers of topics in result
        labels -- include labels of topics in result
        words -- include words of topics in result
        element_limit -- max number of words/labels to be returned
        """

        qs=self.__urls["models"] + "/%s"%model
        if topic_ids:
            qs += "?topic_ids=true"
        else:
            qs += "?topic_ids=false"
        if labels:
            qs += "&labels=true"
        else:
            qs += "&labels=false"
        if words:
            qs += "&words=true"
        else:
            qs += "&words=false"
        if elements_limit is not None:
            qs += "&elements_limit=%d"%elements_limit
        return self.__get(qs)
    
    def create_model(self, model, description, lang, qualifiers=None, fork=None, topics_number=None, forkfile=None, forkkey=None):
        """Create a new model.
    
        Parameters:
        description -- long description of the model.
        lang -- language of the model
        qualifiers -- list of lpo qualifiers to be used with this model (default None)
        fork -- shall the model be forked from an existing model
        topics_number -- number of topics to be precreated in the model
        }
        """
        
        body={"description":description,
              "lang":lang}
        if qualifiers is not None:
            body.update({"qualifiers":qualifiers})
        if fork is not None:
            body.update({"fork":fork})
            if forkfile is not None:
                body.update({"forkfile":forkfile})
            if forkkey is not None:
                body.update({"forkkey":forkkey})
        if  topics_number is not None:
            body.update({"topics_number":topics_number})
        return self.__put(self.__urls["models"] + '/%s'%model,json.dumps(body))


    def delete_model(self,model):
        """Delete an existing model associated to the API key."""

        return self.__delete(self.__urls["models"] + '/%s'%model)

    def update_model(self, model, update_words=True, auto_labeling=True, labels=None):
        """Update an existing model associated to tu user API key.

        Parameters:
        model -- the identifier of the model to update
        update_words -- shall words of topic be recomputed during learn operations
        auto_labeling -- shall topics be automatically computed
        labels -- dictionnary of topics (key : topics id, value : topic label) to be
                  added / updated in the model for supervised learning
        """

        body = {"update_words":update_words,
                "auto_labeling":auto_labelling}
        if labels is not None:
            body.update({"labels":labels})
        return self.__post(self.__urls["models"] + '/%s'%model, json.dumps(body))

    
    # learn (iterator)
    def learn(self, dataset, model, chunk_size=1, content_extraction=False):
        """Learn topics in a model from a dataset.
        
        Parameters:
        dataset -- XPLRDataset object containing the documents to be learned
        model -- model used for learning
        chunck_size -- size of document chuncks to be sent to XPLR in a single request (default 1)
        content_extraction -- perform content extraction on content before learning (default False)
        
        Returns an iterator on the result structures of each chunck sent to XPLR
        """

        params={"model":model}
        if content_extraction:
            params.update({"content_extraction":content_extraction})
        body = {"parameters":params}
        for docs in dataset.iterdocs(chunk_size):
            body.update({"collection":docs})
            yield self.__post(self.__urls["learn"], json.dumps(body))
        return 

    # predict

    def predict_uri(self, uri, **options):
        """Predict the content located at a given url.

        Parameters:
        uri -- the uri from which content is fetched
        options -- all avalaible options from XPLR predict API method
        """
        
        params={}
        params.update(options)
        body = {"parameters":params}
        body.update({"document":{"uri":uri}})
        return self.__post(self.__urls["predict"], json.dumps(body))

    def predict_content(self, data, content_type="text/plain", uri=str(uuid.uuid1()), title=None, **options):
        """Predict a content from data
        data -- the content to be predicted
        content_type -- the mimetype of the content (used for content extraction)
        uri -- the unique identifier for indexing the document into XPLR
        title -- the title of the document
        options -- all avalaible options from XPLR predict API method
        """

        params={}
        params.update(options)
        body = {"parameters":params}
        body.update({"document":{"content":data,"content_type":content_type,"uri":uri}})
        if title is not None:
            body['document'].update({"title":title})
        return self.__post(self.__urls["predict"], json.dumps(body))


    def search(self, query, **options):
        """Search in the XPLR index
        query -- the searched words
        options -- all avalaible options from XPLR search API
        """
        params={}
        params.update({'q':query})
        params.update(options)
        body = {"parameters":params}
        return self.__post(self.__urls["search"], json.dumps(body))

    def recommend_uri(self, uri, **options):
        """Recommend from the content located at a given url.

        Parameters:
        uri -- the uri from which content is fetched
        options -- all avalaible options from XPLR recommend API
        """
        
        params={}
        params.update(options)
        body = {"parameters":params}
        body.update({"document":{"uri":uri}})
        return self.__post(self.__urls["recommend"], json.dumps(body))

    def recommend_content(self, data, content_type="text/plain", uri=str(uuid.uuid1()), title=None, **options):
        """Recommend from a content from data
        data -- the content to be predicted
        content_type -- the mimetype of the content (used for content extraction)
        uri -- the unique identifier for indexing the document into XPLR
        title -- the title of the document
        options -- all avalaible options from XPLR recommend API
        """

        params={}
        params.update(options)
        body = {"parameters":params}
        body.update({"document":{"content":data,"content_type":content_type,"uri":uri}})
        if title is not None:
            body['document'].update({"title":title})
        return self.__post(self.__urls["recommend"], json.dumps(body))


    
class XPLRDataset(object):
    """Dataset manager for documents to be learnt by XPLR.
    
    Public methods:
    add_url: adds an url to the dataset 
    add_file: adds a (reference to) a local file to the dataset
    add_data: adds a data to the dataset
    iter: returns an iterator over the documents of the dataset
    iterdocs: returns an iterator over dictionnaries that conform
              to the json structure needed by XPLR learn method
    delete: delete the dataset
    info: returns the state of the dataset
    """

    URL=0
    DATA=1
    FILE=2
    def __init__(self, name, datadir = os.path.expanduser('~/.xplr_datasets')):
        """initialise or loads an XPLRDataset.
        
        Parameters:
        name -- name of the dataset
        datadir -- location of the dataset on the filesystem (default : ~/.xplr_dataset)
        """

        if not os.path.exists(datadir):
            os.path.makedirs(datadir)
        self.__dir=datadir
        self.__name=name
        self.__jsonf=os.path.join(datadir, name+'.json')
        if not os.path.exists(jsonf):
            self.__set=[]
            self.__flush()
        else:
            with open(self.__jsonf) as f:            
                self.__set=json.load(f)

    def __flush(self):
        with open(self.__jsonf, 'w') as f:
            json.dump(self.__set,f)
            
    def add_url(self,url,title=None):
        doc={"type":self.URL,
             "id":str(uuid.uuid1()),
             "url":url,
             "title":title}
        self.__set.append(doc)
        self.__flush()

    def add_file(self,datafile,title=None):
        doc={"type":self.FILE,
             "id":uuid.uuid1(),
             "file":datafile,
             "title":title}
        self.__set.append(doc)
        self.__flush()

    def add_data(self,data,title=None,content_type=None):
        id=uuid.uuid1()
        doc={"type":self.DATA,
             "id":uuid.uuid1(),
             "data":data,
             "title":title,
             "content_type":content_type
             }
        with open(os.path.join(self.__dir,self.__name,id),'w') as f:
            f.write(data)
        self.__set.append(doc)
        self.__flush()

    def iter(self, chunk_size=None):
        if chunk_size is None :
            chunk_size=1
        for i in xrange(0,len(self.__set),chunk_size):
            yield self.__set[i:i+chunk_size]

    def iterdocs(self,chunk_size=None):
        for docs in self.iter(chunk_size):
            yield [self.__prepare(d) for d in docs]

    def delete(self):
        os.path.rmtree(os.path.join(self.__dir,self.__name))
        os.path.rm(os.path.join(self.__dir,self.__name+'.json'))

    def info(self):
        return {"name":self.__name,"documents":len(self.__set)}

    def __prepare(self,doc):
        d={}
        t=doc.get('type')
        if t == self.URL:
            d.update({'uri':doc.get('url')})
            if doc.get("title",None) is not None:
                d.update({'title': doc.get("title")})
        if t == self.FILE:
            with open(doc.get('file')) as f:
                data=f.read()
            d.update({'content': data})
            d.update({'uri': 'urn:xplr:'+doc.get("id")})
            if doc.get("title",None) is not None:
                d.update({'title': doc.get("title")})
        if t == self.DATA:
            d.update({'content': +doc.get("data")})
            d.update({'uri': 'urn:xplr:'+doc.get("id")})
            if doc.get("title",None) is not None:
                d.update({'content': doc.get("title")})
            if doc.get("content_type", None) is not None:
                d.update({'content_type': doc.get("content_type")})
        return d
   
