-- #1
SELECT 
	D.ID 
FROM 
	DOCUMENT AS D FULL JOIN PAGE AS P
ON 
	D.ID = P.DOCUMENT_ID 
WHERE 
	DOCUMENT_ID IS NULL;

-- #2
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
	
-- #3
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
	
-- #5
/*

	I can think of 3 options to implement support for commenting feature on reports, documents, and pages.
	
	1. Creating corresponding Comment table for reports, documents, and pages.
	
		It gives you clear way to understand the database structure.
		Also, it provides simple relationship between comment and its parent table,
		which the user can perform and maintain db operation (ex. join) smoothly.
		However, one thing that the user need to think about is that
		certain databases have a limit on the number of tables can be added (ex. MySQL depends on OS constraints on file sizes),
		which the user needs to assess its decision to create tables beforehand.
		
	2. Creating dedicated field for comment inside each schema.
		
		This option will provide a relief from option #1 limitation on the number of tables
		since it does not require to add extra tables for each schema.
		However, some type of field has a limit on the size of value being stored.
		Also, whenever there is a new comment to be saved, some logic need to be implemented from ORM
		in order to update the field. (ex. comma delimited, semi-colon delimited, etc)
	
	3. Creating single comment table with 3 different fields. (for_reports, for_documents, for_pages)
		
		By checking either of one field when the user is saving new comment, 
		it will tell the user that the comment is belong to either reports, documents, or pages.
		From my understanding this is the most efficient way to create a table for comment,
		as if the database is postgres.
	
*/