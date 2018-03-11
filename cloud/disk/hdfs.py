import json
from .models import File
import urllib.parse
import logging
import http.client
logging.basicConfig(level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p',
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name='webhdfs')
WEBHDFS_CONTEXT_ROOT="/webhdfs/v1"
class WebHdfs(object) :
    def __init__(self,namenode_host, namenode_port, hdfs_username):
        self.namenode_host=namenode_host
        self.namenode_port = namenode_port
        self.username = hdfs_username

    def __getNameNodeHTTPClient(self):
        httpClient = http.client.HTTPConnection(self.namenode_host,
                                            self.namenode_port,
                                            timeout=600)
        return httpClient
    def put(self, source_data, target_path, replication=1):
        url_path =WEBHDFS_CONTEXT_ROOT + target_path + '?op=CREATE&overwrite=true&user.name='+self.username
        httpClient = self.__getNameNodeHTTPClient()
        httpClient.request('PUT',url_path,headers={})
        response = httpClient.getresponse()
        msg=response.msg
        redirect_location = msg['location']
        logger.debug("HTTP Location: %s" % (redirect_location))
        result = urllib.parse.urlparse(redirect_location)
        redirect_host = result.netloc[:result.netloc.index(":")]
        redirect_port = result.netloc[(result.netloc.index(":") + 1):]
        # Bug in WebHDFS 0.20.205 => requires param otherwise a NullPointerException is thrown
        redirect_path = result.path + "?" + result.query + "&replication=" + str(replication)

        logger.debug("Send redirect to: host: %s, port: %s, path: %s " % (redirect_host, redirect_port, redirect_path))
        fileUploadClient = http.client.HTTPConnection(redirect_host,
                                                  redirect_port, timeout=600)
        # This requires currently Python 2.6 or higher
        fileUploadClient.request('PUT', redirect_path, source_data, headers={})
        response = fileUploadClient.getresponse()
        logger.debug("HTTP Response: %d, %s" % (response.status, response.reason))
        httpClient.close()
        fileUploadClient.close()
        return response.status
    def copyFromLocal(self, file, target_path,replication = 1):
        return self.put(file,target_path,replication)
    def download(self,source_path):
        url_path = WEBHDFS_CONTEXT_ROOT + source_path +'?op=OPEN&overwrite=true&user.name='+self.username
        httpClient = self.__getNameNodeHTTPClient()
        httpClient.request('GET', url_path, headers={})
        response = httpClient.getresponse()
        if response.length!=None:
            msg = response.msg
            redirect_location = msg['location']
            result=urllib.parse.urlparse(redirect_location)
            redirect_host = result.netloc[:result.netloc.index(":")]
            redirect_port = result.netloc[(result.netloc.index(":")+1):]
            redirect_path = result.path + "?" + result.query
            fileDownloadClient = http.client.HTTPConnection(redirect_host,redirect_port,
                                                             timeout=600)
            fileDownloadClient.request('GET',redirect_path,headers={})
            response = fileDownloadClient.getresponse()
            return {"status":"ok","file":response}
        return {"status":"no"}
