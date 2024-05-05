$(document).ready(function() {
    const components = ['Gearbox', 'Gear', 'Shaft', 'Bearing', 'Motor', 'Pump', 'Valve', 'Compressor', 'Fan', 'Blower', 'Heat Exchanger', 'Cooling Tower', 'Condenser', 'Evaporator', 'Boiler', 'Turbine', 'Generator', 'Transformer', 'Switchgear', 'Circuit Breaker', 'Relay', 'Fuse', 'Battery', 'Inverter', 'Converter', 'Rectifier', 'Capacitor', 'Resistor', 'Inductor', 'Diode'];
    const componentSelect = $('#component-select');

    componentSelect.empty().append('<option value="">Select Component...</option>');
    components.forEach(component => {
        componentSelect.append(`<option value="${component}">${component}</option>`);
    });

    function loadDropdown(url, postData, dropdownSelector) {
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(postData),
            success: function(response) {
                updateDropdown(dropdownSelector, response[Object.keys(response)[0]]);
            },
            error: function(xhr) {
                alert(`Error fetching data: ${xhr.responseText}`);
            }
        });
    }

    function updateDropdown(selector, items) {
        const select = $(selector);
        select.empty().append('<option value="">Select...</option>');
        items.forEach(item => {
            select.append(`<option value="${item}">${item}</option>`);
        });
    }

    $('#component-select').on('change', function() {
        const selectedComponent = $(this).val();
        $('#component-text').val(selectedComponent);  // Update text input
        if (selectedComponent) {
            loadDropdown('/get_failure_modes', {device: selectedComponent}, '#failure-mode-select');
            // loadDropdown('/get_causes', {failure_mode: selectedComponent}, '#cause-select');
            // loadDropdown('/get_effects', {cause: selectedComponent}, '#effect-select');
            // loadDropdown('/get_actions', {effect: selectedComponent}, '#action-select');
        }
    });

    $('#failure-mode-select').on('change', function() {
        const selectedFailureMode = $(this).val();
        $('#failure-mode-text').val(selectedFailureMode);  // Update text input
        if (selectedFailureMode) {
            loadDropdown('/get_causes', {failure_mode: selectedFailureMode}, '#cause-select');
        }
    });

    $('#cause-select').on('change', function() {
        const selectedCause = $(this).val();
        $('#cause-text').val(selectedCause);  // Update text input
        if (selectedCause) {
            loadDropdown('/get_effects', {cause: selectedCause}, '#effect-select');
        }
    });

    $('#effect-select').on('change', function() {
        const selectedEffect = $(this).val();
        $('#effect-text').val(selectedEffect);  // Update text input
        if (selectedEffect) {
            loadDropdown('/get_actions', {effect: selectedEffect}, '#action-select');
        }
    });
});
