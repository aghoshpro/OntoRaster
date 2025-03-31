// Add this at the top of the file
let queryResults = null;

class SPARQLClient {
	constructor(endpoint) {
		this.endpoint = endpoint;
	}

	execute(sparql) {
		console.log("Executing SPARQL query:", sparql);

		const requestBody =
			"query=" +
			encodeURIComponent(sparql) +
			"&Accept=" +
			encodeURIComponent("application/sparql-results+json");

		return fetch(this.endpoint, {
			method: "POST",
			mode: "cors",
			headers: new Headers({
				"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			}),
			body: requestBody,
		}).then((response) => response.json());
	}
}

document.addEventListener("DOMContentLoaded", () => {
	const submitButton = document.getElementById("submit-query");
	const sparqlInput = document.getElementById("sparql-input");
	const output1 = document.getElementById("output-1");

	submitButton.addEventListener("click", () => {
		const query = sparqlInput.value;
		const regionName = extractRegionName(query);
		sparqlClient
			.execute(query)
			.then((result) => {
				console.log("Query result received:", result);
				displayResultTable(result, output1, regionName);
				
				// Trigger event for map visualization with complete results
				const event = new CustomEvent("queryResultsReady", { 
					detail: result 
				});
				document.dispatchEvent(event);
			})
			.catch((error) => {
				console.error("Error executing query:", error);
				output1.innerHTML = `<p class="text-red-500">Error: ${error.message}</p>`;
			});
	});

	// Setup visualization/results tabs
	setupResultsTabs();
});

function setupResultsTabs() {
	const visualizationTab = document.getElementById("visualization-tab");
	const resultsTab = document.getElementById("results-tab");
	const visualizationContent = document.getElementById("visualization-content");
	const resultsContent = document.getElementById("results-content");

	visualizationTab.addEventListener("click", () => {
		// Update tab styles
		visualizationTab.classList.add("text-blue-600", "border-b-2", "border-blue-600");
		resultsTab.classList.remove("text-blue-600", "border-b-2", "border-blue-600");
		resultsTab.classList.add("text-gray-500");
		
		// Show/hide content
		visualizationContent.classList.remove("hidden");
		resultsContent.classList.add("hidden");
		
		// Trigger map resize to fix any display issues
		if (window.map) {
			window.map.invalidateSize();
		}
	});

	resultsTab.addEventListener("click", () => {
		// Update tab styles
		resultsTab.classList.add("text-blue-600", "border-b-2", "border-blue-600");
		resultsTab.classList.remove("text-gray-500");
		visualizationTab.classList.remove("text-blue-600", "border-b-2", "border-blue-600");
		
		// Show/hide content
		resultsContent.classList.remove("hidden");
		visualizationContent.classList.add("hidden");
	});
}

function extractRegionName(query) {
	const match = query.match(/\?regionName\s*=\s*['"]([^'"]+)['"]/);
	return match ? match[1] : "Unknown";
}

function displayResultTable(result, container, regionName) {
	if (
		!result.results ||
		!result.results.bindings ||
		result.results.bindings.length === 0
	) {
		container.innerHTML = "<p class='text-gray-500 italic'>No results found.</p>";
		return;
	}

	const headers = result.head.vars;
	const rows = result.results.bindings;

	let tableHTML = "<table class='w-full border-collapse'><thead><tr>";
	headers.forEach((header) => {
		tableHTML += `<th class='border border-gray-300 px-3 py-2 bg-gray-100'>${header}</th>`;
	});
	tableHTML += "</tr></thead><tbody>";

	rows.forEach((row) => {
		tableHTML += "<tr>";
		headers.forEach((header) => {
			const value = row[header] ? row[header].value : "";
			let displayValue = value;
			
			// Format WKT values to be more readable in the table
			if (header.toLowerCase().includes('wkt') && value.length > 50) {
				displayValue = `<span class="text-green-600 italic cursor-help" title="${value}">displayed on map</span>`;
			}
			
			tableHTML += `<td class='border border-gray-300 px-3 py-2'>${displayValue}</td>`;
		});
		tableHTML += "</tr>";
	});

	tableHTML += "</tbody></table>";
	container.innerHTML = tableHTML;

	// Store the query results
	queryResults = {
		regionName: regionName,
		value: rows[0]?.answer?.value || "N/A",
	};
	
	// Trigger an event to notify that results are ready
	const eventDetail = {
		head: result.head,
		results: result.results,
		regionName: regionName
	};
	
	console.log("Dispatching queryResultsReady event with data:", eventDetail);
	
	const event = new CustomEvent("queryResultsReady", { 
		detail: eventDetail
	});
	document.dispatchEvent(event);

	// After displaying the table, switch to results tab if there are results
	if (result.results && result.results.bindings && result.results.bindings.length > 0) {
		document.getElementById("results-tab").click();
	}
}

const ENDPOINT = "http://localhost:8082/sparql";
const sparqlClient = new SPARQLClient(ENDPOINT);
