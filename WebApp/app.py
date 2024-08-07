from flask import Flask, render_template, jsonify, request
import openai
from flask_caching import Cache
from flask_cors import CORS
from agents import BrainstormingAgent, CompletingAgent
import os
from dotenv import load_dotenv
print("API Key Set:", openai.api_key)  # This should print the key to confirm it's set
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
CORS(app)

# Correct way to load .env file with a specified path
# load_dotenv(r"C:\FMEA\AI-Risk-Assessment-System\WebApp\.env")
print("API Key Set:", openai.api_key)  # This should print the key to confirm it's set


# Retrieve API key from environment variables
# openai.api_key = os.getenv('OPENAI_API_KEY')
print("API Key Set:", openai.api_key)  # This should print the key to confirm it's set

agent = BrainstormingAgent()
# openai.api_key ="sk-proj-ETFsJX268RMex0DnMBXLT3BlbkFJte8z9HsVVPtrYCLYsxja"

print("API Key Set:", openai.api_key)  # This should print the key to confirm it's set
@cache.memoize(timeout=86400)
def get_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Start a new conversation."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content'].strip()
    except openai.APIError as e:
        app.logger.error(f"API error occurred: {e}")
        return f"API error occurred: {e}"
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"

@app.route('/')
def home():
    return render_template('Risk Management Process.html')

@app.route('/1')
def other_page():
    return render_template('index.html')

@app.route('/get_failure_modes', methods=['POST'])
def get_failure_modes():
    data = request.get_json()
    if data and 'device' in data:
        device = data['device']
        # prompt = f"List potential failure modes for a {device}. Each point should be clearly numbered:"
        response = agent.generate_risk_analysis_report(device)
        print(device)
        print(response)
        return jsonify({"failure_modes": response})
    return jsonify({"error": "Device not specified"}), 400


def prompt_settings(base_prompt, detail=""):
    # Adding specific instructions and context for the GPT-3 model.
    # The 'detail' parameter allows custom instructions per function call.
    instructions = f"\n\nPlease list detailed, clear, and concise information. {detail}"
    return f"{base_prompt}{instructions}"

@app.route('/analyze_failure_mode', methods=['POST'])
def analyze_failure_mode():
    data = request.get_json()
    if data.get('failure_mode'):
        prompt = f"Provide a list  of the failure mode '{data['failure_mode']}' including potential causes and impacts."
        analysis = get_gpt_response(prompt_settings(prompt, "Detail each point clearly."))
        return jsonify({"detailed_analysis": analysis.split('\n')})
    return jsonify({"error": "Failure mode not specified"}), 400


@app.route('/get_causes', methods=['POST'])
def get_causes_of_failure():
    data = request.get_json()
    if data.get('failure_mode'):
        prompt = f"list possible causes for the failure mode '{data['failure_mode']}'."
        causes = get_gpt_response(prompt_settings(prompt, "List possible causes:"))
        return jsonify({"causes": causes.split('\n')})
    return jsonify({"error": "Failure mode not specified"}), 400

@app.route('/get_effects', methods=['POST'])
def get_effects_of_failure():
    data = request.get_json()
    if data.get('cause'):
        prompt = f"What are the effects of the cause '{data['cause']}' on the system?"
        effects = get_gpt_response(prompt_settings(prompt, "Enumerate the effects:"))
        return jsonify({"effects": effects.split('\n')})
    return jsonify({"error": "Cause not specified"}), 400

    
@app.route('/get_actions', methods=['POST'])
def get_actions_to_mitigate():
    data = request.get_json()
    if not data or 'effect' not in data:
        app.logger.error("Effect not specified in the request")
        return jsonify({"error": "Effect not specified"}), 400

    effect = data['effect']
    if not effect:
        app.logger.error("Effect is empty")
        return jsonify({"error": "Effect is empty"}), 400

    prompt = f"What are the recommended actions to mitigate the effect: list {effect}?"
    try:
        response = get_gpt_response(prompt_settings(prompt))
        if response:
            actions = response.split('\n')
            return jsonify({"actions": actions})
        else:
            app.logger.error("No response from GPT model")
            return jsonify({"error": "No response received from GPT model"}), 500
    except Exception as e:
        app.logger.error(f"Failed to generate response due to: {str(e)}")
        return jsonify({"error": "Failed to generate actions", "message": str(e)}), 500
    

# app.route('/get_failure_modes', methods=['POST'])
# def get_failure_modes():
#     data = request.get_json()
#     if data and 'device' in data:
#         device = data['device']
#         response =agent.generate_risk_analysis_report(device)

