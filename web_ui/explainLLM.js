// explainLLM.js - Handles explanation of query results using various LLM options

let currentQueryDetails = null;
const OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"; // Default Ollama endpoint

// Add Ollama model availability checking
let availableOllamaModels = [];

document.addEventListener("DOMContentLoaded", () => {
  // Get references to relevant elements
  const apiKeyInput = document.getElementById("api-key");
  const explainOutput = document.getElementById("explanation-output");
  
  // Add model selector dropdown to the UI
  addModelSelector();
  
  // Listen for query results to explain
  document.addEventListener("queryResultsReady", (event) => {
    console.log("Query results received for explanation:", event.detail);
    
    // Store the query results for explanation
    currentQueryDetails = event.detail;
    
    // Auto-explain if there's an API key and auto-explain is enabled
    const autoExplain = localStorage.getItem("llm-auto-explain") === "true";
    if (autoExplain && (apiKeyInput.value || isOllamaSelected())) {
      explainQueryResults();
    }
  });
  
  // Add explain button event listener
  const explainButton = document.getElementById("explain-button");
  if (explainButton) {
    explainButton.addEventListener("click", explainQueryResults);
  }
  
  // Save API key to localStorage when it changes
  apiKeyInput.addEventListener("change", () => {
    if (apiKeyInput.value) {
      // Only save non-empty keys
      localStorage.setItem("llm-api-key", apiKeyInput.value);
    }
  });
  
  // Load saved API key if available
  const savedKey = localStorage.getItem("llm-api-key");
  if (savedKey) {
    apiKeyInput.value = savedKey;
  }
  
  // Add the test button for debugging
  setTimeout(() => {
    addTestButton();
  }, 1000);
});

// Add model selector to the UI
function addModelSelector() {
  const container = document.querySelector("#ontology-viewer .p-4");
  
  // Create model selector dropdown
  const modelSelectorHTML = `
    <div class="flex items-center gap-2 mb-3">
      <select id="llm-model" class="flex-1 p-2 border border-gray-300 rounded-md focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
        <!-- Ollama models will be added here -->
        <option value="ollama-llama3">Ollama - Llama 3</option>
        <option value="gpt-3.5-turbo">OpenAI GPT-3.5</option>
        <option value="gpt-4">OpenAI GPT-4</option>
        <option value="claude-3-sonnet">Claude 3 Sonnet</option>
      </select>
      <button id="explain-button" class="bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded-md transition-colors">
        Explain
      </button>
    </div>
    <div class="flex items-center justify-between mb-3">
      <label class="flex items-center text-sm text-gray-600 cursor-pointer">
        <input type="checkbox" id="auto-explain" class="mr-2">
        Auto-explain new results
      </label>
      <button id="refresh-models" class="text-sm text-blue-600 hover:text-blue-800">
        Refresh Models
      </button>
    </div>
  `;
  
  // Insert model selector before API key input
  const apiKeyInput = document.getElementById("api-key");
  apiKeyInput.insertAdjacentHTML("beforebegin", modelSelectorHTML);
  
  // Setup auto-explain checkbox
  const autoExplainCheckbox = document.getElementById("auto-explain");
  autoExplainCheckbox.checked = localStorage.getItem("llm-auto-explain") === "true";
  autoExplainCheckbox.addEventListener("change", () => {
    localStorage.setItem("llm-auto-explain", autoExplainCheckbox.checked);
  });
  
  // Add refresh button handler
  const refreshButton = document.getElementById("refresh-models");
  refreshButton.addEventListener("click", async () => {
    refreshButton.textContent = "Checking...";
    await checkOllamaModels();
    refreshButton.textContent = "Refresh Models";
  });
  
  // Check for available Ollama models
  checkOllamaModels().then(ollamaAvailable => {
    // If Ollama is available, try to auto-select it
    if (ollamaAvailable) {
      const modelSelector = document.getElementById("llm-model");
      // Try to select a saved model first
      const savedModel = localStorage.getItem("llm-model");
      if (savedModel && modelSelector.querySelector(`option[value="${savedModel}"]`)) {
        modelSelector.value = savedModel;
      } else {
        // Otherwise prefer Ollama
        const ollamaOption = modelSelector.querySelector('option[value^="ollama-"]');
        if (ollamaOption) {
          modelSelector.value = ollamaOption.value;
          localStorage.setItem("llm-model", ollamaOption.value);
        }
      }
    }
    
    // Update API key visibility
    apiKeyInput.style.display = isOllamaSelected() ? "none" : "block";
  });
  
  // Save model preference when changed
  const modelSelector = document.getElementById("llm-model");
  modelSelector.addEventListener("change", () => {
    localStorage.setItem("llm-model", modelSelector.value);
    
    // Show/hide API key based on selected model
    apiKeyInput.style.display = isOllamaSelected() ? "none" : "block";
  });
}

