# pip install boto3
import boto3
from typing import Dict, List, Optional
import json

def query_bedrock_knowledge_base(
    knowledge_base_id: str,
    prompt: str,
    region: str = "us-east-1",
    model_arn: Optional[str] = None
) -> Dict:
    """
    Query a Bedrock Knowledge Base
    
    Args:
        knowledge_base_id (str): The ID of the Bedrock Knowledge Base
        prompt (str): The user's query/prompt
        region (str): AWS region (default: us-east-1)
        model_arn (str): Optional model ARN. If not provided, uses Claude 3 Sonnet
        
    Returns:
        dict: Response containing the generated text and citations
    """
    # Initialize the Bedrock Agent Runtime client
    client = boto3.client(
        service_name='bedrock-agent-runtime',
        region_name=region
    )
    
    # Set default model if not provided
    if model_arn is None:
        model_arn = f"arn:aws:bedrock:{region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    
    try:
        # Call the retrieve_and_generate API
        response = client.retrieve_and_generate(
            input={
                'text': prompt
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn
                }
            }
        )
        
        # Extract the generated text
        generated_text = response['output']['text']
        
        # Extract citations if available
        citations = response.get('citations', [])
        
        return {
            'answer': generated_text,
            'citations': citations,
            'session_id': response.get('sessionId')
        }
        
    except Exception as error:
        print(f"Error querying Bedrock Knowledge Base: {error}")
        raise


# Example usage
def main():
    knowledge_base_id = "YOUR_KB_ID_HERE"
    prompt = "What is Amazon Bedrock?"
    
    try:
        result = query_bedrock_knowledge_base(knowledge_base_id, prompt)
        print("Answer:", result['answer'])
        print("\nCitations:", json.dumps(result['citations'], indent=2))
    except Exception as e:
        print(f"Failed to query knowledge base: {e}")


if __name__ == "__main__":
    main()
