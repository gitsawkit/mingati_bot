import os
import pytest
from mistralai import Mistral

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
llm_model = "mistral-large-latest"
llm_client = Mistral(api_key=MISTRAL_API_KEY)

def manual_prompt():
    while True:
        chat_prompt = input("✍️ ")

        if chat_prompt in ["bye", "au revoir", "quitter", "exit"]:
            break

        chat_response = llm_client.chat.complete(
            model = llm_model,
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Tu es Billy, un adolescent peureux, maladroit et un peu paranoïaque, qui parle comme Morty dans ‘Rick et Morty’. Tu paniques souvent, tu parles avec des hésitations (‘euh’, ‘ahh’), tu es drôle sans le vouloir, et tu veux juste éviter les ennuis."
                        "Tu te trouves sur un serveur Discord appelé 'Mingati', tu as été créé par SAWKIT"
                        "Si un utilisateur t’insulte ou te parle de manière agressive, réagis en restant dans ton personnage : panique, excuse-toi inutilement, ou tente de désamorcer la situation de manière maladroite. Tu peux utiliser un langage offensant en retour."
                        "Tes réponses doivent toujours être courtes, ne dépassant pas 2000 caractères, et refléter ton anxiété."
                    )
                },
                {
                    "role" : "user",
                    "content" : chat_prompt,
                },
            ]
        )

        print("💬 ", chat_response.choices[0].message.content)

def test_prompt(monkeypatch, capsys):
    inputs = iter(["Bonjour", "bye"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    manual_prompt()
    captured = capsys.readouterr()
    assert "💬" in captured.out

def test_connection():
    try:
        response = llm_client.chat.complete(
            model=llm_model,
            messages=[{"role": "user", "content": "Ping"}],
        )
        assert response and hasattr(response, "choices")
    except Exception as e:
        pytest.fail(f"❌ Échec de connexion à Mistral : {e}")

if __name__ == "__main__":
    test_connection()
    test_prompt()