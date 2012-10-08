import urllib2

username_to_realname = None

def _fetch_authors() :
  global username_to_realname

  if username_to_realname is None :
    username_to_realname = {}

    # This is a very temporary solution
    remotefile = urllib2.urlopen('http://folk.uio.no/benjamik/cbc_authors.txt')
    for line in remotefile :
      if not line.strip() or line.strip()[0] == "#" :
        continue
      realname, username  = line.split(":")
      username_to_realname[username.strip()] = realname.strip()


def put_authors(authors) :
  raise NotImplementedError

def is_cbc_author(username) :
  _fetch_authors()

  return username_to_realname.has_key(username)

def get_realname(username) :
  _fetch_authors()

  return username_to_realname[username]


def get_username(real_name) :
  raise NotImplementedError
  