// Check if an Ollama model is selected
function isOllamaSelected() {
  const modelSelector = document.getElementById("llm-model");
  return modelSelector && modelSelector.value.startsWith("ollama-");
}

// Get the selected model
function getSelectedModel() {
  const modelSelector = document.getElementById("llm-model");
  return modelSelector ? modelSelector.value : "gpt-3.5-turbo";
}

// Main function to explain query results
async function explainQueryResults() {
  const explainOutput = document.getElementById("explanation-output");
  const apiKeyInput = document.getElementById("api-key");
  
  // Check if we have results to explain
  if (!currentQueryDetails) {
    explainOutput.value = "No query results to explain. Please run a query first.";
    return;
  }
  
  // Update UI to show we're generating an explanation
  // Add at the top of your file with other constants
const LOADING_MESSAGES = [
    "Insights are cooking....",
    "Shh.. magic is happening 🔮.....",
    "Thinking, wanna tea ? ☕..... ",
    "To be or not to be, that's the question 🎭 or is it 🤔.....",
    "Generating insights..."
];

// Helper function to get random message
function getRandomLoadingMessage() {
    const randomIndex = Math.floor(Math.random() * LOADING_MESSAGES.length);
    return LOADING_MESSAGES[randomIndex];
}

//   explainOutput.value = "Generating insights...";
  explainOutput.value = getRandomLoadingMessage(); // Add random message here
  
  try {
    // Build prompt for the LLM
    const prompt = buildExplanationPrompt(currentQueryDetails);
    
    // Select the appropriate LLM based on the model selection
    let explanation;
    let selectedModel = getSelectedModel();
    let fallbackUsed = false;
    
    const tryOllamaFallback = async () => {
      // Check if Ollama is available for fallback
      const ollamaAvailable = await checkOllamaModels();
      if (ollamaAvailable && availableOllamaModels.length > 0) {
        // Use first available model
        const fallbackModel = availableOllamaModels[0];
        console.log(`Falling back to Ollama model: ${fallbackModel}`);
        fallbackUsed = true;
        return await getOllamaExplanation(prompt, fallbackModel);
      }
      return null;
    };
    
    if (selectedModel.startsWith("ollama-")) {
      // Use Ollama (local LLM)
      const modelName = selectedModel.replace("ollama-", "");
      explanation = await getOllamaExplanation(prompt, modelName);
      
      // If explanation failed, check if model exists
      if (explanation && explanation.includes("Error connecting to Ollama")) {
        const fallbackExplanation = await tryOllamaFallback();
        if (fallbackExplanation) {
          explanation = `[Using available model instead] ${fallbackExplanation}`;
        }
      }
    } else if (selectedModel.startsWith("gpt-")) {
      // Use OpenAI
      if (!apiKeyInput.value) {
        // Try Ollama fallback if no API key
        explanation = await tryOllamaFallback();
        if (!explanation) {
          explainOutput.value = "Please enter an OpenAI API key to use GPT models, or select an Ollama model.";
          return;
        }
      } else {
        explanation = await getOpenAIExplanation(prompt, selectedModel, apiKeyInput.value);
      }
    } else if (selectedModel.startsWith("claude-")) {
      // Use Anthropic Claude
      if (!apiKeyInput.value) {
        // Try Ollama fallback if no API key
        explanation = await tryOllamaFallback();
        if (!explanation) {
          explainOutput.value = "Please enter an Anthropic API key to use Claude models, or select an Ollama model.";
          return;
        }
      } else {
        explanation = await getClaudeExplanation(prompt, selectedModel, apiKeyInput.value);
      }
    }
    
    // Display the explanation
    if (fallbackUsed) {
      explainOutput.value = `[Using available Ollama model as fallback]\n\n${explanation || "Failed to generate explanation."}`;
    } else {
      explainOutput.value = explanation || "Failed to generate explanation.";
    }
    
  } catch (error) {
    console.error("Error generating explanation:", error);
    explainOutput.value = `Error: ${error.message}`;
    
    // Try Ollama as last-resort fallback
    try {
      const fallbackExplanation = await tryOllamaFallback();
      if (fallbackExplanation) {
        explainOutput.value = `[Recovered using Ollama fallback]\n\n${fallbackExplanation}`;
      }
    } catch (fallbackError) {
      console.error("Fallback also failed:", fallbackError);
    }
  }
}

