

$(document).ready(function() {
    const components = ['Gearbox', 'Gear', 'Shaft', 'Bearing', 'Motor', 'Pump', 'Valve', 'Compressor', 'Fan', 'Blower', 'Heat Exchanger', 'Cooling Tower', 'Condenser', 'Evaporator', 'Boiler', 'Turbine', 'Generator', 'Transformer', 'Switchgear', 'Circuit Breaker', 'Relay', 'Fuse', 'Battery', 'Inverter', 'Converter', 'Rectifier', 'Capacitor', 'Resistor', 'Inductor', 'Diode'];
    const componentSelect = $('#component-select');
    componentSelect.empty().append('<option value="">Select Component...</option>');
    components.forEach(component => {
        componentSelect.append(`<option value="${component}">${component}</option>`);
    });

    function updateDropdown(dropdownSelector, items) {
        const list = $(dropdownSelector);
        list.empty(); // Clear existing list items
        items.forEach(item => {
            list.append(`<li>${item}</li>`); // Append new list item for each entry
        });
    }


    const hazards = ['Software Hazard', 'Hardware Hazard', 'Mechanical Hazard', 'Electrical Hazard'];
    const hazardSelect = $('#hazard-select');
    hazardSelect.empty().append('<option value="">Select Hazard...</option>');
    hazards.forEach(hazard => {
        hazardSelect.append(`<option value="${hazard}">${hazard}</option>`);
    });
    
    function updateDropdown(dropdownSelector, items) {
        const list = $(dropdownSelector);
        list.empty(); // Clear existing list items
        items.forEach(item => {
            list.append(`<li>${item}</li>`); // Append new list item for each entry
        });
    }

    function loadDropdown(url, postData, dropdownSelector) {
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(postData),
            success: function(response) {
                updateDropdown(dropdownSelector, response.failure_modes);
            },
            error: function(xhr) {
                alert(`Error fetching data: ${xhr.responseText}`);
            }
        });
    }
   

    $(document).ready(function() {
        $('#generateRiskAnalysisBtn').click(function() {
            // Read the text from the #file-content div
            const inputText = $('#file-content').text().trim(); // Trim to remove extra spaces
    
            if (inputText) {
                $('#loading-message').show(); // Show the loading message
    
                $.ajax({
                    url: '/generate_risk_analysis',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ input_text: inputText }),
                    success: function(response) {
                        $('#failure-mode-select').empty(); // Clear existing list
    
                        if (response.Risk_Analysis_Report) {
                            const reportJson = JSON.parse(response.Risk_Analysis_Report); // Parse the JSON string
                            renderRiskAnalysis(reportJson);
                        } else {
                            $('#failure-mode-select').append(`<li class="list-group-item text-danger">No risk analysis generated.</li>`);
                        }
    
                        $('#loading-message').hide(); // Hide the loading message
                    },
                    error: function(xhr, status, error) {
                        console.error(error);
                        $('#loading-message').hide(); // Hide the loading message on error
                        alert("An error occurred while generating the risk analysis.");
                    }
                });
            } else {
                alert("The file content is empty. Please load the content first.");
            }
        });
    
        function renderRiskAnalysis(report) {
            const container = $('#failure-mode-select');
            container.empty();
    
            // Add intended use and foreseeable misuse
            container.append(`<li class="list-group-item"><strong>Intended Use:</strong> ${report.intended_use}</li>`);
            container.append(`<li class="list-group-item"><strong>Foreseeable Misuse:</strong> ${report.foreseeable_misuse}</li>`);
    
            // Add safety characteristics
            container.append('<li class="list-group-item"><strong>Safety Characteristics:</strong><ul id="safety-characteristics-list"></ul></li>');
            const safetyList = $('#safety-characteristics-list');
            report.safety_characteristics.forEach(characteristic => {
                safetyList.append(`<li>${characteristic}</li>`);
            });
    
            // Render each hazard
            container.append('<li class="list-group-item"><strong>Hazards:</strong><ul id="hazards-list"></ul></li>');
            const hazardsList = $('#hazards-list');
            report.hazards.forEach(hazard => {
                hazardsList.append(`
                    <li class="list-group-item">
                        <strong>Name:</strong> ${hazard.name}<br>
                        <strong>Hazardous Situation:</strong> ${hazard.hazardous_situation}<br>
                        <strong>Risk Estimation:</strong> ${hazard.risk_estimation || "Undefined"}
                    </li>
                `);
            });
        }
    });
    

   
        $('#generateResidualRiskBtn').click(function() {
            const riskControlReport = $('#results').find('p').last().text();  // Assuming the previous report is in <p>
            if (riskControlReport) {
                $('#loading-message-residual').show(); // Show the loading message
                $.ajax({
                    url: '/generate_evaluation_of_overall_residual_risk',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({risk_control_report: riskControlReport}),
                    success: function(response) {
                        $('#results').append('<h3>Evaluation of Overall Residual Risk Report</h3><p>' + response.Evaluation_of_Overall_Residual_Risk_Report + '</p>');
                        $('#loading-message-residual').hide(); // Hide the loading message
                    },
                    error: function(xhr, status, error) {
                        console.error(error);
                        $('#loading-message-residual').hide(); // Hide the loading message even on error
                    }
                });
            } else {
                alert("Please generate the risk control report first.");
            }
        });

        $('#generateRiskEvaluationBtn').click(function() {
            const riskAnalysisItems = [];
            $('#failure-mode-select li').each(function() {
                riskAnalysisItems.push($(this).text());
            });
            const riskAnalysisReport = riskAnalysisItems.join('\n');
        
            console.log("Risk Analysis Items:", riskAnalysisItems); // Detailed debugging
            console.log("Risk Analysis Report:", riskAnalysisReport); // Debugging line
        
            if (riskAnalysisReport.trim() !== "") {
                $('#loading-message-evaluation').show(); // Show the loading message
                $.ajax({
                    url: '/generate_risk_evaluation',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ risk_analysis_report: riskAnalysisReport }),
                    success: function(response) {
                        $('#Evaluations').empty();
                        if (response.Risk_Evaluation_Report) {
                            try {
                                // Remove any backticks or formatting markers from the response
                                const cleanJson = response.Risk_Evaluation_Report.replace(/```json|```/g, '').trim();
                                const evaluationJson = JSON.parse(cleanJson);
                                renderRiskEvaluation(evaluationJson);
                            } catch (error) {
                                console.error("Error parsing JSON:", error);
                                $('#Evaluations').append(`<li class="list-group-item text-danger">Error parsing risk evaluation response.</li>`);
                            }
                        } else {
                            $('#Evaluations').append(`<li class="list-group-item text-danger">No risk evaluation generated.</li>`);
                        }
                        $('#loading-message-evaluation').hide(); // Hide the loading message
                    },
                    error: function(xhr, status, error) {
                        console.error("Error:", error);
                        $('#loading-message-evaluation').hide(); // Hide the loading message even on error
                        alert("An error occurred while generating the risk evaluation.");
                    }
                });
            } else {
                alert("Please generate the risk analysis report first.");
            }
        });
        
        function renderRiskEvaluation(evaluation) {
            const container = $('#Evaluations');
            container.empty();
        
            // Add risk acceptability
            container.append(`<li class="list-group-item"><strong>Risk Acceptability:</strong> ${evaluation.risk_acceptability}</li>`);
        
            // Add risk control measures
            if (evaluation.risk_control_measures && evaluation.risk_control_measures.length > 0) {
                container.append('<li class="list-group-item"><strong>Risk Control Measures:</strong><ul id="control-measures-list"></ul></li>');
                const measuresList = $('#control-measures-list');
                evaluation.risk_control_measures.forEach(measure => {
                    measuresList.append(`<li>${measure.measure} - <strong>Practicability:</strong> ${measure.practicability}</li>`);
                });
            }
        
            // Add residual risk
            container.append(`<li class="list-group-item"><strong>Residual Risk:</strong> ${evaluation.residual_risk}</li>`);
        }
        
        
        $('#device-form').submit(function(event) {
            event.preventDefault();
            const description = $('#device-description').val();
    
            // Show the loading message
            $('#loading-message-json').show();
    
            $.ajax({
                url: '/generate_suggestions',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({description: description}),
                success: function(response) {
                    $('#json-output').text(JSON.stringify(response, null, 2));
                    populateSelect('#component-select', response.components);
                    populateSelect('#hazard-select', response.hazards);
                    // Hide the loading message after the response is received
                    $('#loading-message-json').hide();
                },
                error: function(xhr, status, error) {
                    console.error("Error:", error);
                    $('#json-output').text(`Error: ${error}`);
                    // Hide the loading message even on error
                    $('#loading-message-json').hide();
                }
            });
        });
    

            function populateSelect(selector, items) {
                const select = $(selector);
                select.empty();
                items.forEach(item => {
                    select.append(`<option value="${item}">${item}</option>`);
                });
            }
        

    $('#generateHazardsBtn').click(function() {
        const description = $('#device-description').val();
        const selectedComponent = $('#component-select').val();

        $.ajax({
            url: '/generate_hazards',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({description: description, component: selectedComponent}),
            success: function(response) {
                populateSelect('#hazard-select', response.hazards);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
                $('#json-output').text(`Error: ${error}`);
            }
        });
    });

    function populateSelect(selector, items) {
        const select = $(selector);
        select.empty();
        items.forEach(item => {
            select.append(`<option value="${item}">${item}</option>`);
        });
    }

