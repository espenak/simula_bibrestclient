from simula_bibrestclient.client import BibFolder, BibItem
from getpass import getpass
from pprint import pprint


def portal_state_updatedmessage(update_response):
    print 'Updated', update_response['attributes']['id']
    print 'The current portal_state is "{portal_state}", and the next possible states are: '.format(**update_response)
    pprint(update_response['portal_state_transitions'])


## Setup our login credentials.
auth = dict(username='griff', password='Simula123')
folder = BibFolder(decode_output=True, **auth)
exampleitemid = auth['username'] + '-pubexample'


## Create the item (it will be private by default)
pdf = BibItem.encode_pdf('my.pdf', 'Testdata')
create_response = folder.create_item(exampleitemid, 'ArticleReference',
                                     attributes={'title': 'Example',
                                                 'publication_year': '2012',
                                                 'authors': [{'firstnames': 'Hans Petter',
                                                              'lastname': 'Langtangen',
                                                              'username': 'hpl'},
                                                             {'username': 'griff',
                                                              'firstnames': 'Carsten',
                                                              'lastname': 'Griwodz'}],
                                                 'simula_pdf_file': pdf})
print 'Created {title}'.format(**create_response['attributes'])
print '   View it here: {url}'.format(**create_response)
print 'The current portal_state is "{portal_state}", and the next possible states are: '.format(**create_response)
pprint(create_response['portal_state_transitions'])


## Get an API for the created item
itemid = create_response['attributes']['id']
exampleitem = BibItem(itemid, decode_output=True, **auth)
portal_type = create_response['portal_type']


## Publish the bibitem internally.
## NOTE: You can skip this step, and directly request approval from co-authors.
update_response = exampleitem.publish_internally(portal_type)
portal_state_updatedmessage(update_response)

## Update portal_state to ``submit``, which we can see from the ``title``
## attribute of ``portal_state_transitions`` is "Request approval from co-authors".
## (commented out by default since testing this will send email to the authors)
#update_response = exampleitem.request_approval_from_coauthors(portal_type)
#portal_state_updatedmessage(update_response)
## NOTE: When all co-authors have approved the publication, the publication will
##       change state to ``published``.


## Open a browser "confirm delete" view to delete the item we created
print 'Opening {delete_url} in your browser...'.format(delete_url=exampleitem.get_browser_deleteurl())
exampleitem.browser_confirm_delete()
