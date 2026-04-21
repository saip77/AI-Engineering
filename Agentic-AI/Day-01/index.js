const OpenAI = require("openai");
require("dotenv").config();

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

//Tool Definition
const tools =[
    {
        type:"function",
        function: {
            name: "get_current_time",
            description: "Get the current system time",
            parameters: {
                type: "object",
                properties: {},
            },
        },   
    },
    {
        type:"function",
        function: {
            name: "get_year",
            description: "Get the current year",
            parameters: {
                type: "object",
                properties: {},
            },
        }
    },
]

// Tool Implementation
async function runTool(name, args) {
    if(name === "get_current_time") {
        return new Date().toLocaleString();
    }
    else if(name === "get_year") {
        return new Date().getFullYear().toString();
    }
    throw new Error(`Unknown tool ${name}`);
}


//Agent Loop
async function runAgent(userInput){
    let messages =[
        {role: "system", content: "You are a helpful AI agent. Use tools when needed to answer accurately."},
        {role: "user", content: userInput},
    ];
    while(true){
        const response = await client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: messages,
            tools,
        });

        const message = response.choices[0].message;

        //Handle Tool Execution
        if(message.tool_calls){
            messages.push(message);
            for(const toolCall of message.tool_calls){
                const toolResponse = await runTool(
                    toolCall.function.name,
                    JSON.parse(toolCall.function.arguments || "{}")
                )
                messages.push({
                    role: "tool",
                    tool_call_id: toolCall.id,
                    content: toolResponse,
                });
            }

        }
        else{
            console.log("\n🤖 Agent:", message.content);
            return message.content;
        }
    }
}

runAgent("What is the current year & time?")