"""Mapping between plone and publish representations"""

plone_publish_mapping = (
    ( u'id', 'key'),
    ( u'publication_state', 'status'), # The allowed values here should match in both systems
    ( u'DOI', 'doi'),
    ( u'publication_year', 'year'),
    ( u'pdf_url', 'pdf'),
    ( u'category', 'type'),
)

category_mapping = (
  ( "ArticleReference", "articles" ),
  ( "PhdthesisReference", "theses" ),
  ( "RefereedInproceedingsReference", "refproceedings")
)

plone_fields = { 
  "ArticleReference" : {
    "fields" : set((
       "DOI",
       "abstract",
       "authors",
       "expirationDate",
       "id",
       "identifiers",
       "is_simula_publication",
       "journal",
       "keywords",
       "language",
       "modification_date",
       "note",
       "number",
       "pages",
       "pdf_url",
       "pmid",
       "publication_month",
       "publication_state",
       "publication_url",
       "publication_year",
       "rights",
       "subject",
       "title",
       "uploaded_pdfFile_visibility",
       "volume")),
    "required" : set( ("authors", "publication_state", "publication_year", "title", "uploaded_pdfFile_visibility") ),
    "publish_category" : "articles"
  },

  "PhdthesisReference" : {
    "fields" : set((
       "abstract",
       "address",
       "authors",
       "expirationDate",
       "id",
       "identifiers",
       "is_simula_pubication",
       "isbn",
       "keywords",
       "language",
       "modification_date",
       "note",
       "pdf_url",
       "publication_month",
       "publication_state",
       "publication_type",
       "publication_url",
       "publication_year",
       "publisher_url",
       "rights",
       "school",
       "subject",
       "title",
       "uploaded_pdfFile_visibility")
      ),
    "required" : set(),
    "publish_category" : "thesises"
  },

  "RefereedInproceedingsReference" : {
    "fields" :set((
       "abstract",
       "address",
       "authors",
       "booktitle",
       "category",
       "chapter",
       "edition",
       "editor",
       "expirationDate",
       "from_date",
       "id",
       "identifiers",
       "is_simula_publication",
       "isbn",
       "keywords",
       "language",
       "modification_date",
       "note",
       "number",
       "organization",
       "pages",
       "pdf_url",
       "publication_month",
       "publication_state",
       "publication_url",
       "publication_year",
       "publisher",
       "publisher_url",
       "rights",
       "series",
       "subject",
       "title",
       "to_date",
       "uploaded_pdfFile_visibility",
       "volume")
      ),
    "required" : set(("isbn",)),
    "publish_category" : "refproceedings"
  }
}
