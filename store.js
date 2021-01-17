const store = {
	document: {
		8: { id: 8, report_id: 4, name: "Sample Document", filetype: "txt" },
		34: { id: 34, report_id: 21, name: "Quarterly Report", filetype: "pdf" },
		87: { id: 87, report_id: 21, name: "Performance Summary", filetype: "pdf" },
	},
	page: {
		19: { id: 19, document_id: 34, body: "Lorem ipsum...", footnote: null },
		72: {
			id: 72,
			document_id: 87,
			body: "Ut aliquet...",
			footnote: "Aliquam erat...",
		},
		205: {
			id: 205,
			document_id: 34,
			body: "Donec a dui et...",
			footnote: null,
		},
	},
	report: {
		4: { id: 4, title: "Sample Report" },
		21: { id: 21, title: "Portfolio Summary 2020" },
	},
};

// #1
const mapReportId = data => {
	// Fetch and calculate total pages per document.
	const pages = Object.values(data.page);
	let pageObj = {};

	pages.forEach(page => {
		if (pageObj.hasOwnProperty(page.document_id)) {
			pageObj[page.document_id]++;
		} else {
			pageObj[page.document_id] = 1;
		}
	});

	// Create new document obj with document id, report id, and pages.
	const documents = Object.values(data.document);
	let docObj = {};

	documents.forEach(doc => {
		if (!docObj.hasOwnProperty(doc.id)) {
			docObj[doc.id] = {};
			// Check if pageObj has document id
			// If it does then create new prop 'pages' and assign value from pageObj
			// along with report_id from documents obj.
			if (pageObj.hasOwnProperty(doc.id)) {
				docObj[doc.id]["report_id"] = doc.report_id;
				docObj[doc.id]["pages"] = pageObj[doc.id];
			}
		}
	});

	// Group pages by report id.
	const reports = Object.values(docObj);
	let reportObj = {};

	reports.forEach(report => {
		if (report.report_id) {
			if (!reportObj.hasOwnProperty(report.report_id)) {
				reportObj[report.report_id] = report;
			} else {
				reportObj[report.report_id]["pages"] += report.pages;
			}
		}
	});

	return reportObj;
};

mapReportId(store);
