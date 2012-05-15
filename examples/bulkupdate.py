from simula_bibrestclient.client import BibFolder
from simula_bibrestclient.diff import create_diff
from pprint import pprint

auth = dict(username='grandma', password='test')
folder = BibFolder(decode_output=True, **auth)

# Add as many items as you like to this list. We only use a single item here
# (we used example.py to create it).
items = [{'portal_type': 'ArticleReference',
          'attributes': {'id': 'grandma-example',
                   'title': 'Super bulk updated example'}}]


# Lets start with getting the current values for our items,
# just to have values to compare with when asking the 
# user to confirm the changes (below)
itemids = [item['attributes']['id'] for item in items]
current_values = folder.search(itemids=itemids)
#pprint(current_values) # pretty-print response


# Then pretend to update to get the changes that will be applied when we update
# for real
pretend_response = folder.bulk_update(pretend=True,
                                      items=items)
#pprint(pretend_response) # pretty-print response


# Ask the user to confirm before bulk updating
print 'Are you sure you want to make the following changes:'
print create_diff(current_values['items'], pretend_response['items'])
if raw_input('Confirm changes (y|N): ') == 'y':
    response = folder.bulk_update(items=items)

    # List the changed items
    print 'Changed items:'
    for item in response['items']:
        print '-', item['url']
    #pprint(response) # pretty-print reponse
