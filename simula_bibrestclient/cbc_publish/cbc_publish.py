#!/usr/bin/env python

from argparse import ArgumentParser
import sys, os, pprint, getpass, itertools
import datetime, dateutil.parser

from simula_bibrestclient.client import BibFolder, BibItem
from simula_bibrestclient.diff import create_diff

import publish
import cbc_authors
from plone_publish import plone_publish_mapping, category_mapping, plone_fields

def build_plone_authors(publish_authors) :
  plone_authors = []

  for author in publish_authors :
    print author
    plone_author = {}
    splitted_author = author.split()
    plone_author["lastname"]  =  splitted_author[-1]
    plone_author["firstnames"] = " ".join(splitted_author[:-1])

    if simula_cbc_guys.has_key(author) :
      plone_author["username"] = simula_cbc_guys[author]

    plone_authors.append(plone_author)

  return plone_authors
      

def publish_to_plone( publish_item ) :
  " Returns item converted to plone format"
  attributes = {}
  attributes.update(publish_item)

  # Remove category from item.
  # NOTE: This must be done before the automatic mapping, since
  # plone has a field category
  category = attributes["category"]
  del attributes["category"]

  # remove id
  # id = attributes["key"]
  # del attributes["key"]

  # remove entrytype
  if attributes.has_key("entrytype") :
    del attributes["entrytype"]
  
  # TODO: Fix handling of duplicates
  if attributes.has_key("duplicate") :
    del attributes["duplicate"]


  for plone_key, publish_key in plone_publish_mapping :
      if attributes.has_key(publish_key) :
        if attributes.has_key(plone_key) :
          raise KeyError("Key '%s' is mapped from publish key '%s', but is already present" % (plone_key, publish_key))
        attributes[plone_key] = attributes[publish_key]
        del attributes[publish_key]


  # capitalize publication status
  attributes["publication_state"] = attributes["publication_state"].capitalize()

  # create authors
  attributes["authors"] = build_plone_authors(attributes["author"])
  del attributes["author"]

  # special handling of pdf urls
  # FIXME
  

  if attributes.has_key("pdf_url") and attributes["pdf_url"] == "missing" :
    del attributes["pdf_url"]

  # FIXME: How to handle pdf files
  attributes["uploaded_pdfFile_visibility"] = "private"

  # validate date fields
  for date_field in ("from_date", "to_date") :
    if attributes.has_key(date_field) :
      date = dateutil.parser.parse(attributes[date_field])
      # print out date in a format understandable for plone
      attributes[date_field] = date.strftime('%Y-%m-%dT%H:%M:%S')
  
  # FIXME: Ensure cbc affiliation
      


  # determine plone portal type
  portal_type = None
  for (plone_portal_type, publish_category) in category_mapping :
    if category == publish_category :
      portal_type = plone_portal_type
      break
    
  if plone_portal_type is None :
    raise ValueError("Can't map publish category '%s' to plone portal_type" % category)

  # Remove fields not present on plone
  for field in attributes.keys() :
    if not field in plone_fields[portal_type]["fields"] :
      print "Warning: Field '%s' doesn't exist in Plone. Data will be discarded" % field
      del attributes[field]

  return {'portal_type' : plone_portal_type, 
          'attributes'  : attributes}


def validate_plone_item(portal_type, item) :
  fields = plone_fields[portal_type]["fields"]

  for field in item.iterkeys() :
    if not field in fields :
      raise KeyError("Field '%s' is not valid" % field)

  print "Portal_type: %s " % portal_type

  required_fields = plone_fields[portal_type]["required"]
  for required_field in required_fields :
    if not item.has_key(required_field):
      raise ValueError("Field '%s' is required for entries of type '%s'" % (required_field, portal_type))

# Will return (portal_type, itemid) on Plone
def create_plone_item(publish_item, bib_folder, make_public=True) :
  pprint.pprint(publish_item)

  #Creates and uploads a publication to plone
  plone_item = publish_to_plone(publish_item)

  validate_plone_item(portal_type, plone_item)
  pprint.pprint(plone_item)

  # use create_item() to create a new item in the folder
  create_response = folder.create_item(id, portal_type, **plone_item)
  print 'Created {title}'.format(**create_response['attributes'])
  print '   View it here: {url}'.format(**create_response)
  pprint.pprint(create_response)

  # Return the item id on plone
  return (portal_type, create_response['attributes']['id'])

