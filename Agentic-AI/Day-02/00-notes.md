## Types of Agents

### **1. Simple Reflex Agent**
* **Nature:** The most basic type of agent that acts purely on the **current situation**.
* **Mechanism:** It follows **"If-Then" rules** (Condition-Action rules). It does not have a memory of past events or the ability to plan for the future.
* **Example:**
    * **Automatic Doors:** If the sensor detects someone nearby, the door opens. 
    * **Motion Sensor Lights:** If movement is detected, the light turns on.

### **2. Model-Based Reflex Agent**
* **Nature:** A smarter version of the Simple Reflex Agent that can handle partially observable environments.
* **Mechanism:** It maintains an internal **memory** (Model of the World) to keep track of past information or things it can't see right now.
* **Example:**
    * **Name Recall:** If you tell the agent your name earlier in a conversation, it remembers it. A Simple Reflex agent would forget your name as soon as the specific interaction ends, while a Model-Based agent uses its memory to answer "What is my name?"

### **3. Goal-Based Agent**
* **Nature:** These agents don't just react; they **plan** to achieve a specific target.
* **Mechanism:** They take actions that move them closer to a defined **Goal**. They are flexible and can "re-plan" if the environment changes.
* **Example:**
    * **GPS Navigation:** The goal is to reach a destination. The agent checks traffic and roads to find the best route. If a road is closed, it recalculates a new path to still meet the goal.
    * **Flight Booking Assistant:** Given a goal to find a flight under $500, it compares various options to find the one that meets the criteria.

### **4. Utility-Based Agent**
* **Nature:** An upgrade to Goal-Based agents that focuses on **how well** a goal is achieved, not just reaching it.
* **Mechanism:** Every possible action is assigned a **Utility Score**. The agent chooses the action with the highest score to find the "best" or "happiest" path.
* **Example:**
    * **Self-Driving Cars:** While multiple routes might reach the destination (the goal), the agent evaluates which is the safest, fastest, or most fuel-efficient by assigning scores to each.
    * **Chess Bots:** The agent evaluates multiple possible moves and chooses the one with the highest probability of winning.

### **5. Learning Agent**
* **Nature:** These agents improve over time by learning from their **experiences** and feedback.
* **Mechanism:** Based on **Reinforcement Learning**, they perform an action, receive a "Reward" for good performance or a "Penalty" for mistakes, and adjust their future behavior accordingly.
* **Example:**
    * **Game Bots:** A bot might play a game thousands of times. Initially, it plays poorly, but by learning which moves lead to winning (rewards) and which lead to losing (penalties), it eventually becomes an expert.

**Key Differences Summary**
* **Simple Reflex:** Purely reactive, no memory.
* **Model-Based:** Reactive but includes memory.
* **Goal-Based:** Proactive, works toward a specific target.
* **Utility-Based:** Optimizes for the *best* possible outcome using scores.
* **Learning:** Continuously improves through trial and error.
