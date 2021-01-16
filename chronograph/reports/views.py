# from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count
from .models import Report, Document, Page

def get_report_title(request):
    """
    SELECT
        R.TITLE,
        COUNT(*) AS PAGES
    FROM 
        REPORT AS R,
        (
            SELECT 
                D.REPORT_ID
            FROM 
                DOCUMENT AS D FULL JOIN PAGE AS P
            ON 
                D.ID = P.DOCUMENT_ID
            WHERE 
                P.DOCUMENT_ID IS NOT NULL
        ) P
    WHERE
        R.ID = P.REPORT_ID
    GROUP BY
        R.TITLE;
    """
    documents = Document.objects.all();

    pages = Page.objects.filter(document_id__in=documents.values('id'))
    docs_with_pages = documents.filter(id__in=pages.values('document_id'))

    title_with_pages = list(docs_with_pages.values('report__title') \
        .annotate(pages=Count('page')))

    return JsonResponse(title_with_pages, safe=False)