// Build a comprehensive prompt for the LLM
function buildExplanationPrompt(queryResults) {
  console.log("Building prompt from query results:", queryResults);
  
  // Handle empty or invalid results
  if (!queryResults || (!queryResults.head && !queryResults.results)) {
    return "Please explain why a SPARQL query might return no results or invalid data format.";
  }
  
  // Extract variables
  let variables = [];
  if (queryResults.head && queryResults.head.vars) {
    variables = queryResults.head.vars;
  }
  
  // Extract values
  let values = [];
  if (queryResults.results && queryResults.results.bindings && queryResults.results.bindings.length > 0) {
    const bindings = queryResults.results.bindings;
    
    bindings.forEach((binding, index) => {
      let rowData = { rowNum: index + 1, columns: [] };
      
      // For each variable, extract its value
      variables.forEach(varName => {
        if (binding[varName]) {
          rowData.columns.push({
            name: varName,
            value: binding[varName].value,
            type: binding[varName].datatype || binding[varName].type || 'unknown'
          });
        }
      });
      
      values.push(rowData);
    });
  }
  
  // Format the prompt
  let prompt = `I need an explanation of this SPARQL query result in simple terms.`;
  
  if (variables.length > 0) {
    prompt += `\n\nThe query retrieved these variables: ${variables.join(', ')}`;
  }
  
  if (values.length > 0) {
    prompt += `\n\nResults:`;
    values.forEach(row => {
      prompt += `\nRow ${row.rowNum}:`;
      row.columns.forEach(col => {
        // For WKT values, truncate them to avoid token waste
        let displayValue = col.value;
        if (col.name.toLowerCase().includes('wkt') && displayValue.length > 50) {
          displayValue = displayValue.substring(0, 47) + '...';
        }
        prompt += `\n  - ${col.name}: ${displayValue}`;
      });
    });
  }
  
  prompt += `\n\nPlease explain in a short paragraph what this data represents and what insights can be drawn from it. If there are geographic features (WKT data), mention what regions are being shown without including the full geometry strings.`;
  
  console.log("Generated prompt:", prompt);
  return prompt;
}

// Get explanation from Ollama
async function getOllamaExplanation(prompt, modelName) {
  try {
    console.log(`Sending request to Ollama API for model: ${modelName}`);
    
    // Create a correctly formatted request for Ollama's API
    const requestData = {
      model: modelName,
      prompt: prompt,
      stream: false
    };
    
    console.log("Request payload:", requestData);
    
    const response = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Ollama API error (${response.status}): ${errorText}`);
    }
    
    const data = await response.json();
    console.log("Ollama response:", data);
    
    if (!data.response) {
      throw new Error("Ollama returned an empty response");
    }
    
    return data.response;
  } catch (error) {
    console.error("Error with Ollama request:", error);
    return `Error using Ollama: ${error.message}. Make sure Ollama is running with model '${modelName}' available.`;
  }
}

// Get explanation from OpenAI
async function getOpenAIExplanation(prompt, modelName, apiKey) {
  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: modelName,
        messages: [
          {
            role: "system",
            content: "You are a helpful assistant that explains SPARQL query results in simple terms."
          },
          {
            role: "user",
            content: prompt
          }
        ],
        temperature: 0.3,
        max_tokens: 500
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || `OpenAI API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error("OpenAI error:", error);
    return `Error connecting to OpenAI: ${error.message}`;
  }
}

