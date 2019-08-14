#-*-coding:utf-8-*-
from elasticsearch import  Elasticsearch
#连接es服务器
es=Elasticsearch(["10.10.21.46"],timeout=100)
print(es)
data={
    "mappings":{
        "properties":{
            "title":{
                "type":"text",
                "index":True
            },
            "keywords":{
                "type":"text",
                "index":True
            },
            "link":{
                "type":"text",
                "index":True
            },
            "content":{
                "type":"text",
                "index":True
            },
        }
    }
}
es.indices.create(index="pythonTest",body=data)
