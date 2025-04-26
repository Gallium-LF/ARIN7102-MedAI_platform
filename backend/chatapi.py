from openai import OpenAI


def chatapi(user_message: str) -> str:
    client = OpenAI(
        api_key="your_api_key_here",
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a pharma sales assistant, you job is to help answer questions about pharma products."},
            {"role": "user", "content": user_message},
        ],
        stream=False,
    )
    return response.choices[0].message.content


def chatapi_test(user_message: str):
    return user_message
