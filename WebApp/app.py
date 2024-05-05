from flask import Flask, render_template, jsonify, request
import openai
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Your OpenAI API key

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
def index():
    return render_template('index.html')

@app.route('/get_failure_modes', methods=['POST'])
def get_failure_modes():
    data = request.get_json()
    if data and 'device' in data:
        device = data['device']
        prompt = f"List potential failure modes for a {device}. Each point should be clearly numbered:"
        response = get_gpt_response(prompt_settings(prompt, "Format as a numbered list."))
        return jsonify({"failure_modes": response.split('\n')})
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



if __name__ == '__main__':
    app.run(debug=True)