#                 #  agent.generate_risk_analysis_report(data['initial_data'])

#         print(response)
#         return jsonify({"failure_modes": response.split('\n')})
#     return jsonify({"error": "Device not specified"}), 400
risk_evaluation_report=" "
risk_analysis_report = " "
device = " "
selected_component = None
selected_hazared = None
# Global variables to store reports
# Global variables to store reports
global_reports = {
    "risk_analysis_report": "",
    "risk_evaluation_report": "",
    "risk_control_report": "",
    "evaluation_of_overall_residual_risk_report": "",
    "risk_management_review_report": "",
    "production_and_post_production_activities_report": "",
    "corrected_text": ""
}
# @app.route('/generate_risk_analysis', methods=['POST'])
# def generate_risk_analysis():
#     data = request.get_json()
#     if data.get('initial_data'):
#         # risk_analysis_report = agent.generate_risk_analysis_report(device)
#         # print(device)

#         global_reports["risk_analysis_report"] = agent.generate_risk_analysis_report(device)
#         return jsonify({"Risk_Analysis_Report": global_reports["risk_analysis_report"]})
    
#         # risk_evaluation_report = agent.generate_risk_evaluation_report(risk_analysis_report)
#         return jsonify({"Risk_Analysis_Report": risk_analysis_report})
#     return jsonify({"error": "Initial data not specified"}), 400



@app.route('/generate_risk_analysis', methods=['POST'])
def generate_risk_analysis():
    if not selected_component:
        return jsonify({"error": "Please select a component"}), 400
    if not selected_hazared:
        return jsonify({"error": "Please select a hazared"}), 400
    if selected_component and selected_hazared:
        print(f'Component: {selected_component}, Hazared: {selected_hazared}')
        
        # Here you would generate the risk analysis report using the component and hazared
        risk_analysis_report = f"Risk analysis report for component: {selected_component}, hazared: {selected_hazared}"

        global_reports["risk_analysis_report"] = agent.generate_risk_analysis_report(selected_component+" "+selected_hazared)
        return jsonify({"Risk_Analysis_Report": global_reports["risk_analysis_report"]})
    
    return jsonify({"error": "Component or hazared not specified"}), 400

# @app.route('/generate_risk_evaluation', methods=['POST'])
# def generate_risk_evaluation():
#     global global_reports
#     if global_reports["risk_analysis_report"]:
#         global_reports["risk_evaluation_report"] = agent.generate_risk_evaluation_report(global_reports["risk_analysis_report"])
#         print(global_reports["risk_evaluation_report"])
#         return jsonify({"Risk_Evaluation_Report": global_reports["risk_evaluation_report"]})
#     return jsonify({"error": "Risk analysis report not specified"}), 400
@app.route('/text_correction', methods=['POST'])
def text_correction():
    data = request.json
    corrected_text = data['text'].strip()
    global_reports["corrected_text"] = corrected_text  # Store corrected text globally
    print(corrected_text)
    return jsonify({'corrected_text': corrected_text})

# @app.route('/generate_risk_evaluation', methods=['POST'])
# def generate_risk_evaluation():
#     data = request.get_json()
#     risk_analysis_report = data.get('risk_analysis_report', '')

#     if risk_analysis_report:
#         global_reports["risk_evaluation_report"] = agent.generate_risk_evaluation_report(risk_analysis_report)
#         print(global_reports["risk_evaluation_report"])
#         return jsonify({"Risk_Evaluation_Report": global_reports["risk_evaluation_report"]})
    
#     return jsonify({"error": "Risk analysis report not specified"}), 400
@app.route('/print_contents', methods=['POST'])
def print_contents():
    data = request.get_json()
    risk_analysis_report = data.get('risk_analysis_report', '').strip()

    print("Received Risk Analysis Report for Printing:", repr(risk_analysis_report))  # Print the received data

    return jsonify({"status": "success", "message": "Data printed successfully."})


@app.route('/generate_risk_evaluation', methods=['POST'])
def generate_risk_evaluation():
    data = request.get_json()
    risk_analysis_report = data.get('risk_analysis_report', '')

    print("Received Risk Analysis Report:", risk_analysis_report)  # Debugging line

    if risk_analysis_report.strip():
        global_reports["risk_evaluation_report"] = agent.generate_risk_evaluation_report(risk_analysis_report)
        print(global_reports["risk_evaluation_report"])
        return jsonify({"Risk_Evaluation_Report": global_reports["risk_evaluation_report"]})
    
    return jsonify({"error": "Risk analysis report not specified"}), 400

