from django.utils.translation import gettext as _

DICTIONARY_LIST_API_SUMMARY = _('Obtaining a list of dictionaries.')
DICTIONARY_LIST_API_DESCRIPTION = _(
    'Obtaining a list of dictionaries. An additional option is to retrieve the current ones as of a specified date.',
)

ELEMENTS_LIST_API_SUMMARY = _('Retrieving elements from a given dictionaries.')
ELEMENTS_LIST_API_DESCRIPTION = _(
    'Retrieving elements from a given dictionaries. Can return according to the dictionary version.',
)

ELEMENTS_CHECK_API_SUMMARY = _('Validation an element')
ELEMENTS_CHECK_API_DESCRIPTION = _(
    'Validation of a dictionary element is a check that the item with the given code'
    ' and value is present in the specified version of the dictionary.',  # noqa: WPS326
)

DICTIONARY_ID_PATH_PARAM_DESCRIPTION = _('Dictionary identifier')

DATE_QUERY_PARAM_DESCRIPTION = _(
    'Start date in format YYYY-MM-DD. If not passed, all dictionaries are returned.',
)
VERSION_QUERY_PARAM_DESCRIPTION = _(
    'Version of dictionary.'
    ' If not passed, elements of the current version are returned.'  # noqa: WPS326
    ' The current version is the one whose start date is later than all other versions of '  # noqa: WPS326
    ' the dictionary, but not later than the current date.',  # noqa: WPS326
)
CODE_QUERY_PARAM_DESCRIPTION = _('Code of a dictionary element')
VALUE_QUERY_PARAM_DESCRIPTION = _('Value of a dictionary element')
