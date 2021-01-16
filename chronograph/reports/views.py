# from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count, Sum
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
    documents = Document.objects.all();

    total_pages = Page.objects.filter(document_id__in=documents.values('id')) \
        .values('document_id') \
        .annotate(total_pages=Count('document_id'))
    
    pages_with_footnote = Page.objects.filter(footnote__isnull=False) \
        .values('document_id') \
        .annotate(pages_with_fn=Count('document_id'))
    
    combined_pages = []

    for tp_doc in total_pages:
        tp_doc_id = tp_doc['document_id']

        for pwf_doc in pages_with_footnote:
            pwf_doc_id = pwf_doc['document_id']

            if tp_doc_id == pwf_doc_id:
                tp_doc['pages_with_fn'] = pwf_doc['pages_with_fn']
                tp_doc['percentage'] = str(round(pwf_doc['pages_with_fn'] / tp_doc['total_pages'], 2) * 100) + '%'
    
        combined_pages.append(tp_doc)
    
    return JsonResponse(combined_pages, safe=False)

    