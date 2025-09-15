"""
Main Azure Function for Portfolio Assistant API.
Receives user message and forwards it to the Azure AI Agent;
then, returns the response.
"""
import logging
import json
from azure.functions import HttpRequest, HttpResponse
from portfolio_assistant.agent_client import AgentClient
from portfolio_assistant.search_client import SearchClient
from portfolio_assistant.utils import configure_logging

configure_logging()


def main(req: HttpRequest) -> HttpResponse:
    """
    Azure Function trigger for portfolio assistant chat.

        Arg:
            req (HttpRequest): incoming request composed of
            data sent by the client
        Return:
            HTTP response: AI response (or error message)
    """
    logging.info("Portfolio Assistant API triggered.")
    try:
        logging.info(f"Raw body: {req.get_body()}")

        try:
            body = req.get_json()
        except Exception as e:
            try:
                logging.info(f"Attempting to decode body: {req.get_body()}")
                body = json.loads(req.get_body().decode())
            except Exception as ex:
                logging.error(f"Failed to decode body: {str(ex)}")
                return HttpResponse(
                    body=json.dumps({"error": f"Invalid JSON: {str(e)}"}),
                    status_code=400,
                    mimetype="application/json"
                )
        user_message = body.get("message")
        conversation_id = body.get("conversation_id", "default")
        if not user_message:
            return HttpResponse(
                body='{"error":"Missing user message"}',
                status_code=400,
                mimetype="application/json"
            )

        agent_client = AgentClient(search_client=SearchClient())
        ai_response = agent_client.ask(user_message, conversation_id)

        return HttpResponse(
            body=json.dumps(ai_response),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