// Get explanation from Anthropic Claude
async function getClaudeExplanation(prompt, modelName, apiKey) {
  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: modelName,
        max_tokens: 500,
        messages: [
          {
            role: "user",
            content: prompt
          }
        ]
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || `Claude API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.content[0].text;
  } catch (error) {
    console.error("Claude error:", error);
    return `Error connecting to Claude API: ${error.message}`;
  }
}

// Function to check for available Ollama models
async function checkOllamaModels() {
  try {
    const response = await fetch('http://localhost:11434/api/tags', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      availableOllamaModels = data.models?.map(model => model.name) || [];
      console.log("Available Ollama models:", availableOllamaModels);
      
      // Update the model selector with available models
      updateModelSelector();
      
      return true;
    }
    
    return false;
  } catch (error) {
    console.error("Error checking Ollama models:", error);
    return false;
  }
}

// Update model selector with available Ollama models
function updateModelSelector() {
  const modelSelector = document.getElementById("llm-model");
  if (!modelSelector) return;
  
  // Get current selection to preserve it if possible
  const currentSelection = modelSelector.value;
  
  // Get all option elements that are for Ollama models
  const ollamaOptions = Array.from(modelSelector.querySelectorAll('option'))
    .filter(option => option.value.startsWith('ollama-'));
  
  // Remove existing Ollama options
  ollamaOptions.forEach(option => option.remove());
  
  // Determine if llama3.2 is available
  const hasLlama32 = availableOllamaModels.some(model => 
    model.includes('llama3.2') || model.includes('llama3:2') || model === 'llama3'
  );
  
  // Add available Ollama models
  let ollamaModelsAdded = false;
  availableOllamaModels.forEach(model => {
    const option = document.createElement('option');
    option.value = `ollama-${model}`;
    
    // Create user-friendly display name
    let displayName = model;
    if (model.includes('llama3.2')) {
      displayName = 'Llama 3.2';
    } else if (model.includes('llama3')) {
      displayName = 'Llama 3';
    } else if (model.includes('llama2')) {
      displayName = 'Llama 2';
    } else if (model.includes('deepseek')) {
        displayName = 'DeepSeek R1-8B';
    } else if (model.includes('mistral')) {
      displayName = 'Mistral';
    }
    
    option.textContent = `${displayName}`;
    
    // If this is llama3.2, insert at the top
    if (model.includes('llama3.2') || (model === 'llama3' && !hasLlama32)) {
      modelSelector.insertBefore(option, modelSelector.firstChild);
    } else {
      modelSelector.appendChild(option);
    }
    
    ollamaModelsAdded = true;
  });
  
  // Add a generic Ollama option if no models were found
  if (!ollamaModelsAdded) {
    const option = document.createElement('option');
    option.value = 'ollama-llama3.2';
    option.textContent = 'Llama 3.2';
    modelSelector.appendChild(option);
    
    const option2 = document.createElement('option');
    option2.value = 'ollama-mistral';
    option2.textContent = 'Mistral';
    modelSelector.appendChild(option2);
  }
  
  // Try to restore previous selection, or select first Ollama model
  if (availableOllamaModels.length > 0) {
    if (currentSelection && modelSelector.querySelector(`option[value="${currentSelection}"]`)) {
      modelSelector.value = currentSelection;
    } else {
      // Select first Ollama model by default
      const firstOllamaOption = modelSelector.querySelector('option[value^="ollama-"]');
      if (firstOllamaOption) {
        modelSelector.value = firstOllamaOption.value;
        // Save this as the preference
        localStorage.setItem("llm-model", firstOllamaOption.value);
      }
    }
    
    // Update API key visibility
    const apiKeyInput = document.getElementById("api-key");
    if (apiKeyInput) {
      apiKeyInput.style.display = isOllamaSelected() ? "none" : "block";
    }
  }
}

// Add this function to explainLLM.js 
function testExplanation() {
  currentQueryDetails = {
    head: { vars: ['answer', 'regionName'] },
    results: { 
      bindings: [{ 
        answer: { value: '523.75', type: 'literal' },
        regionName: { value: 'München', type: 'literal' }
      }]
    }
  };
  
  explainQueryResults();
}

// Call this from the browser console to test:
// testExplanation();

// Add a function to add a test button (for debugging)
function addTestButton() {
  const container = document.querySelector("#ontology-viewer .p-4");
  const testButtonHTML = `
    <button id="test-explanation" class="mt-2 text-sm text-gray-600 hover:text-gray-800">
      Test Explanation
    </button>
  `;
  
  container.insertAdjacentHTML("beforeend", testButtonHTML);
  
  document.getElementById("test-explanation").addEventListener("click", () => {
    testExplanation();
  });
}
