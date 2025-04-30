## LLM Usage Record

### Backend

  **Prompt:**  
  ```
  I have this new sqlalchemy implementation. Do you remember my todo tutorial app? How can I use this instead?
  [(Tanner's SQLAlchemy code made from a tutorial)]
  ```
- **Reflection:**  
  I used the FastAPI + SQLAlchemy boilerplate ChatGPT generated—`database.py`, `models.py`, `schemas.py`, `crud.py`, and `main.py`—almost without change. I don’t fully understand every line yet, but it’s working and is basic enough I think it's unlikely ChatGPT will get it wrong.

---

### Frontend

  **Prompt:**  
  ```
  How can I change this to enter an activity name and an amount of money instead, with the result being displayed in a table rendered into the webpage? I want to convert this tutorial todo app to a financial advisor app, and tracking finance is the first step.
  ```
- **Reflection:**  
  I updated `TodoComponent.vue` with two inputs (`name` and `amount`), updated the fetch URLs and methods, and rendered a `<table>`. This is further works on server-database connections that I had no clues about, and I'm keeping what ChatGPT did.

---

### Full-Stack

1. **Convert to SQLAlchemy + FastAPI**  
    **Prompt:**  
    ```
    Both please  (help wiring SQLAlchemy backend and updated Vue frontend)
    ```  
   - **Reflection:**  
   I asked for help in wiring SQLAlchemy backend and updated Vue frontend. By the time I finished that commit, I had a working “activity + amount” CRUD cycle. The example made clear where to modify both the API model and the Vue template, and now I could add further fields myself.

2. **Docker setup**  
   - **Prompt:**  
     ```
     If I make a Docker image to run using my working version, can he run it on his computer? If so, please help me make the Docker setup. ['he' refers to Tanner who has trouble running npm in how device and lab computers.]
     ```  
   - **Reflection:**  
     I used the Dockerfiles and `docker-compose.yml` ChatGPT provided verbatim to make the Docker-related files. It works fine on my computer, but my teammate have trouble with opening Docker and the lab computers needed admin access to download Docker so we couldn't verify if it's working.

3. **Writing the development.md guide**  
   - **Prompt:**  
     ```
     Please help me write up the development.md [(Following a prompt where I passed the assignment texts and ask it to help me clarify the difference between development.md and running.md)]
     ```  
   - **Reflection:**  
     I used ChatGPT to help me recall the steps I took to get this project to work, as they were done by ChatGPT already. I adopted the full “Development Guide” draft with only minor edits. It clearly lays out the Python venv steps, `npm run dev`, Docker-based dev, testing, and Git workflow.

4. **Filling LLM.md**  
   - **Prompt:**  
     ```
     With my current work as a template, can you help me fill in how you have helped me with this project so far? You can edit my already written sections if needed to make the result better. [(I also passed in my mostly finished self-written LLM.md)]
     ```  
   - **Reflection:**  
     I had ChatGPT provide a summary of what I have used it for, and then I edited the wordings to make it more clear based on my understanding, as well as fixing some mistakes such as topic heading vs content. It helped me recall several things I forgot I used it for.

---


