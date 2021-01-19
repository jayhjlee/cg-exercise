# pylint: disable=maybe-no-member

from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count, FloatField
from django.db.models.functions import Cast
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

    documents = Document.objects.all()

    pages = Page.objects.filter(document_id__in=documents.values('id'))
    docs_with_pages = documents.filter(id__in=pages.values('document_id'))

    title_with_pages = list(docs_with_pages.values('report__title') \
        .annotate(pages=Count('page')))

    return JsonResponse(title_with_pages, safe=False)


def get_pages_with_fn_pct(request):
    """
    SELECT
        TP.DOC_ID,
        TP.TOTAL_PAGES,
        PWF.PAGES_WITH_FN,
        ROUND(PWF.PAGES_WITH_FN / TP.TOTAL_PAGES::NUMERIC, 2) PERCENTAGE
    FROM
        (
            SELECT 
                D.ID AS DOC_ID,
                COUNT(*) AS TOTAL_PAGES
            FROM
                DOCUMENT D,
                PAGE P
            WHERE
                D.ID = P.DOCUMENT_ID
            GROUP BY
                DOC_ID
            ORDER BY
                DOC_ID ASC
        ) TP,
        (
            SELECT
                P.DOCUMENT_ID AS PAGE_DOC_ID,
                COUNT(*) PAGES_WITH_FN
            FROM
                PAGE P
            WHERE
                P.FOOTNOTE IS NOT NULL
            GROUP BY
                PAGE_DOC_ID
            ORDER BY
                PAGE_DOC_ID
        ) PWF
    WHERE
        TP.DOC_ID = PWF.PAGE_DOC_ID
    GROUP BY
        TP.DOC_ID,
        TP.TOTAL_PAGES,
        PWF.PAGES_WITH_FN;
    """
    
    documents = Document.objects.all()

    pages = Page.objects.filter(document_id__in=documents.values('id')) \
        .values('document_id') \
        .annotate(pages_with_fn=Count('footnote')) \
        .annotate(total_pages=Count('document_id')) \
        .annotate(fn_ratio=Cast(Count('footnote'), FloatField()) / Cast(Count('document_id'), FloatField()))
    
    for page in pages:
        page['fn_ratio'] = str(round(page['fn_ratio'], 2) * 100) + "%"

    return JsonResponse(list(pages), safe=False)

    