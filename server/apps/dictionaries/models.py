from django.db import models
from django.utils.translation import gettext_lazy as _

_DICTIONARY_CODE_MAX_LENGTH = 100
_DICTIONARY_NAME_MAX_LENGTH = 300
_DICTIONARY_ELEMENT_VERSION_MAX_LENGTH = 50
_DICTIONARY_ELEMENT_CODE_MAX_LENGTH = 100
_DICTIONARY_ELEMENT_VALUE_MAX_LENGTH = 300


class Dictionary(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identifier'))
    code = models.CharField(
        max_length=_DICTIONARY_CODE_MAX_LENGTH,
        unique=True,
        verbose_name=_('Code'),
    )
    name = models.CharField(
        max_length=_DICTIONARY_NAME_MAX_LENGTH,
        verbose_name=_('Name'),
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Dictionary')
        verbose_name_plural = _('Dictionaries')

    def __str__(self) -> str:
        """All django models should have this method."""
        return self.name


class DictionaryVersion(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identifier'))
    dictionary = models.ForeignKey(
        Dictionary,
        on_delete=models.CASCADE,
        verbose_name=_('Dictionary identifier'),
    )
    version = models.CharField(
        max_length=_DICTIONARY_ELEMENT_VERSION_MAX_LENGTH,
        verbose_name=_('Version'),
    )
    date = models.DateField(verbose_name=_('Date'))

    class Meta:
        verbose_name = _('Dictionary version')
        verbose_name_plural = _("Dictionary version's")
        constraints = [
            models.UniqueConstraint(
                fields=['version', 'dictionary_id'],
                name='unique_version_dictionary_id',
            ),
            models.UniqueConstraint(
                fields=['date', 'dictionary_id'],
                name='unique_version_date_dictionary',
            ),
        ]

    def __str__(self) -> str:
        """All django models should have this method."""
        return self.version


class DictionaryElement(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name=_('Identifier'),
    )
    version = models.ForeignKey(
        DictionaryVersion,
        on_delete=models.CASCADE,
        verbose_name=_('Dictionary version identifier'),
    )
    code = models.CharField(
        max_length=_DICTIONARY_ELEMENT_CODE_MAX_LENGTH,
        verbose_name=_('Element code'),
    )
    value = models.CharField(  # noqa: WPS110
        max_length=_DICTIONARY_ELEMENT_VALUE_MAX_LENGTH,
        verbose_name=_('Element value'),
    )

    class Meta:
        verbose_name = _('Dictionary element')
        verbose_name_plural = _("Dictionary element's")
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'version_id'],
                name='unique_code_version_id',
            ),
        ]

    def __str__(self) -> str:
        """All django models should have this method."""
        return self.code
