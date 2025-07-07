"""Tools for the resolutions agent."""

import os
from typing import Any

from vertexai import rag
from vertexai.generative_models import GenerativeModel

from utils import extract_and_concatenate_rag_content  # type: ignore

summary_model = GenerativeModel(
    model_name=os.environ.get('GOOGLE_CLOUD_LLM_NAME', '')
)


def get_intent_resolution_instructions(
    intent: str, customer_motivation: str
) -> Any:
    """Classifies the user intent based on the provided information.

    Args:
        intent (str): A high level generic title for the user's intent.
        customer_motivation (str): A brief description of the user's motivation
            for contacting The Home Depot.

    Returns:
        str: If an intent is identified then the function will return
        step-by-step instructions to resolve the user's intent. Otherwise,
        it will return a message asking the user for more clarity on
        their intent.

    Example:
        >>> get_intent_resolution_instructions(
                 intent = "Account Security",
                 customer_motivation = "The customer is experiencing issues
                    with their Home Depot account, such as orders not
                    appearing, unauthorized access attempts, or
                    difficulty linking purchases to their account."
    """
    print('\n\n\n\n\nClassifying intent...........')
    response = (
        'I am struggling to understand. Please provide more details '
        'about your reason for contacting The Home Depot so I can assist you '
        'better.'
    )

    if intent:
        text = f"""Intent: {intent},
        Customer Motivation: {customer_motivation}"""

        # Direct context retrieval
        rag_retrieval_config = rag.RagRetrievalConfig(
            top_k=3,
        )

        try:
            response = rag.retrieval_query(
                rag_resources=[
                    rag.RagResource(
                        rag_corpus=os.environ.get('RAG_CORPUS'),
                    )
                ],
                text=text,
                rag_retrieval_config=rag_retrieval_config,
            )

            response = extract_and_concatenate_rag_content(response)

            prompt = f"""Given the following intent, customer motivation, and
            resolution goals,
            {text}
            and the following step-by-step instructions retrieved from the
            RAG engine,
            {response}
            Please summarizer the likely step-by-step instructions an agent
            would need to follow to relove the given intent, customer
              motivation, and resolution goals

            """

            response = summary_model.generate_content(prompt)
            response = response.text.strip()

        except Exception as e:
            print(f'Error during RAG retrieval: {e}')

    print(f'RESPONSE: {response}')
    print('Returning response...\n\n\n\n\n\n\n\n\n')
    return response
