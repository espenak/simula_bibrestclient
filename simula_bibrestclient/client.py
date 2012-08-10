import json
from restkit import Resource, BasicAuth
from warnings import warn

from .defaults import folderurl


def urljoin(url, *paths):
    if not url.endswith('/'):
        url += '/'
    return url + '/'.join(paths)


class BibResource(Resource):
    """
    Base class for the REST APIs.
    """
    def __init__(self, url, username, password,
                 mimetype='application/json',
                 decode_output=False):
        """
        :param url: URL to the REST API (including @@rest).
        :param username: Simula website username.
        :param password: Simula website password.
        :param mimetype: See :obj:`.mimetype`.
        :param decode_output: See :obj:`.decode_output`.
        """

        #: The mimetype to use for input/output
        self.mimetype = mimetype

        #: Decode the response from the server? If not
        #: ``mimetype=='application/json'``, this will raise an exception if
        #: ``True``.
        self.decode_output = decode_output

        if decode_output and mimetype != 'application/json':
            raise ValueError('decode_output only works with application/json mimetype.')
        auth = BasicAuth(username, password)
        super(BibResource, self).__init__(uri=url, filters=[auth])

    def _removeheader(self, headers, header):
        """
        Remove header
        """
        for key in headers:
            if key.lower() == header:
                del headers[key]
                return

    def request(self, method='GET', body=None, headers=None, params_dict=None, **kwargs):
        if headers:
            if not isinstance(headers, dict):
                raise ValueError('"headers" must be a dict or None')
            self._removeheader(headers, 'accept')
        else:
            headers = {}
        headers['accept'] = self.mimetype
        response = super(BibResource, self).request(method=method, body=body,
                                                    headers=headers,
                                                    params_dict=params_dict,
                                                    **kwargs)
        return self.decode(response.body_string())

    def post(self, requestdata):
        """
        Perform HTTP POST request with ``requestdata`` in the request body and
        :obj:`.mimetype` in the ``Accept`` header.

        :param requestdata:
            Bytestring encoded with as :obj:`.mimetype`.
        """
        return super(BibResource, self).post(payload=requestdata)

    def put(self, requestdata):
        """
        Perform HTTP PUT request with ``requestdata`` in the request body and
        :obj:`.mimetype` in the ``Accept`` header.

        :param requestdata:
            Bytestring encoded with as :obj:`.mimetype`.
        """
        return super(BibResource, self).put(payload=requestdata)

    def encode(self, data):
        """
        JSON-encode ``data``.
        """
        return json.dumps(data)

    def decode(self, data):
        """
        If :obj:`.decode_output` is True, decode decode the response and return
        a Python datastructure. If :obj:`.decode_output` is False, return
        ``data``.
        """
        if self.decode_output:
            return json.loads(data)
        else:
            return data


