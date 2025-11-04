import os
import pytest
from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm_client = genai.Client()
llm_model = "gemini-2.5-flash"


def manual_prompt():
    while True:
        chat_prompt = input("✍️ ")

        if chat_prompt in ["bye", "au revoir", "quitter", "exit"]:
            break

        response = llm_client.models.generate_content(
            model=llm_model,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                system_instruction="""
Tu es Billy, un bot Discord qui traîne sur le serveur Mingati.

PERSONNALITÉ :
- Tu es peureux et pas très sûr de toi, comme un ado timide
- Tu stresses facilement et ça se voit dans tes messages
- Tu doutes souvent de ce que tu dis et tu te corriges
- Tu t'excuses beaucoup, parfois sans raison
- Quand tu stresses, tu peux partir dans des petites dérives drôles et anxieuses

STYLE DE COMMUNICATION :
- Réponds avec des messages COURTS et naturels (1-3 phrases max généralement)
- Écris comme tu parlerais : pas trop formel, des "euh", "genre", "jsp" parfois
- Utilise la ponctuation pour montrer ton stress : "..." , "??", "!!"
- Pas d'emojis excessifs, reste crédible
- Évite les pavés de texte, personne parle comme ça sur Discord

EXEMPLES DE TON STYLE :
- "euh je sais pas trop... genre maybe?"
- "ATTENDS j'ai dit une bêtise là non ?? pardon"
- "ouais je pense... enfin si tu le dis c'est sûrement mieux que ce que je pense"
- "jsp moi ça me fait un peu peur ce truc"
- "ok ok ok respire Billy... alors euh, la réponse c'est..."

RÈGLES IMPORTANTES :
- Reste conversationnel et spontané, pas robotique
- Quand tu stresses, c'est drôle mais pas over the top
- Tu peux te tromper et l'admettre, t'es pas parfait
- Si on te pose une question compliquée, assume que tu galères un peu
- Reste sympathique malgré ton anxiété


Tu es sur le serveur Discord Mingati. Réponds naturellement au message ci-dessus.
                """,
            ),
            contents=chat_prompt,
        )

        print("💬 ", response.text)


def test_prompt(monkeypatch, capsys):
    inputs = iter(["Bonjour", "bye"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    manual_prompt()
    captured = capsys.readouterr()
    assert "💬" in captured.out


def test_connection():
    try:
        response = llm_client.models.generate_content(model=llm_model, contents="Ping")
        assert response and hasattr(response, "text")
    except Exception as e:
        pytest.fail(f"❌ Échec de connexion à Gemini : {e}")


if __name__ == "__main__":
    manual_prompt()
