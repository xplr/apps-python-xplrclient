#!/usr/bin/env python
"""
XPLR Command line client
"""
import argparse
import os.path
import sys
import xplr_client

xplr_client.VERBOSE=False


    
# ---- CLI stuff


def xplr_info(args, xplr):
    xplr_client.LOG('calling info')
    dformat( xplr.info())
    
    
def xplr_model (args, xplr):
    xplr_client.LOG('calling model')
    if args.act == 'create':
        dformat(xplr.create_model(args.model, args.description,
                                  args.lang, args.topics_number, args.fork))
    if args.act == 'update':
        dformat(xplr.update_model(args.model, args.update_words, args.auto_labeling,
                                  dict(args.labels)))
    if args.act == 'delete':
        dformat(xplr.delete_model(args.model))
    if args.act == 'info':
        dformat(xplr.get_model(args.model))


def xplr_predict (args, xplr):
    xplr_client.LOG('calling predict')
    params={}
    for param in ['model',
                   'topics_limit',
                   'elements_limit',
                   'qualifiers',
                   'content_extraction',
                   'index',
                   'recurrent',
                   'labels',
                   'words',
                   'return_content',
                   'return_title',
                   'return_content_type',
                   'return_image',
                   'return_description',
                   'return_excerpts',
                   'return_url',
                   'remote_user_agent',
                   'idx_fields']:
        if  param in dir(args) and getattr(args,param) is not None:
           params.update({param:getattr(args,param)}) 
    if args.url is not None:
        # predict from url
        dformat(xplr.predict_uri(args.url, **params))
    else:
        # predict from data on stdin
        data=sys.stdin.read()
        if args.uri is not None:
            params.update({'uri':args.uri})
        dformat(xplr.predict_content(data,**params))

def xplr_search (args, xplr):
    xplr_client.LOG('calling search')
    for param in ['q',
                  'documents_limit',
                  'documents_topics_limit',
                  'found_topics_limit',
                  'related_topics_limit',
                  'elements_limit',
                  'use_fields',
                  'labels',
                  'words',
                  'exact_match',
                  'date_from',
                  'date_to',
                  'extra_parameters']:
        if  param in dir(args) and getattr(args,param) is not None:
           params.update({param:getattr(args,param)}) 
    dformat(xplr.search(data,**params))
    
def xplr_dataset (args, xplr):
    xplr_client.LOG('calling dataset')
    if args.act == 'list':
        for f in os.path.listdir(args.datadir):
            try:
                n,e=os.path.splitext(f)
                if e == ".json":
                    print n
            except:
                pass
    else:        
        ds=xplr_client.XPLRDataset(args.dataset, args.datadir)
        if args.act == "delete":
            ds.delete()
        if args.act == "info":
            dformat(ds.info())
        if args.act == "add":
            if args.url:
                ds.add_url(args.url)
            elif args.file:
                ds.add_file(args.file,args.title)
            elif args.dir:
                raise Exception, "Not Implemented"
            else:
                data=sys.stdin.read()
                ds.add_data(data,args.title,args.content_type)
            
        
    
def xplr_learn (args, xplr):
    xplr_client.LOG('calling learn')
    model=args.model
    dataset=xplr_client.XPLRDataset(arg.dataset)
    params={}
    for param in ['chunk_size',
                   'content_extraction',
                   'remote_user_agent']:
        if  param in dir(args) and getattr(args,param) is not None:
           params.update({param:getattr(args,param)}) 
    
    for resp in xplr.learn(dataset, args.model, **params):
        print "--- chunck ---"
        dformat(resp)
    
def xplr_recommend (args, xplr):
    xplr_client.LOG('calling recommend')
    model=args.model
    dataset=xplr_client.XPLRDataset(arg.dataset)
    params={}
    for param in ['model',
                  'documents_limit',
                  'documents_topics_limit',
                  'found_topics_limit',
                  'related_topics_limit',
                  'elements_limit',
                  'qualifiers',
                  'content_extraction',
                  'labels',
                  'words',
                  'date_from',
                  'date_to',
                  'in_index']:
        if  param in dir(args) and getattr(args,param) is not None:
           params.update({param:getattr(args,param)}) 
    
    if args.url is not None:
        # recommend from url
        if args.content_extraction:
            params.update({'content_extraction':args.content_extraction}) 
        dformat(xplr.recommend_uri(args.url, **params))
    else:
        # recommend from data on stdin
        data=sys.stdin.read()
        dformat(xplr.recommend_content(data,**params))



        
def dformat(d, i=''):
    if QUIET:
        return
    i += '  '
    if isinstance(d, dict):
        for k,v in d.iteritems():
            pre=i+'['+str(k)+']'
            if not isinstance(v, list) and not isinstance(v,dict):
                print pre,v
            else:
                 print pre 
                 dformat(v,i)
    elif isinstance(d, list):
        first=True
        for v in d:
            if not first:
                print i+'--'
            first=False
            dformat(v,i)
    else:
        print i+str(d)
    

