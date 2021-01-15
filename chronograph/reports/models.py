from django.db import models


class Document(models.Model):
    report = models.ForeignKey('Report', models.DO_NOTHING, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    filetype = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document'


class Page(models.Model):
    document = models.ForeignKey(Document, models.DO_NOTHING, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    footnote = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'page'


class Report(models.Model):
    title = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report'
