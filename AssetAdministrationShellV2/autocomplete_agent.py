# import openai
# from flask import jsonify, request

# class AutoCompleteAgent:
#     def __init__(self, api_key):
#         # Initialize the OpenAI API key
#         self.api_key = api_key
#         openai.api_key = self.api_key

#     def generate_prompt(self, context, user_input, additional_context=""):
#         """
#         Generate a prompt based on the context, user input, and additional context.

#         :param context: The context of the autocomplete (e.g., 'file_content', 'failure_mode').
#         :param user_input: The user's input text.
#         :param additional_context: Additional context or data to include in the prompt.
#         :return: A string prompt for the AI model.
#         """
#         # Base prompt for the assistant
#         base_prompt = "You are an intelligent autocomplete system for risk management. Provide suggestions."

#         # Dictionary to map contexts to specific prompts
#         context_prompts = {
#             'file_content': "The file is about making a hazard analysis for a specific component in a digital twin. Please generate additional hazards if any are missing, following the same format as before. User input includes priorities and component details: {additional_context}.",
#             'failure_mode': "You are assisting a risk analysis engineer. Based on the provided hazard analysis {additional_context}, please generate a Risk Analysis report addressing the following points: 1. Intended use and foreseeable misuse. 2. Safety-related characteristics. 3. Hazards and hazardous situations. 4. Risk estimation for each situation.",
#             'evaluations': """You are assisting a risk analysis engineer. Based on the Risk Analysis: {additional_context}, please generate a Risk Evaluation for each hazard  addressing:

#             "risk_acceptability": "Determine if the risks meet acceptability criteria.",
#             "risk_control_measures": "Identify and evaluate control measures for each hazard. Include the following information for each control measure:
#             "measure": "Description of the control measure",
#             "practicability": "Evaluation of practicability"
    
#             "residual_risk": "Assess if the residual risk is acceptable."
            
#             Ensure adherence to these criteria for the evaluation.""",
#             'risk_control': """Provide suggestions for risk control measures. You are assisting a risk analysis engineer. Based on the evaluation data: {additional_context}, generate a report according to ISO risk analysis standards, including:

#             Risk control option analysis:
#             - Is risk control required?
#             - If yes, identify appropriate control measures.
#             - If no, assess new hazards or risk changes.
#             - Is control practicable?
#             - If yes, implement and verify measures.
#             - If no, assess new hazards or risk changes.
#             """,
#             'results': "Suggest potential results or conclusions for the risk management process based on the data provided: {additional_context}.",
#             'management_review': "Provide suggestions for management review insights or improvements. Consider the management data: {additional_context}."
#         }

#         print("Context:", context)
#         print("Additional Context:", additional_context)
#         print("User Input:", user_input)

#         # Format the prompt with additional context
#         context_prompt = context_prompts.get(context, "").format(additional_context=additional_context)

#         # Combine base prompt with the context-specific prompt
#         return f"{base_prompt} {context_prompt} User input: {user_input}"

#     def get_suggestion(self, context, user_input, additional_context=""):
#         """
#         Get a suggestion from the AI model based on the context, user input, and additional context.

#         :param context: The context of the autocomplete (e.g., 'file_content', 'failure_mode').
#         :param user_input: The user's input text.
#         :param additional_context: Additional context or data to include in the prompt.
#         :return: The AI-generated suggestion.
#         """
#         try:
#             # Generate the appropriate prompt
#             prompt = self.generate_prompt(context, user_input, additional_context)

#             # Use OpenAI API to get the chat completion
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant providing suggestions."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=150,  # Adjust this as needed for your application
#                 temperature=0.7
#             )

#             # Extract and return the suggestion from the response
#             suggestion = response.choices[0].message['content'].strip()
#             return suggestion

#         except openai.error.OpenAIError as e:
#             # Handle OpenAI API errors
#             print(f"OpenAI API error: {e}")
#             raise Exception("Error while fetching suggestion from OpenAI.")
#         except Exception as e:
#             # Handle other unexpected errors
#             print(f"Unexpected error: {e}")
#             raise Exception("An unexpected error occurred while generating suggestions.")


