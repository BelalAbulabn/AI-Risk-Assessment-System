import openai

# Set your API key here
openai.api_key = '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'

def query_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Confirm this is the correct model
            messages=[{"role": "system", "content": "Start a new conversation."},
                      {"role": "user", "content": prompt}]
        )
        # Assuming the latest response is what you need
        return response['choices'][0]['message']['content']
    except openai.APIError as e:
        return f"An API error occurred: {e}"
    except openai.RateLimitError as e:
        return "Rate limit exceeded. Please try later."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example prompt
prompt_text = "Explain the benefits of AI in education."
response_text = query_openai(prompt_text)
print("Generated Response:", response_text)