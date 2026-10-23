import os
# from llm import gpt_model_call
import json
# from openai import OpenAI
import openai

# class BrainstormingAgent:
#     def __init__(self):
#         self.prompt_template = """You are assisting a risk analysis engineer in performing iso standerd. Here is the FMEA table data:
# {{fmea_table}}

# Now, you should focus on the {{dic_key_value}} in row {{selected_row}}. 
# Please brainstorm and provide 3 similar items for "{{dic}}", addressing different possible aspects, and generate a concise reason and a concise comment for each one.

# You should provide the output in JSON format using the following template:
# Output template:
# {"output":[{"reason": "a_different_aspect", "content": "a_similar_but_different_content", "comment": "a_concise_explanation"},
# {"reason": "a_different_aspect", "content": "a_similar_but_different_content", "comment": "a_concise_explanation"},
# {"reason": "a_different_aspect", "content": "a_similar_but_different_content", "comment": "a_concise_explanation"}]}

# You should now complete the output with the template:
# Output: """

#     def generate_output(self, fmea_table, dic_key_value, selected_row, dic, model='gpt-3.5'): # alternative model: 'gpt-3.5/4'
#         self.prompt_filled = self.prompt_template.replace("{{fmea_table}}", fmea_table)
#         self.prompt_filled = self.prompt_filled.replace("{{dic_key_value}}", dic_key_value)
#         self.prompt_filled = self.prompt_filled.replace("{{selected_row}}", selected_row)
#         self.prompt_filled = self.prompt_filled.replace("{{dic}}", dic)
#         openai.api_key=os.getenv("OPENAI_API_KEY")
#         print(openai.api_key)
#         print("***********************")
#         # print(input_text)
#         print("***********************")
#         print("LLM agent working")
#         print("***********************")
#         try:
#             text_output = gpt_model_call(self.prompt_filled, model=model)
#             print(text_output)
#         except Exception as e:
#             print(f"Error: {e}")

#             return None

#         try:
#             # Parse the text output into a JSON object
#             result_json = json.loads(text_output)
#             print(result_json)
#         except json.JSONDecodeError as json_err:
#             print(f"JSON Decode Error: {json_err}")
#             return None

#         # Write the JSON data to a file
#         with open('generation_agent.json', 'w') as file:
#             json.dump(result_json, file, indent=4)
#         print("Result:\n")
#         print(text_output)
#         return result_json

# # Todo: new agent
# class CompletingAgent:
#     def __init__(self):
#         self.prompt_template = """You are assisting a risk analysis engineer in performing FMEA analysis. Here is the FMEA table data:
# {{fmea_table}}

# Now, you should focus on the {{dic_key_value}} in row {{selected_row}}. 
# Please brainstorm and provide 3 alternative items for "{{dic}}", addressing different possible aspects, and generate a concise reason and a concise comment for each one.

# You should provide the output in JSON format using the following template:
# Output template:
# {"output":[{"reason": "a_different_aspect", "content": "a_similar_but_different_content", "comment": "a_concise_explanation"},
# {"reason": "a_different_aspect", "content": "a_similar_but_different_content", "comment": "a_concise_explanation"},
# {"reason": "a_different_aspect", "content": "a_similar_but_different_content", "comment": "a_concise_explanation"}]}

# You should now complete the output with the template:
# Output: """

#     def generate_output(self, fmea_table, dic_key_value, selected_row, dic, model='gpt-3.5'):
#         self.prompt_filled = self.prompt_template.replace("{{fmea_table}}", fmea_table)
#         self.prompt_filled = self.prompt_filled.replace("{{dic_key_value}}", dic_key_value)
#         self.prompt_filled = self.prompt_filled.replace("{{selected_row}}", selected_row)
#         self.prompt_filled = self.prompt_filled.replace("{{dic}}", dic)
#         openai.api_key=os.getenv("OPENAI_API_KEY")
#         print(openai.api_key)
#         # print(input_text)
#         print("***********************")
#         print("LLM agent working")
#         print("***********************")
#         try:
#             text_output = gpt_model_call(self.prompt_filled, model=model)
#             print(text_output)
#         except Exception as e:
#             print(f"Error: {e}")

#             return None

#         try:
#             # Parse the text output into a JSON object
#             result_json = json.loads(text_output)
#             print(result_json)
#         except json.JSONDecodeError as json_err:
#             print(f"JSON Decode Error: {json_err}")
#             return None

#         # Write the JSON data to a file
#         with open('generation_agent.json', 'w') as file:
#             json.dump(result_json, file, indent=4)
#         print("Result:\n")
#         print(text_output)
#         return result_json
    
# class BrainstormingAgent:
#     def __init__(self):
#         self.prompt_template = """You are assisting a risk analysis engineer. Here are some details about the system or scenario:
# {{system_details}}

# Based on the above information, please provide a detailed risk analysis. Identify potential risks and suggest preliminary mitigation strategies. Format your response with each risk and strategy clearly numbered."""

#     def generate_output(self, system_details, model='gpt-3.5-turbo'):
#         prompt = self.prompt_template.replace("{{system_details}}", system_details)
#         openai.api_key = "your-openai-api-key"  # Replace with the actual API key and manage securely

#         try:
#             response = openai.ChatCompletion.create(
#                 model=model,
#                 messages=[{"role": "system", "content": "Start a new conversation."},
#                           {"role": "user", "content": prompt}]
#             )
#             text_output = response.choices[0].message['content'].strip()
#             return text_output
#         except Exception as e:
#             print(f"Error: {e}")
#             return None

# class CompletingAgent:
#     def __init__(self):
#         self.prompt_template = """You are assisting in the development of a comprehensive risk management plan. Based on the following system characteristics:
# {{system_characteristics}}

# Please generate a structured risk evaluation that identifies key risk points and evaluates their impact and likelihood. Provide recommendations for risk control measures."""

#     def generate_output(self, system_characteristics, model='gpt-3.5-turbo'):
#         prompt = self.prompt_template.replace("{{system_characteristics}}", system_characteristics)
#         openai.api_key = "your-openai-api-key"  # Securely managed

#         try:
#             response = openai.ChatCompletion.create(
#                 model=model,
#                 messages=[{"role": "system", "content": "Start a new conversation."},
#                           {"role": "user", "content": prompt}]
#             )
#             text_output = response.choices[0].message['content'].strip()
#             return text_output
#         except Exception as e:
#             print(f"Error: {e}")
#             return None


import openai


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

