from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms import AssetAdministrationShellForm, SubmodelForm, PropertyForm, ComponentForm, get_aas_choices, get_submodel_choices
from models import db, AssetAdministrationShell, Submodel, Property, Component
import json
from flask import jsonify
from agents import BrainstormingAgent, CompletingAgent
from flask_migrate import Migrate
from routes import main_bp
from flask_cors import CORS

import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Register the main blueprint for API routes
app.register_blueprint(main_bp, url_prefix='/api')



@app.route('/')
def index():
    asset_administration_shells = AssetAdministrationShell.query.all()
    submodels = Submodel.query.all()
    properties = Property.query.all()
    components = Component.query.all()
    
    # Debugging output
    print("AAS:", asset_administration_shells)
    print("Submodels:", submodels)
    print("Properties:", properties)
    print("Components:", components)
    
    return render_template('index.html', 
                           asset_administration_shells=asset_administration_shells, 
                           submodels=submodels, 
                           properties=properties, 
                           components=components)

def parse_json_field(field_data):
    import json
    try:
        return json.loads(field_data) if field_data else None
    except json.JSONDecodeError:
        return None

@app.route('/add_aas', methods=['GET', 'POST'])
def add_aas():
    form = AssetAdministrationShellForm()
    if form.validate_on_submit():
        aas = AssetAdministrationShell(
            global_asset_id=form.global_asset_id.data,
            asset_kind=form.asset_kind.data,
            model_type=form.model_type.data,
            category=form.category.data,
            description=parse_json_field(form.description.data),
            display_name=parse_json_field(form.display_name.data),
            embedded_data_specifications=parse_json_field(form.embedded_data_specifications.data),
            extensions=parse_json_field(form.extensions.data),
            id_short=form.id_short.data,
            derived_from=parse_json_field(form.derived_from.data)
        )
        db.session.add(aas)
        db.session.commit()
        flash('AssetAdministrationShell added successfully!')
        return redirect(url_for('index'))
    return render_template('add_aas.html', form=form)

@app.route('/add_submodel', methods=['GET', 'POST'])
def add_submodel():
    form = SubmodelForm()
    form.aas_id.choices = get_aas_choices()
    if form.validate_on_submit():
        submodel = Submodel(
            aas_id=form.aas_id.data,
            type=form.type.data,
            keys=form.keys.data,
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(submodel)
        db.session.commit()
        flash('Submodel added successfully!')
        return redirect(url_for('index'))
    return render_template('add_submodel.html', form=form)

@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    form = PropertyForm()
    form.submodel_id.choices = get_submodel_choices()
    if form.validate_on_submit():
        property = Property(
            submodel_id=form.submodel_id.data,
            key=form.key.data,
            value=form.value.data
        )
        db.session.add(property)
        db.session.commit()
        flash('Property added successfully!')
        return redirect(url_for('index'))
    return render_template('add_property.html', form=form)

@app.route('/add_component', methods=['GET', 'POST'])
def add_component():
    form = ComponentForm()
    form.submodel_id.choices = get_submodel_choices()
    if form.validate_on_submit():
        component = Component(
            submodel_id=form.submodel_id.data,
            name=form.name.data,
            type=form.type.data,
            material=form.material.data,
            description=form.description.data,
            specifications=form.specifications.data,
            usage_patterns=form.usage_patterns.data,
            failure_modes=form.failure_modes.data,
            detection_methods=form.detection_methods.data,
            mitigation_measures=form.mitigation_measures.data,
            dependencies=form.dependencies.data,
            interactions=form.interactions.data
        )
        db.session.add(component)
        db.session.commit()
        flash('Component added successfully!')
        return redirect(url_for('index'))
    return render_template('add_component.html', form=form)

@app.route('/risk_management_process')

def risk_management_process():
    return render_template("risk_management.html")

@app.route('/autocomplete')
def autocomplete():
    return render_template("AutoComplete.html")



@app.route('/export_json')
def export_json():
    data = {
        "aas": [aas.to_dict() for aas in AssetAdministrationShell.query.all()],
        "submodels": [submodel.to_dict() for submodel in Submodel.query.all()],
        "properties": [property.to_dict() for property in Property.query.all()],
        "components": [component.to_dict() for component in Component.query.all()],
    }
    return json.dumps(data, indent=4)

@app.route('/import_json', methods=['POST'])
def import_json():
    import json
    from flask import request, redirect, url_for

    file = request.files['file']
    if not file:
        flash('No file provided!')
        return redirect(url_for('index'))

    data = json.load(file)

    def get_or_create(model, defaults=None, **kwargs):
        instance = db.session.get(model, kwargs.get('id'))
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items())
            params.update(defaults or {})
            instance = model(**params)
            db.session.add(instance)
            db.session.commit()
            return instance, True

    # Clear existing data
    AssetAdministrationShell.query.delete()
    Submodel.query.delete()
    Property.query.delete()
    Component.query.delete()

    for aas_data in data.get('aas', []):
        defaults = {k: v for k, v in aas_data.items() if k != 'id'}
        get_or_create(AssetAdministrationShell, id=aas_data['id'], defaults=defaults)

    for submodel_data in data.get('submodels', []):
        defaults = {k: v for k, v in submodel_data.items() if k != 'id'}
        aas = db.session.get(AssetAdministrationShell, submodel_data['aas_id'])
        if aas:
            defaults['aas_id'] = aas.id
            get_or_create(Submodel, id=submodel_data['id'], defaults=defaults)

    for property_data in data.get('properties', []):
        defaults = {k: v for k, v in property_data.items() if k != 'id'}
        submodel = db.session.get(Submodel, property_data['submodel_id'])
        if submodel:
            defaults['submodel_id'] = submodel.id
            get_or_create(Property, id=property_data['id'], defaults=defaults)

    for component_data in data.get('components', []):
        defaults = {k: v for k, v in component_data.items() if k != 'id'}
        submodel = db.session.get(Submodel, component_data['submodel_id'])
        if submodel:
            defaults['submodel_id'] = submodel.id
            get_or_create(Component, id=component_data['id'], defaults=defaults)

    db.session.commit()
    flash('Data imported successfully!')
    return redirect(url_for('index'))

    db.session.commit()
    flash('Data imported successfully!')
    return redirect(url_for('index'))



