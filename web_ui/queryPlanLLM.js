// queryPlanLLM.js - Simplified version that only explains ontologies
document.addEventListener("DOMContentLoaded", () => {
    addQueryPlanTab();
    
    const explainPlanButton = document.getElementById("generate-query");
    if (explainPlanButton) {
        explainPlanButton.addEventListener("click", explainQueryPlan);
    }
});

function addQueryPlanTab() {
    const editorContainer = document.querySelector(".bg-white.rounded-lg.shadow-md.overflow-hidden");
    if (!editorContainer) return;

    const tabsHTML = `
        <div class="border-b border-gray-200">
            <nav class="flex" aria-label="Tabs">
                <button id="editor-tab" 
                    class="px-4 py-2 text-sm font-medium text-blue-600 border-b-2 border-blue-600">
                    Editor
                </button>
                <button id="plan-tab" 
                    class="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                    Query Plan
                </button>
            </nav>
        </div>
        <div id="editor-content" class="p-3">
            <!-- Existing editor content will be moved here -->
        </div>
        <div id="plan-content" class="p-3 hidden">
            <div class="bg-gray-50 rounded-md p-4">
                <h3 class="text-sm font-medium text-gray-900 mb-2">Query Ontology Analysis</h3>
                <pre id="query-plan-output" class="text-sm text-gray-600 whitespace-pre-wrap"></pre>
            </div>
        </div>
    `;

    const header = editorContainer.querySelector(".bg-blue-500");
    header.insertAdjacentHTML("afterend", tabsHTML);

    // Move existing editor content
    const editorContent = document.getElementById("editor-content");
    const existingContent = editorContainer.querySelector(".p-3");
    if (existingContent && editorContent) {
        while (existingContent.firstChild) {
            editorContent.appendChild(existingContent.firstChild);
        }
        existingContent.remove();
    }

    setupTabHandlers();
}

function setupTabHandlers() {
    const editorTab = document.getElementById("editor-tab");
    const planTab = document.getElementById("plan-tab");
    const editorContent = document.getElementById("editor-content");
    const planContent = document.getElementById("plan-content");

    editorTab.addEventListener("click", () => {
        editorTab.classList.add("text-blue-600", "border-b-2", "border-blue-600");
        planTab.classList.remove("text-blue-600", "border-b-2", "border-blue-600");
        editorContent.classList.remove("hidden");
        planContent.classList.add("hidden");
    });

    planTab.addEventListener("click", () => {
        planTab.classList.add("text-blue-600", "border-b-2", "border-blue-600");
        editorTab.classList.remove("text-blue-600", "border-b-2", "border-blue-600");
        planContent.classList.remove("hidden");
        editorContent.classList.add("hidden");
    });
}

async function explainQueryPlan() {
    const sparqlInput = document.getElementById("sparql-input");
    const planOutput = document.getElementById("query-plan-output");
    
    if (!sparqlInput || !planOutput) return;
    
    const query = sparqlInput.value.trim();
    if (!query) {
        planOutput.textContent = "Please enter a SPARQL query first.";
        return;
    }

    // Show the plan tab
    const planTab = document.getElementById("plan-tab");
    planTab.click();

    // Update UI to show loading state
    planOutput.textContent = "Analyzing query ontologies...";

    try {
        const explanation = await explainOntologies(query);
        planOutput.textContent = explanation;
    } catch (error) {
        console.error("Error explaining query:", error);
        planOutput.textContent = `Error analyzing query: ${error.message}`;
    }
}

async function explainOntologies(query) {
    const modelSelector = document.getElementById("llm-model");
    const selectedModel = modelSelector ? modelSelector.value : "ollama-llama3";

    const prompt = `Analyze this SPARQL query and explain only the ontologies and their relationships:

${query}

Focus on:
1. The ontology prefixes used (e.g., rdfs, geo, etc.)
2. The classes and properties from these ontologies
3. How these ontologies relate to each other in the query

Keep the explanation simple and concise.`;

    try {
        if (selectedModel.startsWith("ollama-")) {
            const modelName = selectedModel.replace("ollama-", "");
            return await getOllamaExplanation(prompt, modelName);
        } else if (selectedModel.startsWith("gpt-")) {
            return await getOpenAIExplanation(prompt, selectedModel, document.getElementById("api-key").value);
        } else if (selectedModel.startsWith("claude-")) {
            return await getClaudeExplanation(prompt, selectedModel, document.getElementById("api-key").value);
        }
    } catch (error) {
        throw new Error(`Failed to get explanation: ${error.message}`);
    }
}

// Export functions that might be needed by other modules
window.queryPlanLLM = {
    explainQueryPlan,
    useThisQuery
};
