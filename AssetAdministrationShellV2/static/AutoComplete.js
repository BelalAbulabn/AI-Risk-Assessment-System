$(document).ready(function () {
    let suggestionText = ""; // Track the current suggestion text
    let suggestionActive = false; // Track if a suggestion is currently active

    // Debounce function to limit the rate of API calls
    const debounce = (func, delay) => {
        let debounceTimer;
        return function () {
            const context = this;
            const args = arguments;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(context, args), delay);
        };
    };

    // Fetch autocomplete suggestions from the server
    const fetchSuggestions = debounce(function (element) {
        if (suggestionActive) return; // Do not fetch new suggestions if one is already active

        const inputText = $(element).text().trim();
        const inputId = $(element).attr('id'); // Get the ID of the input element
        let endpoint = '/api/autocomplete'; // Default endpoint
        let additionalContext = ''; // Initialize additional context

        // Collect additional context from previous sections
        switch (inputId) {
            case 'file-content':
                endpoint = '/api/autocomplete_file_content';
                break;
            case 'failure-mode-select':
                endpoint = '/api/autocomplete_failure_mode';
                additionalContext = $('#file-content').text().trim(); // Add content from file-content
                console.log("Additional context for failure-mode-select:", additionalContext); // Debugging output
                break;
            case 'Evaluations':
                endpoint = '/api/autocomplete_evaluations';
                additionalContext = $('#failure-mode-select').text().trim(); // Add content from failure-mode-select
                break;
            case 'risk-control-list':
                endpoint = '/api/autocomplete_risk_control';
                additionalContext = $('#Evaluations').text().trim(); // Add content from Evaluations
                break;
            case 'results':
                endpoint = '/api/autocomplete_results';
                break;
            case 'management-review-list':
                endpoint = '/api/autocomplete_management_review';
                break;
            default:
                endpoint = '/api/autocomplete';
        }

        if (inputText) {
            // Show loading message
            $(element).siblings('.loading-message').show();

            // AJAX request to the determined endpoint
            $.ajax({
                url: endpoint,  // Use determined endpoint
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ text: inputText, additional_context: additionalContext }),
                success: function (response) {
                    $(element).siblings('.loading-message').hide();
                    if (response.suggestion) {
                        suggestionText = response.suggestion;
                        suggestionActive = true; // Mark suggestion as active

                        // Append suggestion to the contenteditable div
                        const suggestionElement = `<span class="suggestion text-muted">${suggestionText}</span>`;
                        $(element).append(suggestionElement);
                    } else {
                        console.log('No suggestion available.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching suggestion:', error);
                    $(element).siblings('.loading-message').hide();
                }
            });
        }
    }, 1000); // Debounce delay of 2 seconds

    // Event listener for input changes in contenteditable elements
    $('.contenteditable').on('input', function () {
        if (suggestionActive) return; // Do not fetch new suggestions if one is already active

        $(this).find('.suggestion').remove();  // Remove previous suggestions
        suggestionText = "";  // Reset suggestion text
        fetchSuggestions(this);  // Fetch new suggestions
    });

    // Handle keydown events for accepting suggestions
    $('.contenteditable').on('keydown', function (event) {
        const suggestionElement = $(this).find('.suggestion');

        if (suggestionElement.length && event.key === 'Tab') {
            event.preventDefault();  // Prevent default Tab behavior

            // Insert the suggestion into the content as normal text
            suggestionElement.replaceWith(document.createTextNode(suggestionText));

            // Move cursor to the end of the content
            const range = document.createRange();
            const selection = window.getSelection();
            range.setStartAfter($(this).contents().last()[0]);
            range.collapse(true);
            selection.removeAllRanges();
            selection.addRange(range);

            suggestionActive = false; // Mark suggestion as inactive
            suggestionText = "";  // Clear suggestion text
        } else if (event.key !== "Backspace" && event.key !== "Delete") {
            // If any other key is pressed and there is an active suggestion, clear the suggestion
            if (suggestionElement.length) {
                suggestionElement.remove();
                suggestionActive = false; // Mark suggestion as inactive
            }
        }
    });
});

function loadFileList() {
    $.ajax({
        url: "/list_txt_files",
        method: "GET",
        success: function(files) {
            const fileSelect = $("#file-select");
            fileSelect.empty(); // Clear existing options
            files.forEach((file) => {
                fileSelect.append(new Option(file, file));
            });
        },
        error: function(error) {
            console.error("Error fetching file list:", error);
        },
    });
}