@app.route('/generate_diagram_data')
def generate_diagram_data():
    data = {
        "aas": AssetAdministrationShell.query.all(),
        "submodels": Submodel.query.all(),
        "properties": Property.query.all(),
        "components": Component.query.all(),
    }
    diagram = "graph TD\n"
    
    for aas in data['aas']:
        display_name = aas.display_name['en'] if aas.display_name else f"AAS {aas.id}"
        display_name = display_name.replace('[', '(').replace(']', ')').replace('\n', ' ')
        diagram += f"AAS{aas.id}[{display_name}]\n"
        for submodel in aas.submodels:
            submodel_name = submodel.name.replace('[', '(').replace(']', ')').replace('\n', ' ')
            diagram += f"AAS{aas.id} --> Submodel{submodel.id}[{submodel_name}]\n"
            for prop in submodel.properties:
                prop_key = prop.key.replace('[', '(').replace(']', ')').replace('\n', ' ')
                prop_value = prop.value.replace('[', '(').replace(']', ')').replace('\n', ' ')
                diagram += f"Submodel{submodel.id} --> Property{prop.id}[{prop_key}: {prop_value}]\n"
            for component in submodel.components:
                component_name = component.name.replace('[', '(').replace(']', ')').replace('\n', ' ')
                diagram += f"Submodel{submodel.id} --> Component{component.id}[{component_name}]\n"
                if component.description:
                    component_desc = component.description.get('en', '').replace('[', '(').replace(']', ')').replace('\n', ' ')
                    diagram += f"Component{component.id} --> Description{component.id}[Description: {component_desc}]\n"
                if component.specifications:
                    component_specs = json.dumps(component.specifications).replace('[', '(').replace(']', ')').replace('\n', ' ')
                    diagram += f"Component{component.id} --> Specifications{component.id}[Specifications: {component_specs}]\n"

    return diagram


# Assuming these functions are defined in the same file or imported correctly
def get_all_asset_administration_shells():
    return [aas.to_dict() for aas in AssetAdministrationShell.query.all()]

def get_all_submodels():
    return [submodel.to_dict() for submodel in Submodel.query.all()]

def get_all_properties():
    return [property.to_dict() for property in Property.query.all()]

def get_all_components():
    return [component.to_dict() for component in Component.query.all()]

