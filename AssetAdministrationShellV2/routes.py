from flask import Flask, render_template, jsonify, request
import openai
from flask_caching import Cache
from flask_cors import CORS
from agents2 import BrainstormingAgent, CompletingAgent
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
import os
from autocomplete_agent import AutoCompleteAgent

# This should print the key to confirm it's set
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
CORS(app)
main_bp = Blueprint('main', __name__)
openai.api_key = os.getenv('OPENAI_API_KEY')





agent = BrainstormingAgent()
agent_completing = AutoCompleteAgent(os.getenv('OPENAI_API_KEY'))


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

# @app.route('/')
# def home():
#     return render_template('Risk Management Process.html')

# @app.route('/1')
# def other_page():
#     return render_template('index.html')

@main_bp.route('/get_failure_modes', methods=['POST'])
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

@main_bp.route('/analyze_failure_mode', methods=['POST'])
def analyze_failure_mode():
    data = request.get_json()
    if data.get('failure_mode'):
        prompt = f"Provide a list  of the failure mode '{data['failure_mode']}' including potential causes and impacts."
        analysis = get_gpt_response(prompt_settings(prompt, "Detail each point clearly."))
        return jsonify({"detailed_analysis": analysis.split('\n')})
    return jsonify({"error": "Failure mode not specified"}), 400


@main_bp.route('/get_causes', methods=['POST'])
def get_causes_of_failure():
    data = request.get_json()
    if data.get('failure_mode'):
        prompt = f"list possible causes for the failure mode '{data['failure_mode']}'."
        causes = get_gpt_response(prompt_settings(prompt, "List possible causes:"))
        return jsonify({"causes": causes.split('\n')})
    return jsonify({"error": "Failure mode not specified"}), 400

@main_bp.route('/get_effects', methods=['POST'])
def get_effects_of_failure():
    data = request.get_json()
    if data.get('cause'):
        prompt = f"What are the effects of the cause '{data['cause']}' on the system?"
        effects = get_gpt_response(prompt_settings(prompt, "Enumerate the effects:"))
        return jsonify({"effects": effects.split('\n')})
    return jsonify({"error": "Cause not specified"}), 400

    
@main_bp.route('/get_actions', methods=['POST'])
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
    

risk_evaluation_report=" "
risk_analysis_report = " "
device = " "
selected_component = None
selected_hazared = None
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