class BibFolder(BibResource):
    """
    Bibliography folder REST API.
    """
    def __init__(self, username, password, folderurl=folderurl, **kwargs):
        url = urljoin(folderurl, '@@rest')
        super(BibFolder, self).__init__(url, username, password, **kwargs)

    def _check_search_paramcount(self, *params):
        paramcount = 0
        for param in params:
            if bool(param):
                paramcount += 1
        if paramcount > 1:
            warn('Providing more than one parameter to BibFolder.search() makes no sense because only the first one is used in this order: simula_author_usernames,author_names,search.')

    def _parse_commalist(self, namelist, attrname):
        if namelist:
            if not isinstance(namelist, (list,tuple)):
                raise ValueError('"{0}" must be list or tuple'.format(attrname))
            return ','.join(namelist)
        else:
            return None

    def search(self, simula_author_usernames=[], author_names=[], search='', itemids=[]):
        """
        Perform HTTP GET to search the publication catalog. The default is to
        return all publications, however the results can be limited using the
        parameters below. Only the first search limiting parameter that is not
        ``bool(False)`` is used, and they are checked in the order they are
        listed.

        :param simula_author_usernames:
            List of author Plone usernames.
            Matches exact usernames (no fuzzy searching).
            E.g.: ``['hpl', 'griff']``
        :param author_names:
            List of author names. E.g.: ``['Griwodz C', 'Langtangen H']``
        :param search:
            Free text search. Searches the SearchableText index.
            E.g: ``"addresses the problem of managing an evolving"``
        :param itemids:
            Search for one or more item IDs.
            Matches the given itemids exactly (no fuzzy searching).
            E.g.: ``['Simula.010', 'Simula.002']``
        """

        self._check_search_paramcount(simula_author_usernames, author_names, search)
        simula_author_usernames = self._parse_commalist(simula_author_usernames, 'simula_author_usernames')
        author_names = self._parse_commalist(author_names, 'author_names')
        itemids = self._parse_commalist(itemids, 'itemids')
        params = dict(simula_author_usernames=simula_author_usernames,
                      author_names=author_names,
                      search=search,
                      itemids=itemids)
        return self.get(params_dict=params)

    def create_item(self, id, portal_type, **attributes):
        """
        Perform HTTP POST to create a bibliography item within this folder.

        .. note::
            This is a very thin wrapper around :meth:`.post`. See the
            source for this method (link on the right hand side) to see what it does.

        :param id: ID (short name) of the new item.
        :param portal_type: The portal_type of the bibliography item.
        :param attributes: Attributes for the new item.
        """
        data = dict(portal_type=portal_type, attributes=dict(id=id))
        data['attributes'].update(attributes)
        return self.post(self.encode(data))

    def bulk_update(self, items, pretend=False):
        """
        Perform HTTP PUT to update many items.

        .. note::
            This is a very thin wrapper around :meth:`.put`. See the
            source for this method (link on the right hand side) to see what it does.

        :param items:
            List of items to update.
        :pretend:
            Just pretend to make the changes? If ``True``, no changes are made
            to the database, however the response will still be just as if we
            used ``pretend=False``.
        """
        data = dict(parameters=dict(pretend=pretend),
                    items=items)
        return self.put(self.encode(data))


class BibItem(BibResource):
    """
    Bibliography item (e.g.: ArticleReferece, PhdThesis, Book, ...) REST API.
    """
    def __init__(self, itemid, username, password, folderurl=folderurl, **kwargs):
        """
        :param itemid:
            The id of the bibliography item.
        """
        url = urljoin(folderurl, itemid, '@@rest')
        super(BibItem, self).__init__(url, username, password, **kwargs)

    def get(self):
        """
        Perform HTTP GET to get the bibliography item.
        """
        return super(BibItem, self).get()

    def update(self, portal_type, portal_state=None, **attributes):
        """
        Perform HTTP PUT to update the item bibliography item.

        .. note::
            This is a very thin wrapper around :meth:`.put`. See the
            source for this method (link on the right hand side) to see what it does.

        :param portal_state: Change the state of the bibitem. When an item is
            created, its state is ``private``. Any request changing or getting the
            item includes ``portal_state_transitions``, which describes the next possible
            states.
        :param portal_type: The portal_type for the bibliography item.
        :param attributes: Attributes to update.
        """
        kw = {'attributes': attributes}
        if portal_state:
            kw['portal_state'] = portal_state
        params = dict(portal_type=portal_type, **kw)
        return self.put(self.encode(params))

    def request_approval_from_coauthors(self, portal_type):
        """
        Shortcut for ``update(portal_state='submit')``.
        """
        return self.update(portal_type, portal_state='submit')

    def publish_internally(self, portal_type):
        """
        Shortcut for ``update(portal_state='publish_internally')``.
        """
        return self.update(portal_type, portal_state='publish_internally')

    def get_browser_deleteurl(self):
        """
        Returns the URL for the confirm-delete view for this bibliography item
        on the website.
        """
        return self.uri.replace('@@rest', 'delete_confirmation')

    def browser_confirm_delete(self):
        """
        Open a webbrowser tab on the :meth:`get_browser_deleteurl`.
        This view asks the user to confirm if they want to delete the
        item or not.
        """
        import webbrowser
        webbrowser.open_new_tab(self.get_browser_deleteurl())
