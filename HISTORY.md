# History


## Version 1.0.4

- Added ``pretend``-support to all of the methods that change the database.
  Note that this is only a client change, the API already supported pretend.

## Version 1.0.3

- Changed ``BibFolder.create_item`` and ``BibItem.update`` to get
  ``attributes`` as a dict instead of kwargs.
  See 13406b0cfe35fd8ff557eadc0a86cbd754c44129 for more details.
- Added support in ``BibItem.update(...)`` for ``portal_state``, including the
  ``request_approval_from_coauthors(...)`` and ``publish_internally(...)`` shortcut
  methods.
- Added ``get_restapi_url()`` and ``get_website_url()`` to ``BibFolder`` and ``BibItem``.


## Version 1.0.2

- Early beta version.
