# from llm import gpt_model_call
import json
# from openai import OpenAI
import openai

import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

class BrainstormingAgent:
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.prompt_template_Risk_Analysis = """You are assisting a risk analysis engineer. Based on the provided hazard analysis {{data_details}}, please generate a Risk Analysis report in JSON format that addresses the following key points:

1. Establish intended use and reasonably foreseeable misuse.
2. Identify characteristics related to safety.
3. Identify hazards and hazardous situations.
4. Estimate the risk(s) for each hazardous situation.

The JSON response should have the following structure:

{
    "intended_use": "Description of intended use",
    "foreseeable_misuse": "Description of foreseeable misuse",
    "safety_characteristics": "List of characteristics related to safety",
    "hazards": [
        {
            "name": "Name of the hazard",
            "hazardous_situation": "Description of the hazardous situation",
            "risk_estimation": "Estimated risk level"
        }
    ]
}
"""
#add new prompt
#add new prompt
#get the data from the user
#generate the report
#return the report

        self.prompt_template_Risk_Evaluation = """
You are assisting a risk analysis engineer. Based on the Risk_Analysis: {{data_details}}, please generate a Risk Evaluation for echt hazard in JSON format addressing the key points:

{
  "risk_acceptability": "Determine if the identified risks meet the risk acceptability criteria.",
  "risk_control_measures": [
    {
      "measure": "Description of the risk control measure",
      "practicability": "Evaluation if the measure is practicable"
    }
  ],
  "residual_risk": "Assess the residual risk and determine if it is acceptable."
}

Ensure that you adhere to these criteria for the evaluation.
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
# New template for suggestion generation
        self.prompt_template_Suggestion = """You are an assistant designed to provide suggestions based on user input. Based on the input: "{{user_input}}", please generate a set of relevant suggestions that are clear and concise. Ensure the suggestions are practical and actionable."""
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




class CompletingAgent:
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.prompt_template = """You are assisting a risk analysis engineer in performing FMEA analysis. Here is the device description:
{{device_description}}

Please brainstorm and provide a list of components and hazards based on the description provided. 

You should provide the output in JSON format using the following template:
Output template:
{
    "components": ["Component1", "Component2", "Component3"],
    "hazards": ["Hazard1", "Hazard2", "Hazard3"]
}

You should now complete the output with the template:
Output: """

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

        with open('generation_agent.json', 'w') as file:
            json.dump(result_json, file, indent=4)
        print("Result:\n")
        print(result_json)
        return result_json

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

