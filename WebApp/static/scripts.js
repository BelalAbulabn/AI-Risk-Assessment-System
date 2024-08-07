

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
   

    


    $('#component-select').on('change', function() {
        const selectedComponent = $(this).val();
        if (selectedComponent) {
            loadDropdown('select_component', {component: selectedComponent}, '#failure-mode-select');
        }
    });    
    $('#hazard-select').on('change', function() {
        const selectedComponent = $(this).val();
        if (selectedComponent) {
            loadDropdown('select_hazared', {hazared: selectedComponent}, '#failure-mode-select');
        }
    });


    $('#generateRiskAnalysisBtn').click(function() {
        const selectedComponent = $('#component-select').val();
        if (selectedComponent) {
            $('#loading-message').show(); // Show the loading message
            $.ajax({
                url: '/generate_risk_analysis',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({initial_data: selectedComponent}),
                success: function(response) {
                    $('#failure-mode-select').empty();
                    response.Risk_Analysis_Report.split('\n').forEach(function(item) {
                        $('#failure-mode-select').append(`<li>${item}</li>`);
                    });
                    $('#loading-message').hide(); // Hide the loading message
                },
                error: function(xhr, status, error) {
                    console.error(error);
                    $('#loading-message').hide(); // Hide the loading message even on error
                }
            });
        } else {
            alert("Please select a component.");
        }
    });



    // $('#generateRiskEvaluationBtn').click(function() {
    //     const riskAnalysisReport = $('#failure-mode-select').text();
    //     if (riskAnalysisReport) {
    //         $('#loading-message-evaluation').show(); // Show the loading message
    //         $.ajax({
    //             url: '/generate_risk_evaluation',
    //             type: 'POST',
    //             contentType: 'application/json',
    //             data: JSON.stringify({risk_analysis_report: riskAnalysisReport}),
    //             success: function(response) {
    //                 $('#Evaluations').empty();
    //                 response.Risk_Evaluation_Report.split('\n').forEach(function(item) {
    //                     $('#Evaluations').append(`<li>${item}</li>`);
    //                 });
    //                 $('#loading-message-evaluation').hide(); // Hide the loading message
    //             },
    //             error: function(xhr, status, error) {
    //                 console.error(error);
    //                 $('#loading-message-evaluation').hide(); // Hide the loading message even on error
    //             }
    //         });
    //     } else {
    //         alert("Please generate the risk analysis report first.");
    //     }
    // });
   
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
                        response.Risk_Evaluation_Report.split('\n').forEach(function(item) {
                            $('#Evaluations').append(`<li>${item}</li>`);
                        });
                        $('#loading-message-evaluation').hide(); // Hide the loading message
                    },
                    error: function(xhr, status, error) {
                        console.error("Error:", error);
                        $('#loading-message-evaluation').hide(); // Hide the loading message even on error
                    }
                });
            } else {
                alert("Please generate the risk analysis report first.");
            }
        });
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


    // Function to enable text editing
    function enableTextEdit(sectionId, listId) {
        $(sectionId).click(function() {
            $(listId).attr('contenteditable', 'true').focus();
            $(listId).addClass('editable');
        });
    }

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
    