import openai
from flask import jsonify, request

class AutoCompleteAgent:
    def __init__(self, api_key):
        # Initialize the OpenAI API key
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_prompt(self, context, user_input, additional_context=""):
        """
        Generate a prompt based on the context, user input, and additional context.

        :param context: The context of the autocomplete (e.g., 'file_content', 'failure_mode').
        :param user_input: The user's input text.
        :param additional_context: Additional context or data to include in the prompt.
        :return: A string prompt for the AI model.
        """
        # Base prompt for the assistant
        base_prompt = "You are an intelligent autocomplete system for risk management. Provide suggestions."

        # Dictionary to map contexts to specific prompts
        context_prompts = {
            'file_content': "The file is about making a hazard analysis for a specific component in a digital twin. Please generate additional hazards if any are missing, following the same format as before. User input includes priorities and component details: {additional_context}.",
            'failure_mode': "You are assisting a risk analysis engineer. Based on the provided hazard analysis {additional_context}, please generate a Risk Analysis report addressing the following points: 1. Intended use and foreseeable misuse. 2. Safety-related characteristics. 3. Hazards and hazardous situations. 4. Risk estimation for each situation.",
            'evaluations': """You are assisting a risk analysis engineer. Based on the Risk Analysis: {additional_context}, please generate a Risk Evaluation for each hazard  addressing:

            "risk_acceptability": "Determine if the risks meet acceptability criteria.",
            "risk_control_measures": "Identify and evaluate control measures for each hazard. Include the following information for each control measure:
            "measure": "Description of the control measure",
            "practicability": "Evaluation of practicability"
    
            "residual_risk": "Assess if the residual risk is acceptable."
            
            Ensure adherence to these criteria for the evaluation.""",
            'risk_control': """Provide suggestions for risk control measures. You are assisting a risk analysis engineer. Based on the evaluation data: {additional_context}, generate a report according to ISO risk analysis standards, including:

            Risk control option analysis:
            - Is risk control required?
            - If yes, identify appropriate control measures.
            - If no, assess new hazards or risk changes.
            - Is control practicable?
            - If yes, implement and verify measures.
            - If no, assess new hazards or risk changes.
            """,
            'results': "Suggest potential results or conclusions for the risk management process based on the data provided: {additional_context}.",
            'management_review': "Provide suggestions for management review insights or improvements. Consider the management data: {additional_context}."
        }

        # Debugging logs
        print("Context:", context)
        print("Additional Context:", additional_context)
        print("User Input:", user_input)

        # Format the prompt with additional context
        context_prompt = context_prompts.get(context, "").format(additional_context=additional_context)

        # Combine base prompt with the context-specific prompt
        return f"{base_prompt} {context_prompt} User input: {user_input}"

    def get_suggestion(self, context, user_input, additional_context=""):
        """
        Get a suggestion from the AI model based on the context, user input, and additional context.

        :param context: The context of the autocomplete (e.g., 'file_content', 'failure_mode').
        :param user_input: The user's input text.
        :param additional_context: Additional context or data to include in the prompt.
        :return: The AI-generated suggestion.
        """
        try:
            # Generate the appropriate prompt
            prompt = self.generate_prompt(context, user_input, additional_context)

            # Use OpenAI API to get the chat completion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant providing suggestions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,  # Adjust this as needed for your application
                temperature=0.7
            )

            # Extract and return the suggestion from the response
            suggestion = response.choices[0].message['content'].strip()
            return suggestion

        except openai.error.OpenAIError as e:
            # Handle OpenAI API errors
            print(f"OpenAI API error: {e}")
            raise Exception("Error while fetching suggestion from OpenAI.")
        except Exception as e:
            # Handle other unexpected errors
            print(f"Unexpected error: {e}")
            raise Exception("An unexpected error occurred while generating suggestions.")


