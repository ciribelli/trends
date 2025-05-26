import requests
import logging

def consulta_grok(token):
    logging.info('entrei na funcao do grok...')
    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


    payload = {
        "model": "grok-3-latest",
        "search_parameters": {
            "mode": "auto",
            "max_search_results": 5
        },
        "messages": [
            {
                "role": "system",
                "content": "Você é um assistente virtual prestativo e objetivo que suporta com informações em tempo real - concentre-se em fornecer atualicações das últimas 24 horas. Mas seja breve e direto ao ponto, evitando informações desnecessárias. Sua resposta nao pode ser maior que 2000 caracteres."
            },
            {
                "role": "user",
                "content": ("Faça uma atualização geral sobre as novidades de tecnologia e inovações "
                            "que estão acontecendo no mundo, incluindo tendências emergentes, "
                            "avanços em inteligência artificial, especialmente IA Generativa multimodal (texto, imagem, vídeos). Não tendo novidades, simplesmente diga 'Nenhuma novidade'.")
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    logging.info(response.json())
    return response.json()['choices'][0]['message']['content']

