# from llm import gpt_model_call
import json
# from openai import OpenAI
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

class BrainstormingAgent:
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.prompt_template_Risk_Analysis = """You are assisting a risk analysis engineer. Based on the provided data: {{data_details}}, please generate a Risk Analysis addressing the key points and answering the question: "What could be the risks involved based on ISO standards when developing it in a car?" The report should include:

1. Establish intended use and reasonably foreseeable misuse.
2. Identify characteristics related to safety.
3. Identify hazards and hazardous situations.
4. Estimate the risk(s) for each hazardous situation.

Please ensure to address the most important four points in the analysis.
"""
        self.prompt_template_Risk_Evaluation = """You are assisting a risk analysis engineer. Based on the Risk_Analysis: {{data_details}}, please generate a Risk Evaluation addressing the key points:

1. Comparing the risks with the risk acceptability criteria to determine if risk control measures are needed.
2. Evaluating if the identified risk control measures are practicable.
3. Implementing and verifying the identified risk control measures if practicable.
4. Assessing the residual risk to determine if it is acceptable.

Please ensure to address the most important four points in the evaluation.
"""
        self.prompt_template_Risk_Control = """You are assisting a risk analysis engineer. Based on the evaluation data: {{data_details}} please generate a report according to ISO risk analysis standards. The report should include:

1. Risk control option analysis
    - Is risk control required?
    - If yes, identify appropriate risk control measures.
    - If not, go to: "Are new hazards or hazardous situations introduced or existing risks affected?"
    - Is control practicable?
    - If yes, implement and verify the identified risk control measures.
    - If not, go to: "Are new hazards or hazardous situations introduced or existing risks affected?"

2. Implementation of risk control measures
    - Are the implemented measures effective?

3. Residual risk evaluation
    - Is the residual risk acceptable?
    - If yes, are new hazards or hazardous situations introduced or existing risks affected?
    - If no, have all identified hazardous situations been considered?

4. Re-risk analysis
    - Reevaluate risks considering implemented measures.

5. Benefits and risks of control measures
    - Discuss the advantages and potential drawbacks of the control measures.
 """        
        self.prompt_template_Evaluation_of_Overall_Residual_Risk = """You are assisting a risk analysis engineer. Based on the provided data: {{data_details}} Please generate an Evaluation of Overall Residual Risk report addressing the key points."""
        self.prompt_template_Risk_Management_Review = """You are assisting a risk analysis engineer. Based on the provided data: {{data_details}} Please generate a Risk Management Review report addressing the key points."""
        self.prompt_template_Production_and_Post_Production_Activities = """You are assisting a risk analysis engineer. Based on the provided data: {{data_details}} Please generate a Production and Post-Production Activities report addressing the key points."""

    def generate_report(self, prompt_template, data_details, temperature=0.7):
        prompt = prompt_template.replace("{{data_details}}", data_details)
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful assistant designed to assist with risk analysis."},
                          {"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def generate_risk_analysis_report(self, data_details, temperature=0.7):

        return self.generate_report(self.prompt_template_Risk_Analysis, data_details, temperature)

    def generate_risk_evaluation_report(self, data_details, temperature=0.7):
        print(data_details)
        return self.generate_report(self.prompt_template_Risk_Evaluation, data_details, temperature)

    def generate_risk_control_report(self, data_details, temperature=0.7):
        return self.generate_report(self.prompt_template_Risk_Control, data_details, temperature)

    def generate_evaluation_of_overall_residual_risk_report(self, data_details, temperature=0.7):
        return self.generate_report(self.prompt_template_Evaluation_of_Overall_Residual_Risk, data_details, temperature)

    def generate_risk_management_review_report(self, data_details, temperature=0.7):
        print("Generating Risk Management Review Report")
        return self.generate_report(self.prompt_template_Risk_Management_Review, data_details, temperature)

    def generate_production_and_post_production_activities_report(self, data_details, temperature=0.7):
        return self.generate_report(self.prompt_template_Production_and_Post_Production_Activities, data_details, temperature)

# Example usage
# agent = BrainstormingAgent()

# # Step-by-step generation of reports
# initial_data = "Initial data for risk analysis."
# risk_analysis_report = agent.generate_risk_analysis_report(initial_data)
# print("Risk Analysis Report:\n", risk_analysis_report)

# risk_evaluation_report = agent.generate_risk_evaluation_report(risk_analysis_report)
# print("Risk Evaluation Report:\n", risk_evaluation_report)

# risk_control_report = agent.generate_risk_control_report(risk_evaluation_report)
# print("Risk Control Report:\n", risk_control_report)

# evaluation_of_overall_residual_risk_report = agent.generate_evaluation_of_overall_residual_risk_report(risk_control_report)
# print("Evaluation of Overall Residual Risk Report:\n", evaluation_of_overall_residual_risk_report)

# risk_management_review_report = agent.generate_risk_management_review_report(evaluation_of_overall_residual_risk_report)
# print("Risk Management Review Report:\n", risk_management_review_report)

# production_and_post_production_activities_report = agent.generate_production_and_post_production_activities_report(risk_management_review_report)
# print("Production and Post-Production Activities Report:\n", production_and_post_production_activities_report)

# You can call each report generation method independently as needed.
import json
import openai


class CompletingAgent:
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.prompt_template = """
        You are assisting a risk analysis engineer in performing FMEA analysis. Here is the device description or device name:
        {{device_description}}

         brainstorm and provide all possible hazards based on the description provided.at lest 7 to 10 Diffrent  One hazard for ech compent  component can have more than one hazard, and different hazard types such as software, hardware, mechanical, or others.

        Format the output in JSON format as follows:
        [
            {
                "hazard": "Hazard name",
                "type": "Hazard type",
                "description": "Hazard description",
                "detection_method": "Detection method",
                "mitigation_measure": "Mitigation measure"

            },
            ...
        ]
"""


        self.hazard_prompt_template = """You are assisting a risk analysis engineer in performing FMEA analysis. Here is the device description and selected component:
Device Description: {{device_description}}
Component: {{component}}

Please brainstorm and provide a list of possible hazards associated with the selected component based on the description provided.

You should provide the output in JSON format using the following template:
Output template:
{
    "hazards": ["Hazard1", "Hazard2", "Hazard3"]
}

You should now complete the output with the template:
Output: """

        self.Ass_prompt_template = """
You are an engineer responsible for generating digital twins in the Asset Administration Shells format. Here is the device description or name:
Device Description, Name: {{device_description}}

Please brainstorm and provide the device with all its submodels and components in the following format:

You should provide the output in JSON format using the following template:
Output template:
{
    "aas": [
        {
            "id": 1,
            "global_asset_id": "GlobalAssetID_001",
            "asset_kind": "Instance",
            "model_type": "AssetAdministrationShell",
            "category": "CategoryA",
            "description": "This is a description of AAS.",
            "display_name": "AAS_001",
            "embedded_data_specifications": {"specKey": "specValue"},
            "extensions": {"extKey": "extValue"},
            "id_short": "AAS1",
            "derived_from": null
        }
    ],
    "submodels": [
        {
            "id": 1,
            "aas_id": 1,
            "type": "ModelReference",
            "keys": [{"key": "Key1", "type": "Global"}],
            "name": "Submodel_001",
            "description": "This is a description of the submodel."
        },
        {
            "id": 2,
            "aas_id": 1,
            "type": "ModelReference",
            "keys": [{"key": "Key2", "type": "Global"}],
            "name": "Submodel_002",
            "description": "This is another description of a submodel."
        }
    ],
    "properties": [
        {
            "id": 1,
            "submodel_id": 1,
            "key": "PropertyKey1",
            "value": "PropertyValue1"
        },
        {
            "id": 2,
            "submodel_id": 2,
            "key": "PropertyKey2",
            "value": "PropertyValue2"
        }
    ],
    "components": [
        {
            "id": 2,
            "submodel_id": 2,
            "name": "BatteryPack",
            "type": "Lithium-Ion",
            "material": "Lithium",
            "status": "Operational",
            "description": {
                "usage": "Main battery pack for the electric vehicle."
            },
            "specifications": {
                "voltage": "400V",
                "current": "150A",
                "capacity": "75 kWh",
                "energy_density": "250 Wh/kg",
                "charging_time": "1 hour (fast charging)",
                "discharge_rate": "2C"
            },
            "operating_conditions": {
                "temperature_range": "-20 to 60 C",
                "humidity": "0 to 95% RH"
            },
            "usage_patterns": {
                "daily_usage": "Average 100 miles",
                "charging_cycles": "1000 cycles"
            },
            "maintenance_history": {
                "last_maintenance_date": "2024-06-01",
                "notes": "No issues found."
            },
            "failure_modes": {
                "thermal_runaway": "Risk of overheating",
                "capacity_fade": "Reduction in capacity over time"
            },
            "failure_probabilities": {
                "thermal_runaway": 0.01,
                "capacity_fade": 0.1
            },
            "failure_severity": {
                "thermal_runaway": "high",
                "capacity_fade": "moderate"
            },
            "detection_methods": {
                "thermal_runaway": "Temperature sensors",
                "capacity_fade": "Battery management system monitoring"
            },
            "mitigation_measures": {
                "thermal_runaway": "Cooling system",
                "capacity_fade": "Regular monitoring and calibration"
            },
            "historical_performance_data": {
                "mean_time_between_failures": "5000 hours",
                "last_failure_date": "N/A"
            },
            "incident_reports": {
                "none": "No incidents reported."
            },
            "inspection_results": {
                "2024-06-01": "No issues found during last inspection"
            },
            "predictive_analytics_data": {
                "expected_lifetime": "8 years based on current usage patterns"
            },
            "compliance_standards": {
                "ISO9001": "Certified",
                "ISO14001": "Certified"
            },
            "safety_ratings": {
                "SIL": 2
            },
            "regulatory_requirements": {
                "EU_Machinery_Directive": "Compliant"
            },
            "certification_info": {
                "certification_number": "123456789",
                "certification_date": "2022-01-10"
            },
            "dependencies": {
                "power_supply": "Requires 480V 3-phase power",
                "cooling_system": "Requires external cooling system"
            },
            "interactions": {
                "connected_to": "Main vehicle power system",
                "controls": "Managed by vehicle's battery management system"
            }
        },
        {
            "id": 3,
            "submodel_id": 2,
            "name": "CoolingSystem",
            "type": "Coolant",
            "material": "Coolant Fluid",
            "status": "Operational",
            "description": "Cooling system for the battery pack.",
            "specifications": {
                "flow_rate": "10 L/min",
                "temperature_range": "-10 to 50 C",
                "coolant_type": "Ethylene glycol-based"
            },
            "operating_conditions": {
                "temperature_range": "-20 to 40 C",
                "humidity": "0 to 100% RH"
            },
            "usage_patterns": {
                "continuous_operation": "8 hours/day"
            },
            "maintenance_history": {
                "last_maintenance_date": "2024-05-01",
                "notes": "Coolant replaced."
            },
            "failure_modes": {
                "leakage": "Coolant leakage",
                "pump_failure": "Coolant pump failure"
            },
            "failure_probabilities": {
                "leakage": 0.05,
                "pump_failure": 0.02
            },
            "failure_severity": {
                "leakage": "moderate",
                "pump_failure": "high"
            },
            "detection_methods": {
                "leakage": "Visual inspection for leaks",
                "pump_failure": "Pressure sensor monitoring"
            },
            "mitigation_measures": {
                "leakage": "Regular inspections",
                "pump_failure": "Redundant pump system"
            },
            "historical_performance_data": {
                "mean_time_between_failures": "3000 hours",
                "last_failure_date": "2023-11-20"
            },
            "incident_reports": {
                "2023-11-20": "Coolant pump failure caused temporary overheating"
            },
            "inspection_results": {
                "2024-05-01": "Coolant levels normal"
            },
            "predictive_analytics_data": {
                "expected_lifetime": "5 years with regular maintenance"
            },
            "compliance_standards": {
                "ISO9001": "Certified"
            },
            "safety_ratings": {
                "SIL": 1
            },
            "regulatory_requirements": {
                "EPA": "Compliant"
            },
            "certification_info": {
                "certification_number": "987654321",
                "certification_date": "2021-06-15"
            },
            "dependencies": {
                "power_supply": "Requires connection to battery management system"
            },
            "interactions": {
                "connected_to": "Battery cooling loop",
                "controls": "Managed by battery management system"
            }
        }
    ]
}
"""


    def generate_output(self, device_description, temperature=0.7):
        prompt = self.prompt_template.replace("{{device_description}}", device_description)
        print("***********************")
        print("LLM agent working")
        print("***********************")
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to assist with risk analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            text_output = response.choices[0].message['content'].strip()
            print(text_output)
        except Exception as e:
            print(f"Error: {e}")
            return None
        
        return text_output
    
    def generate_outputass(self, device_description, temperature=0.7):
        prompt = self.Ass_prompt_template.replace("{{device_description}}", device_description)
        print("***********************")
        print("LLM agent working")
        print("***********************")
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to assist with risk analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            text_output = response.choices[0].message['content'].strip()
            print(text_output)
        except Exception as e:
            print(f"Error: {e}")
            return None
        
        return text_output




    def generate_hazards(self, device_description, component, temperature=0.7):
        prompt = self.hazard_prompt_template.replace("{{device_description}}", device_description)
        prompt = prompt.replace("{{component}}", component)
        print("***********************")
        print("LLM agent working")
        print("***********************")
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to assist with risk analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            text_output = response.choices[0].message['content'].strip()
            print(text_output)
        except Exception as e:
            print(f"Error: {e}")
            return None

        # Extract the JSON content from the text_output
        try:
            # Find the start of the JSON content
            start_index = text_output.find('{')
            if start_index != -1:
                json_content = text_output[start_index:]
                result_json = json.loads(json_content)
                print(result_json)
            else:
                print("No JSON content found in the response.")
                return None
        except json.JSONDecodeError as json_err:
            print(f"JSON Decode Error: {json_err}")
            return None

        with open('hazard_generation.json', 'w') as file:
            json.dump(result_json, file, indent=4)
        print("Result:\n")
        print(result_json)
        return result_json

