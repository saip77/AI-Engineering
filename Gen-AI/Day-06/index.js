import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";
import { OpenAIEmbeddings, ChatOpenAI } from "@langchain/openai";
import { PineconeStore } from "@langchain/pinecone";
import { Pinecone as PineconeClient } from "@pinecone-database/pinecone";
import dotenv from "dotenv";
import * as readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

dotenv.config();

async function main() {
  const rl = readline.createInterface({ input, output });

  try {
    console.log("🚀 Initializing RAG System...");

    const loader = new PDFLoader("./French-Revolution.pdf");
    const docs = await loader.load();
    
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: 1000,
      chunkOverlap: 200,
    });
    const splitDocs = await splitter.splitDocuments(docs);
    const validDocs = splitDocs.filter(doc => doc.pageContent?.trim().length > 0);

    const embeddings = new OpenAIEmbeddings({
      model: "text-embedding-3-small",
    });

    const pinecone = new PineconeClient({ apiKey: process.env.PINECONE_API_KEY });
    const pineconeIndex = pinecone.Index(process.env.PINECONE_INDEX);

    console.log("📦 Indexing documents to Pinecone...");
    const vectorStore = await PineconeStore.fromDocuments(validDocs, embeddings, { pineconeIndex });
    
    const retriever = vectorStore.asRetriever({ k: 3 });
    const model = new ChatOpenAI({ model: "gpt-4o-mini", temperature: 0 });

    console.log("\n✅ Ready! Type your question below (or type 'exit' to quit).");

    while (true) {
      const question = await rl.question("\n👤 You: ");

      if (question.toLowerCase() === "exit" || question.toLowerCase() === "quit") {
        console.log("👋 Goodbye!");
        break;
      }

      if (!question.trim()) continue;

      process.stdout.write("🤖 Thinking...");
      const retrievedDocs = await retriever.invoke(question);
      const context = retrievedDocs.map(doc => doc.pageContent).join("\n\n");
      const response = await model.invoke(`
        Answer the question using ONLY the context below. 
        If the answer isn't in the context, say "I don't have enough information on that."

        Context:
        ${context}

        Question:
        ${question}
      `);
      process.stdout.clearLine(0);
      process.stdout.cursorTo(0);
      console.log(`🤖 AI: ${response.content}`);
    }

  } catch (error) {
    console.error("\n❌ Error:", error.message);
  } finally {
    rl.close();
  }
}

main();