$(document).ready(function () {
    // Custom parser to convert text format to JSON
    function parseContent(content) {
        const lines = content.split("\n");
        const components = [];
        let currentComponent = null;
        let hazardBlock = "";
        let currentAAS = "";
        let currentSubmodel = "";
        let properties = [];

        lines.forEach((line) => {
            line = line.trim();

            // Capture Asset Administration Shell Name
            if (line.startsWith("Asset Administration Shell Name:")) {
                currentAAS = line.replace("Asset Administration Shell Name:", "").trim();
            }

            // Capture Submodel Name
            if (line.startsWith("Submodel Name:")) {
                currentSubmodel = line.replace("Submodel Name:", "").trim();
            }

            // Capture Properties
            if (line.startsWith("Property Key:")) {
                properties.push(line.replace("Property Key:", "").trim());
            }

            if (line.startsWith("Component Name:")) {
                // Finalize and push the current component if it exists
                if (currentComponent && hazardBlock) {
                    try {
                        // Parse the collected hazard block
                        const hazards = JSON.parse(hazardBlock);
                        currentComponent["Hazard Response"] = hazards;
                    } catch (e) {
                        console.error("Error parsing hazards:", e);
                        // Push raw hazard block as a fallback
                        currentComponent["Hazard Response"] = hazardBlock;
                    }
                    components.push(currentComponent);
                }

                // Start a new component
                currentComponent = {
                    "Component Name": line.replace("Component Name:", "").trim(),
                    "Hazard Response": [],
                    "Asset Administration Shell Name": currentAAS,
                    "Submodel Name": currentSubmodel,
                    "Properties": properties,
                };

                hazardBlock = ""; // Reset hazard block
                properties = []; // Reset properties
            } else if (line.startsWith("Component ID:")) {
                currentComponent["Component ID"] = line.replace("Component ID:", "").trim();
            } else if (line.startsWith("[") || hazardBlock) {
                // Collect lines for the hazard JSON block
                hazardBlock += line;
            }
        });

        // Add the last component if it exists
        if (currentComponent && hazardBlock) {
            try {
                const hazards = JSON.parse(hazardBlock);
                currentComponent["Hazard Response"] = hazards;
            } catch (e) {
                console.error("Error parsing hazards:", e);
                // Push raw hazard block as a fallback
                currentComponent["Hazard Response"] = hazardBlock;
            }
            components.push(currentComponent);
        }

        return components;
    }

    // Function to render file content
    function renderFileContent(components) {
        const container = $("#file-content");
        container.empty();

        components.forEach((component) => {
            const componentDiv = $("<div></div>").addClass("component");
            componentDiv.append(`<div class="component-title">${component["Component Name"]}</div>`);

            // Display Asset Administration Shell and Submodel details
            componentDiv.append(`<div>Asset Administration Shell: ${component["Asset Administration Shell Name"]}</div>`);
            componentDiv.append(`<div>Submodel: ${component["Submodel Name"]}</div>`);

            // Display Properties
            const propertyList = $('<ul></ul>').addClass('property-list');
            component['Properties'].forEach(property => {
                propertyList.append(`<li>${property}</li>`);
            });
            componentDiv.append(propertyList);

            const hazardList = $("<ul></ul>").addClass("hazard-list");

            // Check if Hazard Response is a JSON object or a raw string
            if (Array.isArray(component["Hazard Response"])) {
                // If parsed successfully, render the hazards
                component["Hazard Response"].forEach((hazard) => {
                    const hazardItem = $("<li></li>").addClass("hazard-item");
                    hazardItem.append(`<div class="hazard-title">Hazard: ${hazard.hazard}</div>`);
                    hazardItem.append(`<div>Type: ${hazard.type}</div>`);
                    hazardItem.append(`<div>Description: ${hazard.description}</div>`);
                    hazardItem.append(`<div>Detection Method: ${hazard.detection_method}</div>`);
                    hazardItem.append(`<div>Mitigation Measure: ${hazard.mitigation_measure}</div>`);
                    hazardItem.append(`<div>Severity: ${hazard.severity || "N/A"}</div>`);
                    hazardItem.append(`<div>Probability: ${hazard.probability || "N/A"}</div>`);
                    hazardItem.append(`<div>Risk: ${hazard.risk}</div>`);

                    hazardList.append(hazardItem);
                });
            } else {
                // If parsing failed, display the raw hazard block
                const hazardItem = $("<li></li>").addClass("hazard-item");
                hazardItem.append(`<pre>${component["Hazard Response"]}</pre>`);
                hazardList.append(hazardItem);
            }

            componentDiv.append(hazardList);
            container.append(componentDiv);
        });
    }

    // Load available text files
    function loadFileList() {
        $.ajax({
            url: "/api/list_txt_files", // Ensure correct API endpoint
            method: "GET",
            success: function (files) {
                const fileSelect = $("#file-select");
                fileSelect.empty(); // Clear existing options
                files.forEach((file) => {
                    fileSelect.append(new Option(file, file));
                });
            },
            error: function (error) {
                console.error("Error fetching file list:", error);
            },
        });
    }

    // Load the file list on page load
    loadFileList();

    // Load file content
    function loadFileContent(filename) {
        $.ajax({
            url: "/api/read_txt_file/" + filename, // Ensure correct API endpoint
            method: "GET",
            success: function (data) {
                const parsedData = parseContent(data.content);
                renderFileContent(parsedData);
            },
            error: function (error) {
                console.error("Error fetching file content:", error);
            },
        });
    }

    // Event handler for the Load File button
    $("#loadFileBtn").click(function () {
        const selectedFile = $("#file-select").val();
        if (selectedFile) {
            loadFileContent(selectedFile);
        } else {
            alert("Please select a file to load.");
        }
    });
});

