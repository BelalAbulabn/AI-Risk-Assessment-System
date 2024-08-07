from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import json
from models import AssetAdministrationShell, Submodel
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def get_aas_choices():
    return [(aas.id, aas.global_asset_id) for aas in AssetAdministrationShell.query.all()]

def get_submodel_choices():
    return [(submodel.id, submodel.name) for submodel in Submodel.query.all()]
class AssetAdministrationShellForm(FlaskForm):
    global_asset_id = StringField('Global Asset ID', validators=[DataRequired()])
    asset_kind = StringField('Asset Kind')
    model_type = StringField('Model Type')
    category = StringField('Category')
    description = TextAreaField('Description')
    display_name = TextAreaField('Display Name')
    embedded_data_specifications = TextAreaField('Embedded Data Specifications')
    extensions = TextAreaField('Extensions')
    id_short = StringField('ID Short')
    derived_from = TextAreaField('Derived From')
    submit = SubmitField('Add AAS')

class SubmodelForm(FlaskForm):
    aas_id = StringField('AAS ID', validators=[DataRequired()])
    type = StringField('Type')
    keys = TextAreaField('Keys', validators=[DataRequired()])
    name = StringField('Name')
    description = TextAreaField('Description')
    submit = SubmitField('Add Submodel')

class PropertyForm(FlaskForm):
    submodel_id = StringField('Submodel ID', validators=[DataRequired()])
    key = StringField('Key', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Add Property')

class ComponentForm(FlaskForm):
    submodel_id = StringField('Submodel ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    type = StringField('Type')
    material = StringField('Material')
    description = TextAreaField('Description')
    specifications = TextAreaField('Specifications')

    # New fields for risk analysis
    operating_conditions = TextAreaField('Operating Conditions')
    usage_patterns = TextAreaField('Usage Patterns')
    failure_modes = TextAreaField('Failure Modes')
    detection_methods = TextAreaField('Detection Methods')
    mitigation_measures = TextAreaField('Mitigation Measures')
    dependencies = TextAreaField('Dependencies')
    interactions = TextAreaField('Interactions')

    submit = SubmitField('Add Component')
