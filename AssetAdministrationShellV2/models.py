from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AssetAdministrationShell(db.Model):
    __tablename__ = 'aas'

    id = db.Column(db.Integer, primary_key=True)
    global_asset_id = db.Column(db.String, nullable=False)
    asset_kind = db.Column(db.String, default="NotApplicable")
    model_type = db.Column(db.String, default="AssetAdministrationShell")
    category = db.Column(db.String, nullable=True)
    description = db.Column(db.JSON, nullable=True)
    display_name = db.Column(db.JSON, nullable=True)
    embedded_data_specifications = db.Column(db.JSON, nullable=True)
    extensions = db.Column(db.JSON, nullable=True)
    id_short = db.Column(db.String, nullable=True)
    derived_from = db.Column(db.JSON, nullable=True)

    submodels = db.relationship("Submodel", back_populates="aas", cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "global_asset_id": self.global_asset_id,
            "asset_kind": self.asset_kind,
            "model_type": self.model_type,
            "category": self.category,
            "description": self.description,
            "display_name": self.display_name,
            "embedded_data_specifications": self.embedded_data_specifications,
            "extensions": self.extensions,
            "id_short": self.id_short,
            "derived_from": self.derived_from,
            "submodels": [submodel.to_dict() for submodel in self.submodels]
        }

class Submodel(db.Model):
    __tablename__ = 'submodels'

    id = db.Column(db.Integer, primary_key=True)
    aas_id = db.Column(db.Integer, db.ForeignKey('aas.id'))
    type = db.Column(db.String, default="ModelReference")
    keys = db.Column(db.JSON, nullable=False)
    name = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)

    aas = db.relationship("AssetAdministrationShell", back_populates="submodels")
    properties = db.relationship("Property", back_populates="submodel", cascade="all, delete-orphan")
    components = db.relationship("Component", back_populates="submodel", cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "aas_id": self.aas_id,
            "type": self.type,
            "keys": self.keys,
            "name": self.name,
            "description": self.description,
            "properties": [property.to_dict() for property in self.properties],
            "components": [component.to_dict() for component in self.components]
        }

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    submodel_id = db.Column(db.Integer, db.ForeignKey('submodels.id'))
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

    submodel = db.relationship("Submodel", back_populates="properties")
    def to_dict(self):
        return {
            "id": self.id,
            "submodel_id": self.submodel_id,
            "key": self.key,
            "value": self.value
        }

class Component(db.Model):
    __tablename__ = 'components'

    id = db.Column(db.Integer, primary_key=True)
    submodel_id = db.Column(db.Integer, db.ForeignKey('submodels.id'))
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    material = db.Column(db.String, nullable=True)
    description = db.Column(db.JSON, nullable=True)
    specifications = db.Column(db.JSON, nullable=True)  
    operating_conditions = db.Column(db.JSON, nullable=True)
    usage_patterns = db.Column(db.JSON, nullable=True)
    failure_modes = db.Column(db.JSON, nullable=True)
    detection_methods = db.Column(db.JSON, nullable=True)
    mitigation_measures = db.Column(db.JSON, nullable=True)
    dependencies = db.Column(db.JSON, nullable=True)
    interactions = db.Column(db.JSON, nullable=True)
    hazard_analysis = db.Column(db.JSON, nullable=True) 

    submodel = db.relationship("Submodel", back_populates="components")
    
    def to_dict(self):
        return {
            "id": self.id,
            "submodel_id": self.submodel_id,
            "name": self.name,
            "type": self.type,
            "material": self.material,
            "description": self.description,
            "specifications": self.specifications,
            "operating_conditions": self.operating_conditions,
            "usage_patterns": self.usage_patterns,
            "failure_modes": self.failure_modes,
            "detection_methods": self.detection_methods,
            "mitigation_measures": self.mitigation_measures,
            "dependencies": self.dependencies,
            "interactions": self.interactions
        }