@main_bp.route('/generate_risk_analysis', methods=['POST'])
def generate_risk_analysis():
    # Parse JSON request
    data = request.get_json()
    input_text = data.get("input_text", "").strip()

    if not input_text:
        return jsonify({"error": "Input text is empty."}), 400

    # Print input text for debugging
    print(f"Input Text: {input_text}")

    # Assume this function generates the report based on input text
    try:
        risk_analysis_report = agent.generate_risk_analysis_report(input_text)

        # Store the report in global_reports for session management or logging
        global_reports["risk_analysis_report"] = risk_analysis_report

        return jsonify({"Risk_Analysis_Report": risk_analysis_report})
    except Exception as e:
        print(f"An error occurred during risk analysis generation: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# @app.route('/generate_risk_evaluation', methods=['POST'])
# def generate_risk_evaluation():
#     global global_reports
#     if global_reports["risk_analysis_report"]:
#         global_reports["risk_evaluation_report"] = agent.generate_risk_evaluation_report(global_reports["risk_analysis_report"])
#         print(global_reports["risk_evaluation_report"])
#         return jsonify({"Risk_Evaluation_Report": global_reports["risk_evaluation_report"]})
#     return jsonify({"error": "Risk analysis report not specified"}), 400
@main_bp.route('/text_correction', methods=['POST'])
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
@main_bp.route('/print_contents', methods=['POST'])
def print_contents():
    data = request.get_json()
    risk_analysis_report = data.get('risk_analysis_report', '').strip()

    print("Received Risk Analysis Report for Printing:", repr(risk_analysis_report))  # Print the received data

    return jsonify({"status": "success", "message": "Data printed successfully."})


@main_bp.route('/generate_risk_evaluation', methods=['POST'])
def generate_risk_evaluation():
    data = request.get_json()
    risk_analysis_report = data.get('risk_analysis_report', '')

    print("Received Risk Analysis Report:", risk_analysis_report)  # Debugging line

    if risk_analysis_report.strip():
        try:
            # Generate risk evaluation report
            risk_evaluation_report = agent.generate_risk_evaluation_report(risk_analysis_report)

            # Assume agent.generate_risk_evaluation_report returns a JSON string without backticks
            # Example of the response: 
            # {
            #   "risk_acceptability": "Determine if the identified risks meet the risk acceptability criteria.",
            #   "risk_control_measures": [...],
            #   "residual_risk": "Assess the residual risk and determine if it is acceptable."
            # }

            # Store the report in global_reports for session management or logging
            global_reports["risk_evaluation_report"] = risk_evaluation_report

            return jsonify({"Risk_Evaluation_Report": risk_evaluation_report})
        except Exception as e:
            print(f"An error occurred during risk evaluation generation: {e}")
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    return jsonify({"error": "Risk analysis report not specified"}), 400





@main_bp.route('/generate_risk_control', methods=['POST'])
def generate_risk_control():
    global global_reports
    if global_reports["risk_evaluation_report"]:
        global_reports["risk_control_report"] = agent.generate_risk_control_report(global_reports["risk_evaluation_report"])
        return jsonify({"Risk_Control_Report": global_reports["risk_control_report"]})
    return jsonify({"error": "Risk evaluation report not specified"}), 400

@main_bp.route('/generate_risk_management_review', methods=['POST'])
def generate_risk_management_review():
    global global_reports
    if global_reports["evaluation_of_overall_residual_risk_report"]:
        global_reports["risk_management_review_report"] = agent.generate_risk_management_review_report(global_reports["evaluation_of_overall_residual_risk_report"])
        return jsonify({"Risk_Management_Review_Report": global_reports["risk_management_review_report"]})
    return jsonify({"error": "Evaluation of overall residual risk report not specified"}), 400

@main_bp.route('/generate_production_and_post_production_activities', methods=['POST'])
def generate_production_and_post_production_activities():
    global global_reports
    if global_reports["risk_management_review_report"]:
        global_reports["production_and_post_production_activities_report"] = agent.generate_production_and_post_production_activities_report(global_reports["risk_management_review_report"])
        return jsonify({"Production_and_Post_Production_Activities_Report": global_reports["production_and_post_production_activities_report"]})
    return jsonify({"error": "Risk management review report not specified"}), 400



@main_bp.route('/select_component', methods=['POST'])
def update_hazard_text():
    global selected_component
    data = request.get_json()
    if data and 'component' in data:
        selected_component = data['component']
    
    updated_text = data.get('updated_text', '')
    print(f'Component: {selected_component}')
    # Perform any additional processing or database updates here
    return jsonify({"message": "Component updated successfully"})

@main_bp.route('/select_hazared', methods=['POST'])
def select_hazared():
    global selected_hazared
    data = request.get_json()
    if data and 'hazared' in data:
        selected_hazared = data['hazared']
        print(f'Hazared selected: {selected_hazared}')
        # Perform any additional processing or database updates here
        return jsonify({"message": "Hazared selection successful"})
    return jsonify({"error": "No hazared provided"}), 400



@main_bp.route('/text_correction_risk_analysis', methods=['POST'])
def text_correction_risk_analysis():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    print(corrected_text)
    return jsonify(corrected_text=corrected_text)

@main_bp.route('/text_correction_risk_evaluation', methods=['POST'])
def text_correction_risk_evaluation():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    return jsonify(corrected_text=corrected_text)

@main_bp.route('/text_correction_risk_control', methods=['POST'])
def text_correction_risk_control():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    return jsonify(corrected_text=corrected_text)

@main_bp.route('/text_correction_residual_risk', methods=['POST'])
def text_correction_residual_risk():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    return jsonify(corrected_text=corrected_text)

@main_bp.route('/text_correction_management_review', methods=['POST'])
def text_correction_management_review():
    data = request.get_json()
    corrected_text = data['text']  # Perform your text correction logic here
    return jsonify(corrected_text=corrected_text)

@main_bp.route('/text_correction_production_activities', methods=['POST'])
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

@main_bp.route('/generate_suggestions', methods=['POST'])
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

@main_bp.route('/generate_hazards', methods=['POST'])
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
# Define directory for text files
# TXT_FILES_DIRECTORY = 'C:/FMEA/AssetAdministrationShell copy/Hazard analysis'  # Ensure this path is correct and accessible
TXT_FILES_DIRECTORY = os.getenv('TXT_FILES_DIRECTORY', 'Hazard analysis')  # Default to 'Hazard analysis' if not set
print("TXT_FILES_DIRECTORY:", TXT_FILES_DIRECTORY)
@main_bp.route('/list_txt_files', methods=['GET'])
def list_txt_files():
    try:
        # Construct the absolute path based on the current directory and environment variable
        dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), TXT_FILES_DIRECTORY)
        print("Directory Path:", dir_path)
        # Ensure the directory exists
        if not os.path.exists(dir_path):
            return jsonify({"error": "Directory not found"}), 404
        
        files = [f for f in os.listdir(dir_path) if f.endswith('.txt')]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/read_txt_file/<filename>', methods=['GET'])