@app.route('/diagram')
def diagram():
    asset_administration_shells = get_all_asset_administration_shells()
    submodels = get_all_submodels()
    properties = get_all_properties()
    components = get_all_components()

    # Print data for debugging
    # print("Asset Administration Shells:", asset_administration_shells)
    # print("Submodels:", submodels)
    # print("Properties:", properties)
    # print("Components:", components)

    return render_template('diagram.html', 
                           asset_administration_shells=asset_administration_shells, 
                           submodels=submodels, 
                           properties=properties, 
                           components=components)




@app.route('/api/delete_aas/<int:id>', methods=['DELETE'])
def api_delete_aas(id):
    aas = AssetAdministrationShell.query.get_or_404(id)
    db.session.delete(aas)
    db.session.commit()
    return jsonify({'message': 'AssetAdministrationShell deleted successfully!'})

@app.route('/api/delete_submodel/<int:id>', methods=['DELETE'])
def api_delete_submodel(id):
    submodel = Submodel.query.get_or_404(id)
    db.session.delete(submodel)
    db.session.commit()
    return jsonify({'message': 'Submodel deleted successfully!'})

@app.route('/api/delete_property/<int:id>', methods=['DELETE'])
def api_delete_property(id):
    property = Property.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()
    return jsonify({'message': 'Property deleted successfully!'})

@app.route('/api/delete_component/<int:id>', methods=['DELETE'])
def api_delete_component(id):
    component = Component.query.get_or_404(id)
    db.session.delete(component)
    db.session.commit()
    return jsonify({'message': 'Component deleted successfully!'})

@app.route('/edit_aas/<int:id>', methods=['GET', 'POST'])
def edit_aas(id):
    aas = AssetAdministrationShell.query.get_or_404(id)
    form = AssetAdministrationShellForm(obj=aas)
    if form.validate_on_submit():
        form.populate_obj(aas)
        db.session.commit()
        flash('AssetAdministrationShell updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit_aas.html', form=form)

@app.route('/edit_submodel/<int:id>', methods=['GET', 'POST'])
def edit_submodel(id):
    submodel = Submodel.query.get_or_404(id)
    form = SubmodelForm(obj=submodel)
    form.aas_id.choices = get_aas_choices()
    if form.validate_on_submit():
        form.populate_obj(submodel)
        db.session.commit()
        flash('Submodel updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit_submodel.html', form=form)

@app.route('/edit_property/<int:id>', methods=['GET', 'POST'])
def edit_property(id):
    property = Property.query.get_or_404(id)
    form = PropertyForm(obj=property)
    form.submodel_id.choices = get_submodel_choices()
    if form.validate_on_submit():
        form.populate_obj(property)
        db.session.commit()
        flash('Property updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit_property.html', form=form)

@app.route('/edit_component/<int:id>', methods=['GET', 'POST'])
def edit_component(id):
    component = Component.query.get_or_404(id)
    form = ComponentForm(obj=component)
    form.submodel_id.choices = get_submodel_choices()
    if form.validate_on_submit():
        form.populate_obj(component)
        db.session.commit()
        flash('Component updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit_component.html', form=form)

@app.route('/api/device', methods=['POST'])
def generate_suggestions():
    data = request.get_json()
    description = data.get('description', '').strip()
    # print( "wsfhsfhb",description)
    if description:
        agent = CompletingAgent()
        result = agent.generate_outputass(description)
        print(result)  # Ensure this prints correctly formatted JSON
        if result:
            try:
                # Ensure result is properly formatted JSON
                result_json = json.dumps(result)
                return result_json, 200, {'Content-Type': 'application/json'}
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                return jsonify({"error": "Failed to generate suggestions"}), 500
        else:
            return jsonify({"error": "Failed to generate suggestions"}), 500

    return jsonify({"error": "Description not provided"}), 400
