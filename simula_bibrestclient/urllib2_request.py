"""
Urllib2 request class. This is here as an example of how to use the API
without restkit.
"""
import urllib2
import base64

class RestRequest(urllib2.Request):
    """
    Request class that:

        - supports specifying a HTTP method
        - defaults to Accept ``application/json``.
        - Supports basic auth

    This is all you need for a basic low-level REST interface.
    """
    def __init__(self, url, data=None,
                 headers={},
                 accept='application/json',
                 method='get', **kwargs):
       self._method = method
       if accept:
           headers['Accept'] = accept
       urllib2.Request.__init__(self, url=url, data=data, headers=headers, **kwargs)

    def get_method(self):
        return self._method.lower()

    def add_basicauth_header(self, username, password):
        base64string = base64.encodestring('{0}:{1}'.format(username, password)).replace('\n', '')
        self.add_header("Authorization", "Basic %s" % base64string)

    @classmethod
    def basicauth_request(cls, username, password, **kwargs):
        request = cls(**kwargs)
        request.add_basicauth_header(username, password)
        response = urllib2.urlopen(request)
        return response


if __name__ == '__main__':
    #################################
    # Example
    #################################

    #folderurl = 'https://simula.no/publications/'
    folderurl = 'http://localhost:8080/simula/publications/'
    #opener = build_opener(url=folderurl, username='grandma', password='test')
    auth = dict(username='grandma', password='test')

    ################################################
    # REST operations on a bibliography folder
    ################################################
    folder_rest_url = '{folderurl}/@@rest'.format(folderurl=folderurl)
    try:
        response = RestRequest.basicauth_request(url=folder_rest_url, method='get', **auth)
    except urllib2.HTTPError, e:
        print 'Error', e
        print e.read()
        raise SystemExit()
    else:
        print
        print 'ALL items in:', folderurl
        print response.read()


    ################################################
    # REST operations on a single bibliography item
    ################################################
    itemid = 'example' # NOTE: Assumes this is an existing ArticleReference with "Short Name"=itemid
    itemurl = '{folderurl}{itemid}/@@rest'.format(folderurl=folderurl,
                                                  itemid=itemid)

    # Perform GET
    try:
        response = RestRequest.basicauth_request(url=itemurl, method='get', **auth)
    except urllib2.HTTPError, e:
        print 'Error', e
        print e.read()
        raise SystemExit()
    else:
        print
        print 'ITEM:', itemurl
        print response.read()

    # Perform PUT
    import json
    data = json.dumps({'portal_type': 'ArticleReference',
                       'item': {'title': 'This was updated using urllib2 and RestRequest'}})
    try:
        response = RestRequest.basicauth_request(url=itemurl, data=data, method='put', **auth)
    except urllib2.HTTPError, e:
        print 'Error', e
        #print e.read()
        raise SystemExit()
    else:
        print
        print 'UPDATED ITEM:', itemurl
        print response.read()
