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
		// Below is my test data...
		208: {
			id: 208,
			document_id: 8,
			body: "Sample page re",
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

// #2
const searchReport = searchStr => {
	searchStr = searchStr.toLowerCase();

	const { report, document, page } = store;

	const reports = Object.values(report);
	const documents = Object.values(document);
	const pages = Object.values(page);

	// Map report id to the each page object.
	pages.forEach(page => {
		page["report_id"] = document[page.document_id]["report_id"];
	});

	// Create single array to search for the reports.
	const combinedData = reports.concat(documents).concat(pages);

	let reportObj = {};

	combinedData.forEach(data => {
		for (key in data) {
			// Check if key !== 'filetype and the type of value is a string.
			if (key !== "filetype" && typeof data[key] === "string") {
				// Match case with search string.
				if (data[key].toLowerCase().search(searchStr) !== -1) {
					// Since combinedData is a combination of report, document and page from store,
					// some of them are actual report object.
					// My thought process to check whether the object is NOT a report object is to check if report_id is exists.
					// If there is a report_id exist, that means that the object is NOT a report object.
					// Else it is a report object.
					if (!data.report_id) {
						// Every report object has its own id.
						if (!reportObj.hasOwnProperty(data.id)) {
							reportObj[data.id] = data;
						}
					} else {
						if (!reportObj.hasOwnProperty(data.report_id)) {
							// Fetch report from original store.
							reportObj[data.report_id] = report[data.report_id];
						}
					}
				}
			}
		}
	});

	if (Object.values(reportObj).length) return Object.values(reportObj);

	return "No report found. Please refine your search phrase.";
};

// #3
/**
 * I would add type of category, which is report, document, page in this particular exercise,
 * as an additional search option along with the search option.
 *
 * This way I think it will decrease the number of iteration
 * which will fetch only relevant data from store following the search option.
 */

// This function is almost similar to the function #2..
const enhancedSearch = (searchStr, option) => {
	if (!Object.keys(store).includes(option))
		return "Search option does not matching with db. Please refine your search option.";

	searchStr = searchStr.toLowerCase();

	const selectedData = Object.values(store[option]);

	// Check if option is 'page'.
	if (option === "page") {
		// Map report id to the each page object.
		selectedData.forEach(data => {
			data["report_id"] = store.document[data.document_id]["report_id"];
		});
	}

	let reportObj = {};

	selectedData.forEach(data => {
		for (key in data) {
			// Check if key !== 'filetype and the type of value is a string.
			if (key !== "filetype" && typeof data[key] === "string") {
				// Match case with search string.
				if (data[key].toLowerCase().search(searchStr) !== -1) {
					// Since combinedData is a combination of report, document and page from store,
					// some of them are actual report object.
					// My thought process to check whether the object is NOT a report object is to check if report_id is exists.
					// If there is a report_id exist, that means that the object is NOT a report object.
					// Else it is a report object.
					if (!data.report_id) {
						// Every report object has its own id.
						if (!reportObj.hasOwnProperty(data.id)) {
							reportObj[data.id] = data;
						}
					} else {
						if (!reportObj.hasOwnProperty(data.report_id)) {
							// Fetch report from original store.
							reportObj[data.report_id] = store.report[data.report_id];
						}
					}
				}
			}
		}
	});

	if (Object.values(reportObj).length) return Object.values(reportObj);

	return "No report found. Please refine your search phrase.";
};

console.log(mapReportId(store));
console.log(searchReport("ali"));
console.log(enhancedSearch("re", "page"));
