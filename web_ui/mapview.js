// mapview.js - Handles WKT geometry visualization on Leaflet map

// Initialize the map when document is loaded
let map = null;

document.addEventListener("DOMContentLoaded", () => {
  // Initialize the map centered on Europe
  map = L.map('map').setView([48.5, 12], 5);
  
  // Add OpenStreetMap tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map);
  
  // Listen for query result events
  document.addEventListener("queryResultsReady", handleQueryResults);
});

// Process query results to find and display WKT geometries
function handleQueryResults(event) {
  // Clear any existing geometries
  clearGeometries();
  
  const results = event.detail;
  if (!results || !results.results || !results.head) {
    console.log("No valid results found to display on map");
    return;
  }
  
  // Find all WKT fields in the results using more flexible pattern matching
  const wktFields = results.head.vars.filter(field => 
    field.toLowerCase().includes('wkt') || 
    field.toLowerCase().endsWith('_wkt') ||
    field.toLowerCase().includes('Wkt') || 
    field.toLowerCase().includes('WKT') || 
    field.toLowerCase().endsWith('geometry')
  );
  
  console.log("Found WKT fields:", wktFields);
  
  if (wktFields.length === 0) {
    console.log("No WKT fields found in query results");
    return;
  }
  
  let foundWktData = false;
  
  // Process each row of results
  results.results.bindings.forEach(row => {
    wktFields.forEach(field => {
      if (row[field] && row[field].value) {
        console.log(`Displaying WKT data from field: ${field}`);
        displayWktOnMap(row[field].value, extractLabelFromResults(results, row));
        foundWktData = true;
        
        // Show the geometry info indicator
        const geometryInfo = document.getElementById('geometry-info');
        if (geometryInfo) {
          geometryInfo.textContent = `Showing geometry from ${field}`;
          geometryInfo.classList.remove('hidden');
        }
      }
    });
  });
  
  if (!foundWktData) {
    console.log("No WKT data values found in matching fields");
  }
}

// Try to extract a meaningful label from the results
function extractLabelFromResults(results, row) {
  // Look for common label fields
  const labelFields = ['regionName', 'name', 'label', 'title', 'id'];
  
  for (const field of labelFields) {
    if (row[field] && row[field].value) {
      return row[field].value;
    }
  }
  
  // If no label field, check if there's an answer field
  if (row['answer'] && row['answer'].value) {
    return `Value: ${row['answer'].value}`;
  }
  
  // Default label
  return 'Geographic Feature';
}

// Clear existing geometries from the map
function clearGeometries() {
  if (!map) return;
  
  map.eachLayer(layer => {
    // Only remove GeoJSON layers, keep the base tile layer
    if (layer instanceof L.GeoJSON) {
      map.removeLayer(layer);
    }
  });
  
  // Hide the geometry info indicator
  const geometryInfo = document.getElementById('geometry-info');
  if (geometryInfo) {
    geometryInfo.classList.add('hidden');
  }
}

// Display WKT geometry on the map
function displayWktOnMap(wktString, label) {
  if (!map) return;
  
  try {
    console.log(`Processing WKT: ${wktString.substring(0, 50)}...`);
    
    // Convert WKT to GeoJSON using Wicket library
    const wkt = new Wkt.Wkt();
    wkt.read(wktString);
    const geojson = wkt.toJson();
    
    // Add GeoJSON to map with styling
    const layer = L.geoJSON(geojson, {
      style: {
        color: '#3388ff',
        weight: 3,
        opacity: 0.7,
        fillColor: '#3388ff',
        fillOpacity: 0.9
      },
      pointToLayer: function(feature, latlng) {
        return L.circleMarker(latlng, {
          radius: 8,
          fillColor: '#ff7800',
          color: '#000',
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8
        });
      }
    }).addTo(map);
    
    // Add popup with label
    layer.bindPopup(label);
    
    // Fit map bounds to the geometry
    map.fitBounds(layer.getBounds(), {
      padding: [50, 50],
      maxZoom: 16
    });
    
    console.log("Successfully displayed geometry on map");
    
  } catch (error) {
    console.error('Error displaying WKT on map:', error);
  }
}

// Modify the existing displayResultTable function to work with this module
function processWktFromResults(result) {
  // Find any fields ending with "Wkt" in the result
  if (!result || !result.head || !result.head.vars) return;
  
  const wktFields = result.head.vars.filter(field => field.endsWith('Wkt'));
  
  if (wktFields.length === 0) return;
  
  // Process each row that has WKT data
  result.results.bindings.forEach(row => {
    wktFields.forEach(field => {
      if (row[field] && row[field].value) {
        displayWktOnMap(row[field].value);
      }
    });
  });
} 