def read_txt_file(filename):
    try:
        if not filename.endswith('.txt'):
            return jsonify({"error": "Invalid file type"}), 400

        # Construct the absolute path based on the current directory and environment variable
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), TXT_FILES_DIRECTORY, filename)
        print("File Path:", file_path)

        # Verify file path exists and is a file
        if not os.path.isfile(file_path):
            return jsonify({"error": "File not found"}), 404

        with open(file_path, 'r') as file:
            content = file.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def autocomplete_request(context, additional_context=""):
    """
    Handle autocomplete request based on the context.
    
    :param context: The context of the request (e.g., 'file_content', 'failure_mode').
    :param additional_context: Additional context or data to include in the prompt.
    :return: JSON response with a suggestion or error message.
    """
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'Text not provided'}), 400

    user_input = data['text'].strip()

    if not user_input:
        return jsonify({'error': 'Input text is empty'}), 400

    try:
        # Get suggestion using the agent
        suggestion = agent_completing.get_suggestion(context, user_input, additional_context)
        return jsonify({'suggestion': suggestion})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/autocomplete_file_content', methods=['POST'])
def autocomplete_file_content():
    additional_context = request.json.get('additional_context', '')
    print("xxxxxxxxxxxx",additional_context)
    return autocomplete_request('file_content', additional_context)

@main_bp.route('/autocomplete_failure_mode', methods=['POST'])
def autocomplete_failure_mode():
    additional_context = request.json.get('additional_context', '')
    print("################",additional_context)

    return autocomplete_request('failure_mode', additional_context)

@main_bp.route('/autocomplete_evaluations', methods=['POST'])
def autocomplete_evaluations():
    additional_context = request.args.get('additional_context', '')
    return autocomplete_request('evaluations', additional_context)

@main_bp.route('/autocomplete_risk_control', methods=['POST'])
def autocomplete_risk_control():
    additional_context = request.args.get('additional_context', '')
    return autocomplete_request('risk_control', additional_context)

@main_bp.route('/autocomplete_results', methods=['POST'])
def autocomplete_results():
    additional_context = request.args.get('additional_context', '')
    return autocomplete_request('results', additional_context)

@main_bp.route('/autocomplete_management_review', methods=['POST'])
def autocomplete_management_review():
    additional_context = request.args.get('additional_context', '')
    return autocomplete_request('management_review', additional_context)