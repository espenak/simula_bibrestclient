from pprint import pprint
from simula_bibrestclient.client import BibFolder, BibItem
from simula_bibrestclient.diff import create_diff


# Setup our login credentials.
auth = dict(username='griff', password='Simula123')
exampleitemid = auth['username'] + '-example'
portal_type = 'ArticleReference'


# Create a bibitem
folder = BibFolder(decode_output=True, **auth)
create_response = folder.create_item(exampleitemid, portal_type,
                                     attributes={'title': 'Example',
                                                 'publication_year': '2012'})
print 'Created {title}'.format(**create_response['attributes'])
print '   View it here: {url}'.format(**create_response)
#pprint(create_response) # Pretty-print the entire response



# Get the created bibitem
itemid = create_response['attributes']['id']
exampleitem = BibItem(itemid, decode_output=True, **auth)


# Pretend to update (no changes are stored in the database, but the response is just like it would be on a regular update)
update_attributes = {'title': 'Updated example item using the Python REST client library'}
pretend_update_response = exampleitem.update(portal_type,
                                             attributes=update_attributes,
                                             pretend=True)
print 'Updated using pretend=True. This does not change the database, as you can see by doing a GET-request:'
get_response = exampleitem.get()
print '    Title stored in the database: ', get_response['attributes']['title']
#pprint(pretend_update_response) # Pretty-print the entire response


# Show the user a DIFF between the pretend_update_response and get_response, and ask them to confirm the changes
print 'Are you sure you want to make the following changes to {id}:'.format(**get_response['attributes'])
print create_diff(get_response['attributes'], pretend_update_response['attributes'])
if raw_input('Confirm changes (y|N): ') == 'y':
    # Really update the item (with pretend=False)
    update_response = exampleitem.update(portal_type,
                                         attributes=update_attributes)
    print 'Updated {id}'.format(**update_response['attributes'])
else:
    print 'Update aborted by user'


# Open a browser "confirm delete" view to delete the item we created
print 'Opening {delete_url} in your browser...'.format(delete_url=exampleitem.get_browser_deleteurl())
exampleitem.browser_confirm_delete()
