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

// Define multiple default queries
const DEFAULT_QUERIES = {
	'Query 1': `PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

SELECT ?regionName ?tempK ?regionWkt {
	?region a :Region_ITALY.
	?region rdfs:label ?regionName .
	?region geo:asWKT ?regionWkt .
	?gridCoverage a :Raster .
	?gridCoverage rasdb:rasterName ?rasterName .
	FILTER (CONTAINS(?regionName, 'Vino'))
	FILTER (CONTAINS(?rasterName, 'Tyrol'))
	BIND ('2023-03-03T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
	BIND (rasdb:rasSpatialMinimum(?timeStamp, ?regionWkt, ?rasterName) AS ?tempK)
}`,
	'Query 2': `PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:	 <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX lgdo: <http://linkedgeodata.org/ontology/>
PREFIX rasdb: <https://github.com/aghoshpro/RasterDataCube/>

SELECT ?bldgName ?distName ?elevation ?distWkt ?distWktColor ?bldgWkt ?bldgWktColor {
	?building a lgdo:Church ; rdfs:label ?bldgName ; geo:asWKT ?bldgWkt .
	?region a :District ; rdfs:label ?distName ; geo:asWKT ?distWkt .
	BIND('#008AFF5C' AS ?distWktColor)
	BIND('red' AS ?bldgWktColor)
	FILTER (geof:sfWithin(?bldgWkt, ?distWkt))
	?gridCoverage a :Raster ; rasdb:rasterName ?rasterName .
	FILTER (CONTAINS(?rasterName, 'Elevation')) # NDVI
	BIND ('2000-02-11T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp) # 2022-01-01T00:00:00+00:00
	BIND (rasdb:rasSpatialMinimum(?timeStamp, ?distWkt, ?rasterName) AS ?elevation)
	FILTER(?elevation < 520) # FILTER(?ndvi > 0.35) # NDVI Scale [0.1 (Desert) to >= 1.0 (Forest)]
}`,
	'Query 3': `PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

SELECT ?regionName ?tempK ?regionWkt {
	?region a :Region_SWEDEN .
	?region rdfs:label ?regionName .
	?region geo:asWKT ?regionWkt .
	?gridCoverage a :Raster .
	?gridCoverage rasdb:rasterName ?rasterName .
	FILTER (?regionName = 'Göteborg') # Stockholm, Umeå, Göteborg, Söderköping
	FILTER (CONTAINS(?rasterName, 'Sweden'))
	BIND ('2022-04-05T00:00:00+00:00'^^xsd:dateTime AS ?startTimeStamp)
	BIND ('2022-06-19T00:00:00+00:00'^^xsd:dateTime AS ?endTimeStamp)
	BIND (rasdb:rasTemporalMaximum(?startTimeStamp, ?endTimeStamp , ?regionWkt, ?rasterName) AS ?tempK)
}`,
	'Query 4': `PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

SELECT ?regionName ?tempK ?regionWkt ?regionWktLabel ?regionWktColor {
	?region a :Region_ITALY .
	?region rdfs:label ?regionName .
	?region geo:asWKT ?regionWkt .
	BIND (?regionName AS ?regionWktLabel)
	?gridCoverage a :Raster .
	?gridCoverage rasdb:rasterName ?rasterName .
	#FILTER (?regionName = 'Bolzano')
	FILTER (CONTAINS(?rasterName, 'Tyrol'))
	BIND ('2023-03-03T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
	BIND (rasdb:rasSpatialAverage(?timeStamp, ?regionWkt, ?rasterName) AS ?tempK)
	FILTER(?tempK > 250) .
	BIND( 
		IF(?tempK < 260, "blue" , 
		IF(?tempK < 265, "#008AFF",
		IF(?tempK < 270, "magenta",
		IF(?tempK < 275, "red",
		IF(?tempK < 280, "black",
		"black")))))
		AS ?regionWktColor).
}
GROUP BY ?regionName ?tempK ?regionWkt ?regionWktLabel ?regionWktColor`,
	'Query 5': `PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

SELECT ?regionName ?answer ?regionWkt {
	?region a :Region .
	?region rdfs:label ?regionName .
	?region geo:asWKT ?regionWkt .
	?gridCoverage a :Raster .
	?gridCoverage rasdb:rasterName ?rasterName .
	#FILTER (?regionName = 'Traunstein') # also try with München, Deggendorf, Bayreuth, Würzburg etc.   
	FILTER (CONTAINS(?regionName, 'R'))
	#FILTER(?regionName NOT IN('Traunstein')) (ISSUE with Traunstein)  
	FILTER (CONTAINS(?rasterName, 'Bavaria'))
	BIND ('2023-09-04T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
	BIND (rasdb:rasSpatialAverage(?timeStamp, ?regionWkt, ?rasterName) AS ?answer)
} `,
'Query 6': `PREFIX :	<https://github.com/aghoshpro/OntoRaster/>
PREFIX gn:  <https://www.geonames.org/ontology#>
PREFIX geo:	<http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX rdfs:	<http://www.w3.org/2000/01/rdf-schema#>
PREFIX rasdb:	<https://github.com/aghoshpro/RasterDataCube/>

SELECT ?featureName ?regionName ?tempK ?pointWkt ?regionWkt ?regionWktColor {
	?region a :Region_SWEDEN ; rdfs:label ?regionName ; geo:asWKT ?regionWkt .
	?gname a gn:UNIV; rdfs:label ?featureName ; geo:asWKT ?pointWkt . # UNIV, LKS, RSTN etc.
	?gridCoverage a :Raster ; rasdb:rasterName ?rasterName .
	BIND('#4400ff' AS ?regionWktColor)
	FILTER (geof:sfWithin(?pointWkt, ?regionWkt))
	FILTER (CONTAINS(?regionName, '')) 
	FILTER (CONTAINS(?rasterName, 'Sweden'))
	BIND ('2022-08-24T00:00:00+00:00'^^xsd:dateTime AS ?timeStamp)
	BIND (rasdb:rasSpatialMaximum(?timeStamp, ?regionWkt, ?rasterName) AS ?tempK)
	FILTER(?tempK > 281) .
}`
};

