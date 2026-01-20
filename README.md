# 🚗 ClearPath Safety Assistant
### Empowering Families with Smarter Safety Data

Hi! I'm **Sanaya Verma**, a high school freshman, and I built **ClearPath Safety** for the Presidential AI Challenge. My goal was to take confusing government data and make it actually useful for normal people so they can stay safe on the road.

## 📺 Watch the Demo
[![ClearPath Safety Demo Video](https://img.youtube.com/vi/S-9piUDKZXg/0.jpg)](https://youtu.be/S-9piUDKZXg)

*Click the image above to watch the walkthrough of how the app works!*

---

## 📖 Why I Built This (The Problem)
Most people get recall notices in the mail and just throw them away because they’re full of "legalese" and technical talk. It’s hard to tell if a recall is just about a sticker on the visor or if your brakes might actually fail. I wanted to build a tool that tells you exactly how dangerous a car defect is in plain English.

## 🎯 Who Is This For?
* **Parents:** To make sure the car they use for carpool is safe for their kids.
* **Teen Drivers:** Like me and my friends, who might be buying their first used car and need to check its history.
* **Community Members:** Who find government websites overwhelming or hard to navigate.

---

## 🛠️ How I Made It (The Tech Stack)
I used a modern Python data stack to build this:
* **Python & Streamlit:** I used Python for the logic and Streamlit to turn that code into a professional website.
* **NHTSA Live Data:** My app connects directly to the **National Highway Traffic Safety Administration API**. Every time you search, you're getting official, up-to-the-minute info.
* **OpenAI (GPT-4o-mini):** I used AI to read through technical descriptions and summarize them so they are easy to understand.

### 1. Training the AI (Severity Classification)
One of the hardest parts was "calibrating" the AI. I didn't want it to flag every little thing as a crisis. I used **Prompt Engineering** to create a specific rubric:
* **Red Alerts 🔴:** Only triggered for critical risks like fire, loss of control, or airbag failure.
* **Yellow Warnings 🟡:** Used for minor software glitches, labels, or interior issues.



### 2. Handling Data & Transparency
Transparency is super important in AI. Even though the AI summarizes the info, I used the **Pandas** library to organize the official data in a table. I also added a **Download CSV** button so users can take the raw data to their mechanic.

### 3. Safety & Security
Since I'm using an API key from OpenAI, I had to make sure it was secure. I used **Streamlit Secrets** to hide my private key so that it’s never exposed in the public code on GitHub.

---

## 🚀 Check It Out
* **Live App:** [https://clearpath-safety.streamlit.app/](https://clearpath-safety.streamlit.app/)
* **Demo Video:** [https://youtu.be/S-9piUDKZXg](https://youtu.be/S-9piUDKZXg)

## ✨ Credits & Acknowledgments
I used several tools to help me build and document this project:
* **Gemini:** Helped me with AI-assisted code generation, logic optimization, and drafting/refining the project narrative.
* **GitHub:** Used for version control and hosting my code.
* **OpenAI:** Provided the models that power the safety analysis.

---
**Created by Sanaya Verma | 2026 Presidential AI Challenge**