# @app.route('/generate_risk_evaluation', methods=['POST'])
# def generate_risk_evaluation():

#     risk_evaluation_report = agent.generate_risk_evaluation_report(risk_analysis_report)
#     print( " 888888 ",risk_analysis_report)
#     return jsonify({"Risk_Evaluation_Report": risk_evaluation_report})
#     return jsonify({"error": "Risk analysis report not specified"}), 400


@app.route('/generate_risk_control', methods=['POST'])
def generate_risk_control():
    global global_reports
    if global_reports["risk_evaluation_report"]:
        global_reports["risk_control_report"] = agent.generate_risk_control_report(global_reports["risk_evaluation_report"])
        return jsonify({"Risk_Control_Report": global_reports["risk_control_report"]})
    return jsonify({"error": "Risk evaluation report not specified"}), 400

@app.route('/generate_risk_management_review', methods=['POST'])
def generate_risk_management_review():
    global global_reports
    if global_reports["evaluation_of_overall_residual_risk_report"]:
        global_reports["risk_management_review_report"] = agent.generate_risk_management_review_report(global_reports["evaluation_of_overall_residual_risk_report"])
        return jsonify({"Risk_Management_Review_Report": global_reports["risk_management_review_report"]})
    return jsonify({"error": "Evaluation of overall residual risk report not specified"}), 400

@app.route('/generate_production_and_post_production_activities', methods=['POST'])
def generate_production_and_post_production_activities():
    global global_reports
    if global_reports["risk_management_review_report"]:
        global_reports["production_and_post_production_activities_report"] = agent.generate_production_and_post_production_activities_report(global_reports["risk_management_review_report"])
        return jsonify({"Production_and_Post_Production_Activities_Report": global_reports["production_and_post_production_activities_report"]})
    return jsonify({"error": "Risk management review report not specified"}), 400



@app.route('/select_component', methods=['POST'])
def update_hazard_text():
    global selected_component
    data = request.get_json()
    if data and 'component' in data:
        selected_component = data['component']
    
    updated_text = data.get('updated_text', '')
    print(f'Component: {selected_component}')
    # Perform any additional processing or database updates here
    return jsonify({"message": "Component updated successfully"})

@app.route('/select_hazared', methods=['POST'])
def select_hazared():
    global selected_hazared
    data = request.get_json()
    if data and 'hazared' in data:
        selected_hazared = data['hazared']
        print(f'Hazared selected: {selected_hazared}')
        # Perform any additional processing or database updates here
        return jsonify({"message": "Hazared selection successful"})
    return jsonify({"error": "No hazared provided"}), 400



@app.route('/text_correction_risk_analysis', methods=['POST'])
def text_correction_risk_analysis():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    print(corrected_text)
    return jsonify(corrected_text=corrected_text)

@app.route('/text_correction_risk_evaluation', methods=['POST'])
def text_correction_risk_evaluation():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    return jsonify(corrected_text=corrected_text)

@app.route('/text_correction_risk_control', methods=['POST'])
def text_correction_risk_control():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    return jsonify(corrected_text=corrected_text)

@app.route('/text_correction_residual_risk', methods=['POST'])
def text_correction_residual_risk():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    return jsonify(corrected_text=corrected_text)

@app.route('/text_correction_management_review', methods=['POST'])
def text_correction_management_review():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    return jsonify(corrected_text=corrected_text)

@app.route('/text_correction_production_activities', methods=['POST'])
def text_correction_production_activities():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    return jsonify(corrected_text=corrected_text)


def extract_components_and_hazards(description):
    # Placeholder logic to extract components and hazards from the description
    # In a real scenario, you would use NLP techniques or predefined rules to extract meaningful data
    components = ["Component1", "Component2", "Component3"]
    hazards = ["Hazard1", "Hazard2", "Hazard3"]
    return components, hazards

@app.route('/generate_suggestions', methods=['POST'])
def generate_suggestions():
    data = request.get_json()
    description = data.get('description', '').strip()

    if description:
        agent = CompletingAgent()
        result = agent.generate_output(description)

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to generate suggestions"}), 500

    return jsonify({"error": "Description not provided"}), 400

@app.route('/generate_hazards', methods=['POST'])
def generate_hazards():
    data = request.get_json()
    description = data.get('description', '').strip()
    component = data.get('component', '').strip()

    if description and component:
        agent = CompletingAgent()
        result = agent.generate_hazards(description, component)

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to generate hazards"}), 500

    return jsonify({"error": "Description or component not provided"}), 400
if __name__ == '__main__':
    app.run(debug=True)



    data = request.get_json()