// First, create a function to wrap the textarea with a highlighted display
function createHighlightedQueryEditor(id, query) {
	return `
		<div class="relative">
			<textarea spellcheck="false" id="sparql-input-${id}" 
				class="w-full p-2 border border-gray-800 rounded-md font-mono text-sm h-[550px] focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white text-transparent font-thin caret-red-800"
			>${query}</textarea>
			<pre id="highlighted-${id}" 
				class="absolute top-0 left-0 w-full h-full p-2 pointer-events-none font-bold font-mono text-sm overflow-hidden"
				aria-hidden="true"
			><code>${highlightSPARQL(query)}</code></pre>
		</div>
	`;
}

// Add styles for syntax highlighting
const styles = `
	.keyword { color:rgb(0, 47, 255); }
	.variable { color:rgb(186, 112, 0); }
	.user-input { color:rgb(0, 158, 11); }
	.custom-input { color:rgb(255, 0, 255); }
	.class { color:rgb(255, 0, 0); }
	.prefix-link { color: rgba(0, 47, 255, 0.62);; }
	.comment { color: #808080; font-style: italic; }
	
	
	pre#highlighted {
		white-space: pre-wrap;
		word-wrap: break-word;
		margin: 0;
	}
`;

function highlightSPARQL(query) {
	query = query.replace(/</g, '&lt;').replace(/>/g, '&gt;');

	const comments = /#(?![0-9a-fA-F]{6}\b).*/g; // Matches comments starting with # /#(?![0-9a-fA-F]{6}\b).*/g;  /#.*/g;
            
	// Temporarily replace comments to prevent them from being affected by other highlights
	let commentMatches = [];
	query = query.replace(comments, (match) => {
		commentMatches.push(match);
		return `__COMMENT_PLACEHOLDER_${commentMatches.length - 1}__`;
	});	

	const keywords = /\b(PREFIX|SELECT|WHERE|FILTER|BIND|AS|CONTAINS)\b/g;
	const variables = /\?[a-zA-Z_]\w*/g;
	const userInputs = /'[^']*'/g;
	const customInputs = /\b([a-zA-Z_]\w*:)\b/g;
	const prefixes = /&lt;[^&]*&gt;/g;
	const classes = /:[A-Z]\w+/g;

	query = query
		.replace(keywords, '<span class="keyword">$&</span>')
		.replace(variables, '<span class="variable">$&</span>')
		.replace(userInputs, '<span class="user-input">$&</span>')
		.replace(customInputs, '<span class="custom-input">$&</span>')
		.replace(classes, '<span class="class">$&</span>')
		.replace(prefixes, '<span class="prefix-link">$&</span>')
		.replace(comments, '<span class="comment">$&</span>');

	            // Restore comments, ensuring they override any other syntax
				commentMatches.forEach((comment, index) => {
					query = query.replace(`__COMMENT_PLACEHOLDER_${index}__`, `<span class="comment">${comment}</span>`);
				});
	return query;
}

