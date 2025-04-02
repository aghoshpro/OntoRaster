// Add this at the top of the file
let queryResults = null;
let queryStartTime;

// Add these utility functions at the top
function easeInOutCubic(x) {
	return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
}

function updateProgressBar(startTime, progressBarFill, executionTime, duration = 10000) {
	const elapsed = performance.now() - startTime;
	const progress = Math.min(elapsed / duration, 0.9); // Max 90% until complete
	const easedProgress = easeInOutCubic(progress) * 100;
	
	progressBarFill.style.width = `${easedProgress}%`;
	executionTime.textContent = `${(elapsed / 1000).toFixed(3)}s`;
}

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

	submitButton.addEventListener("click", async function() {
		const progressBar = document.getElementById('query-progress');
		const progressBarFill = document.getElementById('progress-bar');
		const executionTime = document.getElementById('execution-time');
		
		// Show progress bar
		progressBar.classList.remove('hidden');
		progressBarFill.style.width = '0%';
		
		// Start timer
		const queryStartTime = performance.now();
		
		// Smoother progress animation
		const animationFrame = {id: null};
		const animate = () => {
			updateProgressBar(queryStartTime, progressBarFill, executionTime);
			animationFrame.id = requestAnimationFrame(animate);
		};
		animate();

		const query = sparqlInput.value;
		const regionName = extractRegionName(query);
		try {
			const result = await sparqlClient.execute(query);
			
			// Query complete
			cancelAnimationFrame(animationFrame.id);
			
			// Smooth transition to 100%
			const finalProgress = performance.now();
			const finalAnimation = () => {
				const elapsed = performance.now() - finalProgress;
				const progress = Math.min(elapsed / 300, 1); // 300ms transition to 100%
				const easedProgress = 90 + (progress * 10); // Transition from 90% to 100%
				
				progressBarFill.style.width = `${easedProgress}%`;
				
				if (progress < 1) {
					requestAnimationFrame(finalAnimation);
				} else {
					// Final execution time
					const totalTime = (performance.now() - queryStartTime) / 1000;
					executionTime.textContent = `${totalTime.toFixed(3)}s`;
				}
			};
			requestAnimationFrame(finalAnimation);
			
			console.log("Query result received:", result);
			displayResultTable(result, output1, regionName);
			
			// Trigger event for map visualization with complete results
			const event = new CustomEvent("queryResultsReady", { 
				detail: result 
			});
			document.dispatchEvent(event);
		} catch (error) {
			cancelAnimationFrame(animationFrame.id);
			progressBarFill.style.width = '100%';
			progressBarFill.style.backgroundColor = '#ef4444'; // red for error
			console.error('Query failed:', error);
			output1.innerHTML = `<p class="text-red-500">Error: ${error.message}</p>`;
		}
		
		// Hide progress bar after 3 seconds
		setTimeout(() => {
			progressBar.classList.add('hidden');
		}, 3000);
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
	// Filter out color columns from headers
	const visibleHeaders = headers.filter(header => !header.toLowerCase().includes('color'));
	
	visibleHeaders.forEach((header) => {
		tableHTML += `<th class='border border-gray-300 px-3 py-2 bg-gray-100'>${header}</th>`;
	});
	tableHTML += "</tr></thead><tbody>";

	rows.forEach((row) => {
		tableHTML += "<tr>";
		visibleHeaders.forEach((header) => {
			const value = row[header] ? row[header].value : "";
			let displayValue = value;
			
			// Format WKT values to be more readable in the table
			if (header.toLowerCase().includes('wkt') && value.length > 50) {
				displayValue = `<span class="text-green-600 italic cursor-help tracking-tight" title="${value}">map view</span>`;
			}
			
			tableHTML += `<td class='border border-gray-300 px-3 py-2 text-sm font-medium'>${displayValue}</td>`;
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
