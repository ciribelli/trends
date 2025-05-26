
from dotenv import load_dotenv
import requests


def consulta_grok(token):
    """
    Função para consultar a API Grok e obter informações em tempo real
    """
    load_dotenv() 

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


    payload = {
        "model": "grok-3-latest",
        "search_parameters": {
            "mode": "auto",
            "return_citations": True
        },
        "messages": [
            {
                "role": "system",
                "content": "Você é um assistente virtual prestativo e objetivo que suporta com informações em tempo real - concentre-se em fornecer atualicações das últimas 24 horas."
            },
            {
                "role": "user",
                "content": ("Faça uma atualização geral sobre as novidades de tecnologia e inovações "
                            "que estão acontecendo no mundo, incluindo tendências emergentes, "
                            "avanços em inteligência artificial, computação quântica, "
                            "tecnologias sustentáveis e inovações em hardware e software."
                            "Tendo novidades sobre IA Generativa, traga enquanto destaque.")
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

