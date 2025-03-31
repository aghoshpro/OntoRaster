// mapview.js - Handles WKT geometry visualization on Leaflet map using Turf.js

// Initialize the map and layer group when document is loaded
let map = null;
let featureGroup = null;

document.addEventListener("DOMContentLoaded", () => {
    // Initialize the map centered on Europe
    map = L.map('map').setView([48.5, 12], 4);
    
    // Create a feature group to manage all geometries
    featureGroup = L.featureGroup().addTo(map);
    
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
    
    // Find all WKT fields and their corresponding color/label fields
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
    let allFeatures = [];
    
    // Process each row of results
    results.results.bindings.forEach(row => {
        wktFields.forEach(field => {
            if (row[field] && row[field].value) {
                try {
                    // Get color if specified in results
                    const color = row[field + 'Color']?.value || 
                                row['color']?.value || 
                                getRandomColor();
                    
                    // Get label from results
                    const label = extractLabelFromResults(results, row);
                    
                    // Convert WKT to GeoJSON using Wicket
                    const geojson = wktToGeoJSON(row[field].value);
                    if (!geojson) return;
                    
                    // Create and style the feature
                    const layer = createStyledLayer(geojson, color, label, row);
                    if (layer) {
                        // Add to feature group
                        featureGroup.addLayer(layer);
                        allFeatures.push(layer);
                        foundWktData = true;
                        console.log(`Added geometry for ${label}`);
                    }
                } catch (error) {
                    console.error(`Error processing WKT for ${field}:`, error);
                }
            }
        });
    });
    
    if (foundWktData) {
        // Fit map to show all features
        if (allFeatures.length > 0) {
            map.fitBounds(featureGroup.getBounds(), {
                padding: [50, 50],
                maxZoom: 12
            });
        }
        
        // Show the geometry info indicator
        updateGeometryInfo(allFeatures.length);
    } else {
        console.log("No WKT data values found in matching fields");
    }
}

// Convert WKT to GeoJSON using Wicket
// function wktToGeoJSON(wktString) {
//     try {
//         // Create a new Wkt.Wkt instance
//         const wicket = new Wicket.Wkt();
//         wicket.read(wktString);
        
//         // Convert to GeoJSON
//         // const geoJSON = wicket.toJson();
        
//         // Ensure the GeoJSON is in the correct format for Turf
//         return {
//             type: "Feature",
//             geometry: JSON.stringify(wkt.toJson()),
//             properties: {}
//         };
//     } catch (error) {
//         console.error("Error converting WKT to GeoJSON:", error);
//         return null;
//     }
// }

// Convert WKT to GeoJSON without using Wicket library
function wktToGeoJSON(wktString) {
    try {
        // Basic WKT parser for common geometry types
        // Trim any whitespace and get the type and coordinates
        wktString = wktString.trim();
        
        // Extract the geometry type and coordinates
        const typeMatch = wktString.match(/^([A-Z]+)/);
        if (!typeMatch) throw new Error("Invalid WKT format: geometry type not found");
        
        const type = typeMatch[1].toUpperCase();
        
        // Extract coordinates between parentheses
        let coordsText = wktString.substring(type.length).trim();
        if (!coordsText.startsWith('(') || !coordsText.endsWith(')')) {
            throw new Error("Invalid WKT format: coordinates not properly enclosed in parentheses");
        }
        
        // Remove outer parentheses
        coordsText = coordsText.substring(1, coordsText.length - 1);
        
        let coordinates;
        let geoJSONType;
        
        // Parse different geometry types
        switch (type) {
            case 'POINT':
                coordinates = parsePointCoords(coordsText);
                geoJSONType = 'Point';
                break;
                
            case 'LINESTRING':
                coordinates = parseLineStringCoords(coordsText);
                geoJSONType = 'LineString';
                break;
                
            case 'POLYGON':
                coordinates = parsePolygonCoords(coordsText);
                geoJSONType = 'Polygon';
                break;
                
            case 'MULTIPOINT':
                coordinates = parseMultiPointCoords(coordsText);
                geoJSONType = 'MultiPoint';
                break;
                
            case 'MULTILINESTRING':
                coordinates = parseMultiLineStringCoords(coordsText);
                geoJSONType = 'MultiLineString';
                break;
                
            case 'MULTIPOLYGON':
                coordinates = parseMultiPolygonCoords(coordsText);
                geoJSONType = 'MultiPolygon';
                break;
                
            default:
                throw new Error(`Unsupported WKT geometry type: ${type}`);
        }
        
        // Return a GeoJSON Feature
        return {
            type: "Feature",
            geometry: {
                type: geoJSONType,
                coordinates: coordinates
            },
            properties: {}
        };
    } catch (error) {
        console.error("Error converting WKT to GeoJSON:", error);
        return null;
    }
}

// Helper functions to parse different coordinate formats

function parsePointCoords(coordsText) {
    // Format: "X Y" or "X Y Z"
    const coords = coordsText.split(/\s+/).map(parseFloat);
    return coords.length >= 2 ? [coords[0], coords[1]] : null;
}

function parseLineStringCoords(coordsText) {
    // Format: "X1 Y1, X2 Y2, ..."
    return coordsText.split(',').map(pointStr => {
        return pointStr.trim().split(/\s+/).map(parseFloat);
    });
}

function parsePolygonCoords(coordsText) {
    // Format: "(X1 Y1, X2 Y2, ...), (X1 Y1, X2 Y2, ...)" for polygon with holes
    // or "X1 Y1, X2 Y2, ..." for simple polygon
    
    // Check if we have multiple rings (holes)
    if (coordsText.includes('(')) {
        // Extract each ring
        const rings = [];
        let depth = 0;
        let currentRing = '';
        
        for (let i = 0; i < coordsText.length; i++) {
            const char = coordsText[i];
            if (char === '(') {
                depth++;
                if (depth === 1) continue; // Skip the opening paren of the ring
            } else if (char === ')') {
                depth--;
                if (depth === 0) {
                    // End of this ring
                    rings.push(parseLineStringCoords(currentRing));
                    currentRing = '';
                    continue;
                }
            }
            
            if (depth > 0) {
                currentRing += char;
            }
        }
        
        return rings;
    } else {
        // Simple polygon without explicit rings
        return [parseLineStringCoords(coordsText)];
    }
}

function parseMultiPointCoords(coordsText) {
    // Format: "(X1 Y1), (X2 Y2), ..."
    return coordsText.split(/\),\s*\(/).map(pointStr => {
        pointStr = pointStr.replace(/^\(|\)$/g, '');
        return pointStr.trim().split(/\s+/).map(parseFloat);
    });
}

function parseMultiLineStringCoords(coordsText) {
    // Format: "(X1 Y1, X2 Y2, ...), (X1 Y1, X2 Y2, ...)"
    return coordsText.split(/\),\s*\(/).map(lineStr => {
        lineStr = lineStr.replace(/^\(|\)$/g, '');
        return parseLineStringCoords(lineStr);
    });
}

function parseMultiPolygonCoords(coordsText) {
    // Format: "((X1 Y1, X2 Y2, ...), (hole)), ((X1 Y1, X2 Y2, ...), (hole))"
    const polygons = [];
    let depth = 0;
    let currentPolygon = '';
    
    for (let i = 0; i < coordsText.length; i++) {
        const char = coordsText[i];
        if (char === '(') {
            depth++;
            if (depth === 1) {
                // Starting a new polygon
                currentPolygon = '';
                continue;
            }
        } else if (char === ')') {
            depth--;
            if (depth === 0) {
                // End of a polygon
                polygons.push(parsePolygonCoords(currentPolygon));
                continue;
            }
        }
        
        if (depth > 0) {
            currentPolygon += char;
        }
    }
    
    return polygons;
}

// Create styled layer with popup and centroid marker
function createStyledLayer(geojson, color, label, properties) {
    try {
        // Create the main geometry layer
        const layer = L.geoJSON(geojson, {
            style: {
                color: '#000',
                weight: 2,
                opacity: 1,
                fillColor: color,
                fillOpacity: 0.9
            },
            pointToLayer: (feature, latlng) => {
                return L.circleMarker(latlng, {
                    radius: 8,
                    fillColor: color,
                    color: '#000',
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                });
            }
        });

        // Calculate and add centroid marker
        // try {
        //     // Calculate centroid using Turf.js
        //     const centroid = turf.centroid(geojson);
        //     const latLng = [
        //         centroid.geometry.coordinates[1], 
        //         centroid.geometry.coordinates[0]
        //     ];

        //     // Create marker at centroid
        //     const marker = L.marker(latLng, {
        //         title: label,
        //         riseOnHover: true
        //     });

        //     // Create popup content for the marker
        //     const markerPopupContent = `
        //         <div class="text-center">
        //             <strong>${label}</strong>
        //             <br>
        //             <small class="text-gray-500">Centroid</small>
        //         </div>
        //     `;
        //     marker.bindPopup(markerPopupContent);

        //     // Add marker to the feature group
        //     featureGroup.addLayer(marker);

        //     // Add hover interaction between geometry and marker
        //     layer.on('mouseover', () => {
        //         marker.openPopup();
        //     });
        //     layer.on('mouseout', () => {
        //         marker.closePopup();
        //     });
        // } catch (error) {
        //     console.error("Error creating centroid marker:", error);
        // }

        // Add popup with properties to the main geometry
        const popupContent = createPopupContent(properties, label);
        layer.bindPopup(popupContent);

        // Add hover effect for the main geometry
        layer.on({
            mouseover: (e) => {
                const layer = e.target;
                layer.setStyle({
                    color: '#c90000',
                    weight: 4,
                    opacity: 1,
                    fillOpacity: 0.9
                });
                layer.bringToFront();
            },
            mouseout: (e) => {
                const layer = e.target;
                layer.setStyle({
                    color: '#000',
                    weight: 2
                });
            }
        });

        return layer;
    } catch (error) {
        console.error("Error creating styled layer:", error);
        return null;
    }
}

// Create detailed popup content from properties
function createPopupContent(properties, label) {
    let content = `<div class="popup-content">`;
    content += `<h4 class="font-bold">${label}</h4>`;
    
    // Add all non-WKT properties
    Object.entries(properties).forEach(([key, value]) => {
        if (!key.toLowerCase().includes('wkt') && 
            !key.toLowerCase().includes('color') &&
            !key.toLowerCase().includes('label')) {
            content += `<p><strong>${key}:</strong> ${value.value}</p>`;
        }
    });
    
    content += `</div>`;
    return content;
}

// Update geometry info display
function updateGeometryInfo(featureCount) {
    const geometryInfo = document.getElementById('geometry-info');
    if (geometryInfo) {
        geometryInfo.textContent = `Showing ${featureCount} geographic features`;
        geometryInfo.classList.remove('hidden');
    }
}

// Clear existing geometries from the map
function clearGeometries() {
    if (featureGroup) {
        featureGroup.clearLayers();
    }
    
    const geometryInfo = document.getElementById('geometry-info');
    if (geometryInfo) {
        geometryInfo.classList.add('hidden');
    }
}

// Generate a random color for features without specified colors
function getRandomColor() {
    const colors = [
        '#008AFF5C '
    ];
    return colors[Math.floor(Math.random() * colors.length)];
}

// Extract label from results
function extractLabelFromResults(results, row) {
    const labelFields = [
        'distWktLabel', 'distName', 'regionName', 
        'name', 'label', 'title', 'id'
    ];
    
    for (const field of labelFields) {
        if (row[field] && row[field].value) {
            return row[field].value;
        }
    }
    
    if (row['elevation'] && row['elevation'].value) {
        return `Elevation: ${row['elevation'].value}m`;
    }
    
    if (row['answer'] && row['answer'].value) {
        return `Value: ${row['answer'].value}`;
    }
    
    return 'Geographic Feature';
}

// Make map instance available globally
window.map = map; 