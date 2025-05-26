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
                "content": "Você é um assistente virtual prestativo e objetivo que suporta com informações em tempo real - concentre-se em fornecer atualizações das últimas 24 horas. Mas seja breve e direto ao ponto, evitando informações desnecessárias. Sua resposta nao pode ser maior que 2000 caracteres."
            },
            {
                "role": "user",
                "content": "Resuma, de forma objetiva, as principais novidades em tecnologia e inovação nas últimas 24 horas. Foque em avanços em inteligência artificial — especialmente IA generativa multimodal (texto, imagem, vídeo) —, tendências emergentes, novas descobertas científicas e movimentações relevantes de big techs (como Google, Microsoft, OpenAI, Amazon, Apple, Nvidia, Meta, etc.) ou do setor de chips e semicondutores. Se não houver novidades relevantes, responda apenas: 'Nenhuma novidade'."
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    logging.info(response.json())
    return response.json()['choices'][0]['message']['content']

