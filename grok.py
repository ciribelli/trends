import requests
import logging

def consulta_grok(token):
    logging.info('entrei na funcao do grok...v2')

    url = "https://api.x.ai/v1/responses"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "model": "grok-4-latest",
        "tools": [
            {
                "type": "web_search",
                "max_results": 5
            }
        ],
        "input": [
            {
                "role": "system",
                "content": "Você é um assistente que responde em português de forma objetiva. Máximo 2000 caracteres."
            },
            {
                "role": "user",
                "content": "Summarize the latest news from the last 24h about: generative AI, AI accelerators (NVIDIA-like GPUs), open-source AI agent frameworks, coworkers, and big tech movements. Responda em português. If nothing relevant, answer: 'Nenhuma novidade'."
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()
    logging.info(data)

    # Novo formato de resposta
    try:
        for item in data.get("output", []):
            if item.get("type") == "message" and "content" in item:
                return item["content"][0]["text"]
        return None
    except Exception as e:
        logging.error(f"Erro ao parsear resposta: {e}")
        return None