def update_status(auth, portal_type, itemid) :
  print "Updating status of publication"

  print "Auth: %s" % auth
  print "Portal_type: %s" % portal_type
  print "Item id: %s" % itemid
  plone_item = BibItem(itemid, decode_output=True, **auth)

  print "Created BibItem object"

  # Update portal_state to ``submit``, which we can see from the ``title``
  # attribute of ``portal_state_transitions`` is "Request approval from co-authors".
  update_response = plone_item.update(portal_type, portal_state='publish_internally')
  print 'Updated', update_response['attributes']['id']
  print 'The current portal_state is "{portal_state}", and the next possible states are: '.format(**create_response)
  pprint(create_response['portal_state_transitions'])


# Test if we're are able to convert a publication to publish
def portal_type_is_supported(plone_item) :
  return plone_fields.has_key(plone_item["portal_type"])

def plone_to_publish( plone_item ) :
  plone_item = plone_item.copy()

  publish_item = {}

  for plone_key, publish_key in plone_publish_mapping :
    # TODO: Check that key doesn't exist
    if plone_item["attributes"].has_key(plone_key) :
      publish_item[publish_key] = plone_item["attributes"][plone_key].encode('utf8')
      del plone_item["attributes"][plone_key]

  # Handle authors
  publish_item["author"] = []
  for author in plone_item["attributes"]["authors"] :
    publish_author = " ".join( (author["firstnames"], author["lastname"]) )
    publish_item["author"].append(publish_author if type(publish_author) is not unicode else publish_author.encode('utf8'))
  del plone_item["attributes"]["authors"]

  # Handle category
  portal_type = plone_item["portal_type"]
  publish_category = plone_fields[portal_type]["publish_category"]
  publish_item["category"] = publish_category
  del plone_item["portal_type"]

  # Copy the rest of the fields
  for key, value in plone_item["attributes"].iteritems() :
    # Be sure not to overwrite attribute
    if publish_item.has_key(key) :
      print "Skipping plone attribute '%s' as the attribute already exists in publish" % key
      continue

    key = str(key) if type(key) is not unicode else key.encode('utf8')
    value = value  if type(value) is not unicode else value.encode('utf8')

    publish_item[key] = value


  # Delete empty fields
  # NOTE: Can't modify the dictionary while iterating through it
  keys_to_be_deleted = set()
  for key, value in publish_item.iteritems() :
    if not value :
      keys_to_be_deleted.add(key)

  for key in keys_to_be_deleted :
    del publish_item[key]

  return publish_item

def get_publish_database(args) :
  # Open publish database
  database = publish.importing.read_database(args.filename) if args.filename is not None else publish.importing.read_database()

  # Limit to journal papers and refproceedings for now
  # TODO: Remove when done with testing
  database = [ publication for publication in database if publication["category"] in ("articles", "refproceedings") ]

  # Limit database to papers with this author
  author_name = cbc_authors.get_realname(args.username)
  database = [ publication for publication in database if author_name in publication["author"] ]

  return database

def get_BibFolder(auth) :
  folder = BibFolder(decode_output=True, **auth)
  return folder

def ensure_authentication(request_response) :
  if request_response["authenticated_user"] is None :
    print "Not authenticated"
    sys.exit(1)

def import_command(auth, args) :
  print "Importing"

  filename = args.filename if args.filename is not None else publish.config.get("database_filename")

  if os.path.isfile(filename) :
    print "Error: File %s exists. Can't import to existing file" % (filename)
    return

  folder = get_BibFolder(auth)

  print "Searching for publications with '%s' as author" % args.username
  search_response = folder.search(simula_author_usernames=[args.username])

  # FIXME: Check authentication. search_response["authenticated_user"] appears not to exist...
  # if search_response['authenticated_user'] is None :
  #   print "Error: Login failed. Exiting..."    
  #   sys.exit(1)

  print "Number of publications found: %d" % len(search_response["items"])

  if (not search_response.has_key("items") or len(search_response["items"]) == 0) :
    print "Search didn't return anything. Exiting."
    sys.exit(1)

  publish_database = []
  for plone_item in search_response["items"] :
    if portal_type_is_supported(plone_item) :
      publish_database.append(plone_to_publish(plone_item))
    else :
      print "Skipping publication. Portal type '%s' is not supported" %  plone_item["portal_type"]

  text = publish.formats.pub.write(publish_database)
  with open(filename, 'w') as file :
    file.write(text)
  