if __name__ == '__main__':
            
    metaparser = argparse.ArgumentParser(add_help=False)
    metaparser.add_argument('-v','--verbose', action='store_true', help="display detailed connection messages")
    metaparser.add_argument('-q','--quiet', action='store_true', help="do ,ot display foprmatted answers from XPLR")
    metaparser.add_argument('-C','--config', help="alternative config file", metavar="FILE")
    args, remaining_argv = metaparser.parse_known_args()

    
    config_sections=['cli_model',
                     'cli_predict',
                     'cli_search',
                     'cli_dataset',
                     'cli_learn',
                     'cli_recommend']
    if args.config:
        config = xplr_client.Config(config_sections,args['config'])
    else:
        config = xplr_client.Config(config_sections)

    xplr_client.VERBOSE=args.verbose
    QUIET=args.quiet
    
    parser = argparse.ArgumentParser(parents=[metaparser],description=__doc__)
    
    defaults=config.get("xplr",{})
    parser.set_defaults(**defaults)

    parser.add_argument('-H','--host', action='store',help="XPLR API host")
    parser.add_argument('-P','--port', action='store',help="XPLR API port", type=int)
    parser.add_argument('-K','--key', action='store', help="XPLR API key")
    #parser.add_argument("-S", "--ssl", action="store_true", default=True, help="use ssl on XPLR calls")
    
    subparsers = parser.add_subparsers(title='XPLR commands')
    
    # info
    parser_i = subparsers.add_parser('info', help='Get server info')
    parser_i.set_defaults(callback=xplr_info)

    # models    
    parser_m = subparsers.add_parser('model', help='Create and manage models')
    subparsers_m = parser_m.add_subparsers(title='XPLR models subcommands')

    # model info 
    parser_mi = subparsers_m.add_parser('info' ,help="Get model info")
    parser_mi.add_argument('-i','--topic_ids', action='store_true',help="display topic identifiers")
    parser_mi.add_argument('-l','--labels', action='store_true',help="display labels")
    parser_mi.add_argument('-w','--words', action='store_true',help="display words")
    parser_mi.add_argument('-m','--elements_limit', action='store',help="Number of labels/words displayed",type=int, metavar="N")
    parser_mi.add_argument('model', help='model identifier', metavar="<model_id>")
    parser_mi.set_defaults(act='info')

    # model creation
    parser_mc = subparsers_m.add_parser('create' ,help="Create new model")
    parser_mc.add_argument('-m','--topics_number', action='store',help="Number of topics created",type=int)
    parser_mc.add_argument('-f','--fork', action='store',help="fork an existing model")
    parser_mc.add_argument('-d','--description', action='store',help="long description")
    parser_mc.add_argument('-l','--lang', action='store',help="language")
    parser_mc.add_argument('-q','--qualifiers', nargs="*" ,help="qualifiers")
    parser_mc.add_argument('model', help='model identifier', metavar="<model_id>")
    parser_mc.set_defaults(act='create')

    # model update
    parser_mu = subparsers_m.add_parser('update' ,help="Update model")
    parser_mu.add_argument('-w','--update_words', action='store_true',help="Update words")
    parser_mu.add_argument('-a','--auto_labeling', action='store_true',help="Auto labels")
    parser_mu.add_argument('-l','--labels', help="update labels : -l topicid label",nargs='*',action="append")
    parser_mu.add_argument('model', help='model identifier', metavar="<model_id>")
    parser_mu.set_defaults(act='create')

    # model delete
    parser_md = subparsers_m.add_parser('delete',help="Delete model")
    parser_md.add_argument('model', help='model identifier', metavar="<model_id>")
    parser_md.set_defaults(act='delete')
    
    defaults=config.get("cli_model",{})
    
    defaults.update({'callback':xplr_model})
    parser_m.set_defaults(**defaults)

    # predict
    
    parser_p = subparsers.add_parser('predict',help= 'Perform predictions')
    parser_ps = parser_p.add_mutually_exclusive_group()
    parser_ps.add_argument('-u','--url', action='store',help="predict from url")
    parser_ps.add_argument('-f','--file', action='store',help="predict from file")
    parser_ps.add_argument('-d','--dataset', action='store',help="predict from dataset")
    # if non of u,f,d -> read data on stdin
    
    parser_p.add_argument('--uri', action='store',help="uri for indexation")
    parser_p.add_argument('-m','--model', action='store',help="prediction model")
    parser_p.add_argument('--topics_limit', action='store',help="Number of topics predicted",type=int)
    parser_p.add_argument('--elements_limit', action='store',help="Number of elements within each topic")
    parser_p.add_argument('--qualifiers', action='store_true',help="Use qualifiers on topics")
    parser_p.add_argument('--content_extraction', action='store_true',help="Try to extract text content")
    parser_p.add_argument('--index', action='store_true',help="Shall the document(s) be indexed by xplr")
    parser_p.add_argument('--recurrent', action='store_true',help="Forces the creation of a new entry in XPLR index")
    parser_p.add_argument('--labels', action='store_true',help="Index and/or return topic labels")
    parser_p.add_argument('--words', action='store_true',help="Index and/or return topic words")
    parser_p.add_argument('--return_content', action='store_true',help="Index and/or return text content")
    parser_p.add_argument('--return_title', action='store_true',help="Index and/or return document title")
    parser_p.add_argument('--return_content_type', action='store_true',help="Index and/or return mime content-type")
    parser_p.add_argument('--return_image', action='store_true',help="Index and/or return relevant image")
    parser_p.add_argument('--return_description', action='store_true',help="Index and/or return description")
    parser_p.add_argument('--return_excerpts', action='store_true',help="Index and/or return excepts")
    parser_p.add_argument('--return_url', action='store_true',help="Return document real url")
    parser_p.add_argument('--remote_user_agent', action='store',help="User agent string to be used by XPLR to fetch resources")
    parser_p.add_argument('--idx_fields',help="Extra indexation fields (sequence -x field value) ",nargs='*',action="append")
   
    defaults=config.get("cli_predict",{})
    defaults.update({'callback':xplr_predict})

    # check coherence
    # recurrent requires index
    # idx_fields requires index
    # url interdit uri
    parser_p.set_defaults(**defaults)

    # search 
    
    parsers = subparsers.add_parser('search', help='Search XPLR topics index')
    defaults=config.get("cli_search",{})
    defaults.update({'callback':xplr_search})
    parsers.set_defaults(**defaults)

    # datasets
    parser_d = subparsers.add_parser('dataset', help='Create and manage datasets')
    subparsers_d = parser_d.add_subparsers(title='XPLR dataset subcommands')
    
    # dataset list 
    parser_dl = subparsers_d.add_parser('info' ,help="Get dataset info")
    parser_dl.set_defaults(act='list')

    # dataset info 
    parser_di = subparsers_d.add_parser('info' ,help="Get dataset info")
    parser_di.add_argument('dataset', help='dataset identifier', metavar="<dataset_id>")
    parser_di.set_defaults(act='info')

    # dataset add document
    parser_du = subparsers_d.add_parser('add' ,help="add a document to dataset")
    parser_dus = parser_du.add_mutually_exclusive_group()
    parser_dus.add_argument('-u','--url', action='store',help="add url")
    parser_dus.add_argument('-f','--file', action='store',help="add file")
    parser_dus.add_argument('-d','--dir', action='store',help="add files from directory")
    parser_du.add_argument('-t','--title', help="document title")
    parser_du.add_argument('-c','--content_type', help="document content type")
    parser_du.add_argument('-l','--topic', help="topics identifiers (supervised mode)",  )
    parser_du.add_argument('dataset', help='dataset identifier', metavar="<dataset_id>")
    parser_du.set_defaults(act='add')

    # dataset delete
    parser_dd = subparsers_d.add_parser('delete',help="Delete dataset")
    parser_dd.add_argument('dataset', help='dataset identifier', metavar="<dataset_id>")
    parser_dd.set_defaults(act='delete')

    defaults=config.get("cli_dataset",{})
    defaults.update({'callback':xplr_dataset})
    parser_d.set_defaults(**defaults)
    
    # learn
    
    parser_l = subparsers.add_parser('learn', help='Learn')
    parser_l.add_argument('-m','--model', action='store', required=True)
    parser_l.add_argument('-d','--dataset', action='store', required=True)
    parser_l.add_argument('-c','--chunk_size', action='store', type=int)
    parser_l.add_argument('-x','--content_extraction', action='store_true')
    parser_l.add_argument('--remote_user_agent', action='store',help="User agent string to be used by XPLR to fetch resources")

    defaults=config.get("cli_learn",{})
    defaults.update({'callback':xplr_learn})
    parser_l.set_defaults(**defaults)

    #recommend
    
    parser_r = subparsers.add_parser('recommend', help='Recommend')
    parser_r.add_argument('-a','--app ', action='store')
    parser_r.add_argument('--remote_user_agent', action='store',help="User agent string to be used by XPLR to fetch resources")

    defaults=config.get("cli_recommend",{})
    defaults.update({'callback':xplr_recommend})
    parser_r.set_defaults(**defaults)

    # end of args definition
    
    args = parser.parse_args(remaining_argv)
    xplr_client.LOG(args)

    xplri=xplr_client.XPLR(args.key, args.host, port=int(args.port))
    args.callback(args, xplri)