@app.route('/api/generate_hazard', methods=['POST'])
def generate_hazard():
    try:
        data = request.get_json()
        component_id = data.get('component_id')
        
        # Find the component and its parent structures
        component = Component.query.get_or_404(component_id)
        submodel = Submodel.query.get_or_404(component.submodel_id)
        aas = AssetAdministrationShell.query.get_or_404(submodel.aas_id)

        # Gather data
        hazard_data = {
            "component": {
                "id": component.id,
                "name": component.name,
                "type": component.type,
                "material": component.material,
                "description": component.description,
                "specifications": component.specifications,
                "operating_conditions": component.operating_conditions,
                "usage_patterns": component.usage_patterns,
                "failure_modes": component.failure_modes,
                "detection_methods": component.detection_methods,
                "mitigation_measures": component.mitigation_measures,
                "dependencies": component.dependencies,
                "interactions": component.interactions
            },
            "submodel": {
                "id": submodel.id,
                "name": submodel.name,
                "type": submodel.type,
                "keys": submodel.keys,
                "description": submodel.description
            },
            "aas": {
                "id": aas.id,
                "global_asset_id": aas.global_asset_id,
                "asset_kind": aas.asset_kind,
                "model_type": aas.model_type,
                "category": aas.category,
                "description": aas.description,
                "display_name": aas.display_name,
                "embedded_data_specifications": aas.embedded_data_specifications,
                "extensions": aas.extensions,
                "id_short": aas.id_short,
                "derived_from": aas.derived_from
            }
        }

        if hazard_data:
            agent = CompletingAgent()
            hazard_data_string = json.dumps(hazard_data, indent=4)
            print("Hazard Data String:", hazard_data_string)
            result = agent.generate_output(hazard_data_string)
            print("Agent Result:", result)
            
            if result:
                try:
                    # Log the type of result to understand its format
                    print(f"Result type: {type(result)}")
                    
                    # Assuming result is a plain text string that needs to be wrapped in a JSON structure
                    if isinstance(result, str):
                        hazards = [{"title": "Generated Hazard", "description": result}]
                    else:
                        hazards = result.get('hazards', [])

                    # Update the component's hazard_analysis
                    if not component.hazard_analysis:
                        component.hazard_analysis = []
                    
                    component.hazard_analysis.extend(hazards)
                    db.session.commit()

                    print(f"Updated Hazard Analysis: {component.hazard_analysis}")  # Debug statement

                    return jsonify({"hazards": hazards}), 200
                except Exception as e:
                    print(f"Error processing result: {e}")
                    return jsonify({"error": "Failed to process the result"}), 500
            else:
                print("Agent returned no result")
                return jsonify({"error": "Failed to generate suggestions"}), 500

        print("Hazard data not provided")
        return jsonify({"error": "Description not provided"}), 400

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An internal error occurred: {e}"}), 500





@app.route('/api/save_best_hazard', methods=['POST'])
def save_best_hazard():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        print(f"Received data: {data}")  # Debug statement

        # Extract the necessary fields from the data
        component_id = data.get('component_id')
        best_response_index = int(data.get('best_response_index'))
        best_response = data.get('best_response')
        print(f"Component ID: {component_id}, Best Response Index: {best_response_index}, Best Response: {best_response}")  # Debug statement

        # Retrieve the component and its related entities
        component = Component.query.get_or_404(component_id)
        submodel = Submodel.query.get_or_404(component.submodel_id)
        aas = AssetAdministrationShell.query.get_or_404(submodel.aas_id)
        properties = Property.query.filter_by(submodel_id=submodel.id).all()

        print(f"Component found: {component}")  # Debug statement

        # Ensure hazard_analysis is a list
        if not component.hazard_analysis:
            component.hazard_analysis = []

        # Extend the list if the index is beyond the current length
        while len(component.hazard_analysis) <= best_response_index:
            component.hazard_analysis.append(None)

        # Update the best hazard response at the specified index
        component.hazard_analysis[best_response_index] = best_response

        # Construct the file path for saving the hazard analysis
        hazard_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Hazard analysis')
        
        # Ensure the directory exists
        if not os.path.exists(hazard_dir):
            os.makedirs(hazard_dir)

        # Define the file path
        file_path = os.path.join(hazard_dir, f"hazard_analysis_{component.name}.txt")

        # Append the best hazard analysis response to the file
        with open(file_path, 'a') as file:
            # Write the Asset Administration Shell details
            file.write(f"Asset Administration Shell Name: {aas.global_asset_id}\n")
            
            # Write the Submodel details
            file.write(f"Submodel Name: {submodel.name}\n")
            
            # Write all properties associated with the submodel
            for property in properties:
                file.write(f"Property Key: {property.key}, Property Value: {property.value}\n")
            
            # Write the Component details
            file.write(f"Component Name: {component.name}\n")

            # Write the Hazard Analysis details
            file.write(f"Hazard Response:\n{json.dumps(best_response, indent=2)}\n\n")

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Best hazard analysis response saved successfully."}), 200

    except Exception as e:
        # Print the error message for debugging
        print(f"An error occurred: {e}")  # Debug statement
        return jsonify({"error": f"An internal error occurred: {e}"}), 500



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
