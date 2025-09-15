# Portfolio Assistant

This is a conversational assistant developed to answer questions about my portfolio and qualifications. It utilizes Azure Functions, Python, and Azure AI Foundry and is deployed via GitHub Actions.  

## Project Structure
├── host.json # Azure Functions host configuration  
├── local.settings.json # Local environment variables (not included in repository, not for production)  
├── requirements.txt # Dependencies  
├── .github/workflows/ # GitHub Actions pipeline  
│ └── deploy.yml  
├── ChatFunction/ # Azure Function entrypoint  
│ ├── __init__.py  
│ └── function.json  
├── src/portfolio_assistant/  
│ ├── agent_client.py # Client for Azure AI Foundry chat agent  
│ ├── config.py  
│ ├── utils.py   
│ ├── search_client.py # (Added feature coming soon!)  
│ └── __init__.py  
└── tests/ # Unit tests (pytest)  
├── test_agent_client.py  
├── test_api.py  
└── test_search_client.py # (Added feature coming soon!)  

## Setup Instructions
```bash
git clone https://github.com/vmgaribay/portfolio-assistant.git
cd portfolio-assistant
python -m venv .venv
source .venv/bin/activate   # or for Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
## Running Locally
It is necessary to create your own Azure OpenAI resource and deploy a chat model to obtain the endpoint and API key (I tested with 4.1-mini for a balance of cost and performance).

Prerequisites:
- Azure Functions Core Tools
- Python 3.10 
- An endpoint and key for an Azure OpenAI resource with a deployed chat model

Set up local environment variables in `local.settings.json`:  
```json
{  
  "IsEncrypted": false,  
  "Values": {  
    "FUNCTIONS_WORKER_RUNTIME": "python",  
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",  
    "AZURE_CHAT_AGENT_ENDPOINT": "<your-endpoint>",  
    "AZURE_CHAT_API_KEY": "<your-api-key>"  
  }  
}
```

Run the Azure Function locally:
```bash
func start
```

Test the API endpoint:
```bash
curl -X POST http://localhost:7071/api/chat-function -H "Content-Type: application/json" -d '{"message": "Is this functioning?"}'
```

## Deployment
The project is set up to deploy automatically to Azure Functions via GitHub Actions. It is first necessary to create an Azure Function App with Python runtime since its name and publishing profile are necessary for deployment. Ensure you have the following secrets in your GitHub repository settings:
- AZURE_FUNCTIONAPP_NAME
- AZURE_FUNCTIONAPP_PUBLISH_PROFILE
Push changes to the `main` branch to trigger deployment.

## Future Enhancements
- Connect to Azure Cognitive Search for resume/project search (now in main branch!)
- GitHub Pages portfolio chat interface
- Diagram of architecture

## Acknowledgements
This project was made possible by resources such as GitHub Copilot (GPT-5, GPT-4.1, Claude Sonnet 3.7), Azure Learn, too many YouTube tutorials, patience, and willpower.

## Contact
Victoria Garibay, Ph.D. - [Contact Form](https://vmgaribay.github.io/portfolio/contact_form.html) | [GitHub Profile](https://github.com/vmgaribay)