######### Command line commands ###########
def export_command(auth, args) :
  print "Exporting"

  folder = get_BibFolder(auth)  

  database = get_publish_database(args)

  plone_items = []

  for publication in database :
    plone_items.append(publish_to_plone(publication))


  # Then pretend to update to get the changes that will be applied when we update
  # for real
  pretend_response = folder.bulk_update(pretend=True,
                                        items=plone_items)

  # Ask the user to confirm before bulk updating
  print 'Are you sure you want to make the following changes:'
  print create_diff(current_values['items'], pretend_response['items'])
  if raw_input('Confirm changes (y|N): ') == 'y':
    response = folder.bulk_update(items=items)

    # List the changed items
    print 'Changed items:'
    for item in response['items']:
        print '-', item['url']


def outgoing_command(auth, args) :
  print "Outgoing!" 

  database = get_publish_database(args)

  # build dictionary of publish database
  publish_dict = { publication["key"] : publication for publication in database }

  folder = get_BibFolder(auth)

  print "Searching for publications with '%s' as author" % args.username
  search_response = folder.search(simula_author_usernames=[args.username])

  # build set of ids from the response
  response_ids = { item["attributes"]["id"] for item in search_response["items"] }

  # subtract the search response from the local database
  outgoing = set(publish_dict.keys()).difference(response_ids)

  print "Found %d publications in local database not present in Plone" % len(outgoing)

  if not args.dont_list :
    for key in outgoing :
      publication = publish_dict[key]
      print "%s: %s - %s" % (publication["key"], ", ".join(publication["author"]), publication["title"])


def incoming_command(auth, args) :
  print "Incoming!" 

  database = get_publish_database(args)

  # build set of key from publish database
  publish_ids = { publication["key"] for publication in database }

  print "Searching for publications with '%s' as author" % args.username
  folder = get_BibFolder(auth)
  search_response = folder.search(simula_author_usernames=[args.username])

  # build dict of ids from the response
  response_dict = { item["attributes"]["id"]  : item for item in search_response["items"] }

  # subtract the search response from the local database
  incoming = set(response_dict.keys()).difference(publish_ids)

  print "Found %d publications in Plone not present in local database" % len(incoming)

  if not args.dont_list :
    for key in incoming :
      publication = response_dict[key]
      authors = ["%s %s" % (author["firstnames"], author["lastname"]) for author in publication["attributes"]["authors"]]
      print "(%s) %s : %s" % (key, ", ".join(authors), publication["attributes"]["title"])

def plone_status_command(auth, args) :
  print "Searching for publications with '%s' as author" % args.username
  folder = get_BibFolder(auth)
  search_response = folder.search(simula_author_usernames=[args.username])

  for item in search_response["items"] :
    print "%s (%s) : %s" % (item["attributes"]["id"], item["attributes"]["title"], item["portal_state"])

def makepublic_command(auth, args) :
  print "Warning: The makepublic command is untested!"

  print "Searching for publications with '%s' as author" % args.username
  folder = get_BibFolder(auth)
  search_response = folder.search(simula_author_usernames=[args.username])

  for item in search_response["items"] :
    if item["portal_state"] != "published" :
      print "Found non-public publication"

      if "submit" in [transition['id'] for transition in item["portal_state_transitions"]] :
        print "  Updating status"

        ## Get an API for the created item
        bib_item = BibItem(item["attributes"]["id"], decode_output=True, **auth)

        # FIXME: Check if this works!
        bib_item.request_approval_from_coauthors(item["portal_type"])



  


################### Main ####################
def main(arguments=None, subcommands=[]) :
  parser = ArgumentParser(description="Exchange data between Publish and Simula Plone publication databases")
  parser.add_argument("command", choices=("import", "export", "outgoing", "incoming", "authors", "plone_status", "makepublic"))
  parser.add_argument("--username", "-u", help="Username at Simula")
  parser.add_argument("--password", "-p", help="Password at Simula")
  parser.add_argument("--filename", "-f", help="Filename of publish database")
  parser.add_argument("--dont_list", "-dl", default=False, action="store_true", help="Don't list publications")
  parser.add_argument("--dryrun", "-dr", default=False, action="store_true", help="Don't write to databases (plone or publish")
  args = parser.parse_args()

  # Get username is not given on command line
  if args.username is None :
    args.username = raw_input("Username:")

  # Get password if not given on command line
  if args.password is None :
    args.password = getpass.getpass()

  auth = { "username" : args.username, "password" : args.password }
  
  # Call the function implementing the command
  command_func = args.command+"_command"
  globals()[command_func](auth, args)