$('#generateRiskControlBtn').click(function() {
    const riskEvaluationReport = $('#Evaluations').text();
    if (riskEvaluationReport) {
        $('#loading-message-control').show(); // Show the loading message
        $.ajax({
            url: '/generate_risk_control',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({risk_evaluation_report: riskEvaluationReport}),
            success: function(response) {
                $('#risk-control-list').empty();
                response.Risk_Control_Report.split('\n').forEach(function(item) {
                    $('#risk-control-list').append(`<li>${item}</li>`);
                });
                $('#loading-message-control').hide(); // Hide the loading message
            },
            error: function(xhr, status, error) {
                console.error(error);
                $('#loading-message-control').hide(); // Hide the loading message even on error
            }
        });
    } else {
        alert("Please generate the risk evaluation report first.");
    }
});

 $('#generateResidualRiskBtn').click(function() {
        const riskControlReport = $('#results').find('p').last().text();  // Assuming the previous report is in <p>
        if (riskControlReport) {
            $('#loading-message-residual').show(); // Show the loading message
            $.ajax({
                url: '/generate_evaluation_of_overall_residual_risk',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({risk_control_report: riskControlReport}),
                success: function(response) {
                    $('#results').append('<h3>Evaluation of Overall Residual Risk Report</h3><p>' + response.Evaluation_of_Overall_Residual_Risk_Report + '</p>');
                    $('#loading-message-residual').hide(); // Hide the loading message
                },
                error: function(xhr, status, error) {
                    console.error(error);
                    $('#loading-message-residual').hide(); // Hide the loading message even on error
                }
            });
        } else {
            alert("Please generate the risk control report first.");
        }
    });
    $('#generateRiskManagementReviewBtn').click(function() {
        const residualRiskReport = $('#results').find('p').last().text();  // Assuming the previous report is in <p>
        $.ajax({
            url: '/generate_risk_management_review',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({evaluation_of_overall_residual_risk_report: residualRiskReport}),
            success: function(response) {
                $('#results').append('<h3>Risk Management Review Report</h3><p>' + response.Risk_Management_Review_Report + '</p>');
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });

    $('#generatePostProductionBtn').click(function() {
        const riskManagementReviewReport = $('#results').find('p').last().text();  // Assuming the previous report is in <p>
        $.ajax({
            url: '/generate_production_and_post_production_activities',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({risk_management_review_report: riskManagementReviewReport}),
            success: function(response) {
                $('#results').append('<h3>Production and Post Production Activities Report</h3><p>' + response.Production_and_Post_Production_Activities_Report + '</p>');
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });


    $('#textcorrection').click(function() {
        $('#failure-mode-select').attr('contenteditable', 'true').focus(); // Make the text editable and focus on it
    
        // Optional: Add a class to style the editable text if needed
        $('#failure-mode-select').addClass('editable');
    
        var failureModeText = $('#failure-mode-select').text();
        console.log(failureModeText); // Print it out in the console
    
        // Send the text to the Flask app
        $.ajax({
            url: '/text_correction',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({text: failureModeText}),
            success: function(response) {
                console.log('Corrected text:', response.corrected_text);
                // Optionally, you can update the UI with the corrected text
                $('#failure-mode-select').text(response.corrected_text);
            },
            error: function(xhr) {
                alert(`Error correcting text: ${xhr.responseText}`);
            }
        });
    });
    $(document).ready(function () {
        // Function to load the list of .txt files
        function loadFileList() {
          $.ajax({
            url: "/list_txt_files",
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
      
        // Function to load the content of the selected file
        function loadFileContent(filename) {
          $.ajax({
            url: "/read_txt_file/" + filename,
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
              currentAAS = line.replace(
                "Asset Administration Shell Name:",
                ""
              ).trim();
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
            componentDiv.append(
              `<div class="component-title">${component["Component Name"]}</div>`
            );
      
            // Display Asset Administration Shell and Submodel details
            componentDiv.append(
              `<div>Asset Administration Shell: ${component["Asset Administration Shell Name"]}</div>`
            );
            componentDiv.append(
              `<div>Submodel: ${component["Submodel Name"]}</div>`
            );
      
            // Display Properties
            const propertyList = $('<ul></ul>').addClass('property-list');
            component['Properties'].forEach(property => {
              propertyList.append(`<li>${property}</li>`);
            });
            componentDiv.append(propertyList);
      
            const hazardList = $("<ul></ul>").addClass("hazard-list");
      
            component["Hazard Response"].forEach((hazard) => {
              const hazardItem = $("<li></li>").addClass("hazard-item");
              hazardItem.append(
                `<div class="hazard-title">Hazard: ${hazard.hazard}</div>`
              );
              hazardItem.append(`<div>Type: ${hazard.type}</div>`);
              hazardItem.append(`<div>Description: ${hazard.description}</div>`);
              hazardItem.append(
                `<div>Detection Method: ${hazard.detection_method}</div>`
              );
              hazardItem.append(
                `<div>Mitigation Measure: ${hazard.mitigation_measure}</div>`
              );
              hazardItem.append(`<div>Severity: ${hazard.severity || "N/A"}</div>`);
              hazardItem.append(
                `<div>Probability: ${hazard.probability || "N/A"}</div>`
              );
              hazardItem.append(`<div>Risk: ${hazard.risk}</div>`);
      
              hazardList.append(hazardItem);
            });
      
            componentDiv.append(hazardList);
            container.append(componentDiv);
          });
        }
      
        // Load the file list on page load
        loadFileList();
      
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
      
      
    

    // Function to enable text editing
    function enableTextEdit(sectionId, listId) {
        $(sectionId).click(function() {
            $(listId).attr('contenteditable', 'true').focus();
            $(listId).addClass('editable');
        });
    }

    enableTextEdit('#texteditFileContent', '#file-content');
    enableTextEdit('#texteditRiskAnalysis', '#failure-mode-select');
    
    enableTextEdit('#texteditRiskEvaluation', '#Evaluations');
    enableTextEdit('#texteditRiskControl', '#risk-control-list');
    enableTextEdit('#texteditResidualRisk', '#residual-risk-list');
    enableTextEdit('#texteditManagementReview', '#management-review-list');
    enableTextEdit('#texteditProductionActivities', '#production-activities-list');

    // Function to handle AJAX for text correction
    function textCorrection(buttonId, listId, url) {
        $(buttonId).click(function() {
            var text = $(listId).html(); // Use html() to get the inner HTML of the editable element
            console.log("Text before correction:", text); // Debugging line
            
            $.ajax({
                url: url,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({text: text}),
                success: function(response) {
                    console.log('Corrected text:', response.corrected_text);
                    $(listId).html(response.corrected_text); // Update the HTML with the corrected text
                },
                error: function(xhr) {
                    alert(`Error correcting text: ${xhr.responseText}`);
                }
            });
        });
    }

    // Apply the text correction function to each button and list
    textCorrection('#textcorrection', '#failure-mode-select', '/text_correction');
    textCorrection('#texteditRiskEvaluation', '#Evaluations', '/text_correction_risk_evaluation');
    textCorrection('#texteditRiskControl', '#risk-control-list', '/text_correction_risk_control');
    textCorrection('#texteditResidualRisk', '#residual-risk-list', '/text_correction_residual_risk');
    textCorrection('#texteditManagementReview', '#management-review-list', '/text_correction_management_review');
    textCorrection('#texteditProductionActivities', '#production-activities-list', '/text_correction_production_activities');
});
    
