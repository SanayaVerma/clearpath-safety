# ClearPath Safety: Presidential AI Challenge Submission

## 1. Community Problem & Impact
Vehicle safety is a critical concern for every community, yet official government recall notices are often written in dense, technical "legalese" that is difficult for the average driver to understand. When a family receives a notice about a "steering column intermediate shaft bolt," they may not realize it means their car could lose steering control while driving. This information gap leads to many vehicles remaining unrepaired, posing a risk to the drivers, their families, and everyone on the road. ClearPath Safety solves this by using AI to translate complex Data.gov recall summaries into clear, actionable advice.

## 2. Technical Implementation & AI Component
The application is built using **Python** and the **Streamlit** framework for a responsive web interface. 
- **Data Source:** It connects to the live **NHTSA (National Highway Traffic Safety Administration) API** from Data.gov to fetch real-time safety records.
- **AI Integration:** I integrated the **OpenAI GPT-4o-mini** model. Rather than just acting as a chatbot, the AI acts as a data-processor. It receives the raw JSON response from the government database and uses a custom system prompt to perform "text-simplification" and "urgency classification." 
- **The AI Logic:** The core of the solution is the prompt engineering that instructs the AI to identify the specific danger (e.g., fire risk vs. cosmetic issue) and provide a concrete next step for the user.

## 3. Challenges & Innovation
One major challenge was handling the volume of data. Some older car models have dozens of recalls. I had to design the UI using "expanders" so the user isn't overwhelmed. Innovation-wise, most recall tools just give you a link to a PDF. ClearPath is unique because it interprets that PDF content in real-time, providing immediate clarity without requiring the user to do extra research.

## 4. Responsible AI & Accuracy
To ensure responsible use, the app includes a clear disclaimer that AI advice is for informational purposes. To verify accuracy, I tested the outputs against known major recalls (like the Takata Airbag recall) to ensure the AI did not downplay high-risk situations. By using a "Grounding" technique—where the AI is strictly limited to summarizing the provided government text—I significantly reduced the risk of AI "hallucinations."

## 5. Reflections & Learning
Building ClearPath Safety deepened my understanding of how APIs work and the importance of "Human-Centric AI." I learned that AI is most powerful when it acts as a bridge between high-level data and everyday people. This project taught me how to manage API keys securely using Streamlit Secrets and how to design a tool that is truly accessible to my community.