document.addEventListener("DOMContentLoaded", () => {
	const submitButton = document.getElementById("submit-query");
	const sparqlInput = document.getElementById("sparql-input");
	const output1 = document.getElementById("output-1");

	let queryCount = 1;
	const queryTabs = document.getElementById("query-tabs");
	const queryEditors = document.getElementById("query-editors");
	const addQueryTab = document.getElementById("add-query-tab");
	
	// Clear existing tabs and editors
	queryTabs.innerHTML = '';
	queryEditors.innerHTML = '';

	// Create default query tabs and editors
	Object.entries(DEFAULT_QUERIES).forEach(([tabName, query], index) => {
		// Create tab
		const tab = document.createElement("button");
		tab.className = `px-4 py-2 text-sm font-medium ${index === 0 ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`;
		tab.setAttribute("data-tab", `query-${index + 1}`);
		tab.textContent = tabName;
		queryTabs.appendChild(tab);

		// Create editor with syntax highlighting
		const editor = document.createElement("div");
		editor.id = `query-${index + 1}`;
		editor.className = `query-editor ${index === 0 ? 'active' : 'hidden'}`;
		editor.innerHTML = createHighlightedQueryEditor(index + 1, query);
		queryEditors.appendChild(editor);

		// Add input handler for live syntax highlighting
		const textarea = editor.querySelector(`#sparql-input-${index + 1}`);
		const highlighted = editor.querySelector(`#highlighted-${index + 1}`);
		
		textarea.addEventListener('input', () => {
			const code = textarea.value;
			highlighted.innerHTML = `<code>${highlightSPARQL(code)}</code>`;
		});

		
		// Sync scroll position
		textarea.addEventListener('scroll', () => {
			highlighted.scrollTop = textarea.scrollTop;
			highlighted.scrollLeft = textarea.scrollLeft;
		});
	});

	// Update queryCount to start after default queries
	queryCount = Object.keys(DEFAULT_QUERIES).length;

	// Handle tab switching
	queryTabs.addEventListener("click", (e) => {
		if (e.target.hasAttribute("data-tab")) {
			// Update active tab
			queryTabs.querySelectorAll("button").forEach(btn => {
				btn.classList.remove("text-blue-600", "border-b-2", "border-blue-600");
				btn.classList.add("text-gray-500");
			});
			e.target.classList.add("text-blue-600", "border-b-2", "border-blue-600");
			e.target.classList.remove("text-gray-500");

			// Show active editor
			const editorId = e.target.getAttribute("data-tab");
			queryEditors.querySelectorAll(".query-editor").forEach(editor => {
				editor.classList.remove("active");
				editor.classList.add("hidden");
			});
			document.getElementById(editorId).classList.remove("hidden");
			document.getElementById(editorId).classList.add("active");
		}
	});

	// Add new query tab
	addQueryTab.addEventListener("click", () => {
		queryCount++;
		
		// Add new tab button
		const newTab = document.createElement("button");
		newTab.className = "px-4 py-2 text-sm font-medium text-gray-500";
		newTab.setAttribute("data-tab", `query-${queryCount}`);
		newTab.textContent = `Query ${queryCount}`;
		queryTabs.appendChild(newTab);

		// Add new editor with syntax highlighting
		const newEditor = document.createElement("div");
		newEditor.id = `query-${queryCount}`;
		newEditor.className = "query-editor hidden";
		newEditor.innerHTML = createHighlightedQueryEditor(queryCount, '');
		queryEditors.appendChild(newEditor);

		// Add input handler for the new editor
		const textarea = newEditor.querySelector(`#sparql-input-${queryCount}`);
		const highlighted = newEditor.querySelector(`#highlighted-${queryCount}`);
		
		textarea.addEventListener('input', () => {
			const code = textarea.value;
			highlighted.innerHTML = `<code>${highlightSPARQL(code)}</code>`;
		});

		// Sync scroll position
		textarea.addEventListener('scroll', () => {
			highlighted.scrollTop = textarea.scrollTop;
			highlighted.scrollLeft = textarea.scrollLeft;
		});

		// Activate new tab
		newTab.click();
	});

	// Update submit query handler to use active editor
	document.getElementById("submit-query").addEventListener("click", async function() {
		const activeEditor = queryEditors.querySelector(".query-editor.active textarea");
		if (activeEditor) {
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

			const query = activeEditor.value;
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
		}
	});

	// Setup visualization/results tabs
	setupResultsTabs();

	// Add the styles to the document
	const styleSheet = document.createElement("style");
	styleSheet.textContent = styles;
	document.head.appendChild(styleSheet);
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
