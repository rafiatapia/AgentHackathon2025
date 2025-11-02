//npm install @aws-sdk/client-bedrock-agent-runtime

const { BedrockAgentRuntimeClient, RetrieveAndGenerateCommand } = require("@aws-sdk/client-bedrock-agent-runtime");

/**
 * Query a Bedrock Knowledge Base
 * @param {string} knowledgeBaseId - The ID of the Bedrock Knowledge Base
 * @param {string} prompt - The user's query/prompt
 * @param {string} region - AWS region (default: us-east-1)
 * @returns {Promise} - Response containing the generated text and citations
 */
async function queryBedrockKnowledgeBase(knowledgeBaseId, prompt, region = "us-east-1") {
    // Initialize the Bedrock Agent Runtime client
    const client = new BedrockAgentRuntimeClient({ region });

    // Prepare the command
    const command = new RetrieveAndGenerateCommand({
        input: {
            text: prompt
        },
        retrieveAndGenerateConfiguration: {
            type: "KNOWLEDGE_BASE",
            knowledgeBaseConfiguration: {
                knowledgeBaseId: knowledgeBaseId,
                modelArn: `arn:aws:bedrock:${region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0`
            }
        }
    });

    try {
        // Send the command
        const response = await client.send(command);
        
        // Extract the generated text
        const generatedText = response.output.text;
        
        // Extract citations if available
        const citations = response.citations || [];
        
        return {
            answer: generatedText,
            citations: citations,
            sessionId: response.sessionId
        };
    } catch (error) {
        console.error("Error querying Bedrock Knowledge Base:", error);
        throw error;
    }
}

// Example usage
async function main() {
    const knowledgeBaseId = "YOUR_KB_ID_HERE";
    const prompt = "What is Amazon Bedrock?";
    
    try {
        const result = await queryBedrockKnowledgeBase(knowledgeBaseId, prompt);
        console.log("Answer:", result.answer);
        console.log("\nCitations:", JSON.stringify(result.citations, null, 2));
    } catch (error) {
        console.error("Failed to query knowledge base:", error);
    }
}

// Uncomment to run
// main();

module.exports = { queryBedrockKnowledgeBase };
