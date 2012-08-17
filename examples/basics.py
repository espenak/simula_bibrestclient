from simula_bibrestclient.client import BibFolder, BibItem
from getpass import getpass
from pprint import pprint


def create_pdf():
    ## Normally you would have a PDF on the local disk, in which case you would
    ## do something like this:
    #pdf = BibItem.encode_pdffile('/path/to/my/cool.pdf', 'Testdata')
    ## or:
    #pdf = BibItem.encode_pdf('my.pdf', open('/path/to/my/cool.pdf').read())

    ## But for this example, we just use a simple string
    pdf = BibItem.encode_pdf('my.pdf', 'Testdata')
    return pdf


# Setup our login credentials.
auth = dict(username='griff', password='Simula123')
# Note: you may want to use getpass() to get the password instad of storing it
#       in this file:
#auth = dict(username='grandma', password=getpass())

# We create and update a new ArticleReference with this id/shortname.
# Note that we prefix it with our username so anyone running this script will
# create an article named "<username>-example".
exampleitemid = auth['username'] + '-example'



##################################################
# Work with the folder API
# - search/list
# - create new items in the folder
# - bulk update (update many items in one request)
##################################################

folder = BibFolder(decode_output=True, **auth)

# We can use search() to get bibliography items. If we do not use any
# parameters, ALL simula publications are returned
search_reponse = folder.search(simula_author_usernames=['griff', 'hpl'])
print 'Search for {!r}:'.format(search_reponse['parameters'])
print '    returned {0} items'.format(len(search_reponse['items']))
print '    parameters as they appear to the server:'
print '       ', repr(search_reponse['parameters'])
#pprint(search_reponse) # Pretty-print the entire response


# We can use create_item() to create a new item in the folder
create_response = folder.create_item(exampleitemid, 'ArticleReference',
                                     attributes={'title': 'Example',
                                                 'publication_year': '2012',
                                                 'simula_pdf_file': create_pdf()})
print 'Created {title}'.format(**create_response['attributes'])
print '   View it here: {url}'.format(**create_response)
#pprint(create_response) # Pretty-print the entire response



###############################################
# Work with the item API
# - Get all attributes of a single item
# - Update attributes of an item
# - Delete single item via the web-browser
###############################################

itemid = create_response['attributes']['id']
exampleitem = BibItem(itemid, decode_output=True, **auth)

get_response = exampleitem.get()
print 'Got:', get_response['url']
print '   url:', get_response['url']
print '   portal_type:', get_response['portal_type']
print '   title:', get_response['attributes']['title']
#pprint(get_response) # Pretty-print the entire response


portal_type = get_response['portal_type']
update_response = exampleitem.update(portal_type,
                                     attributes={'title': 'Updated example item using the Python REST client library'})
print 'Updated', update_response['attributes']['id']
print '   new title:', update_response['attributes']['title']
#pprint(update_response) # Pretty-print the entire response


# Open a browser "confirm delete" view to delete the item we created
print 'Opening {delete_url} in your browser...'.format(delete_url=exampleitem.get_browser_deleteurl())
exampleitem.browser_confirm_delete()
