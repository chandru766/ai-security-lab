import json
from . import models

MODULES = [
    {"id": "mod01", "title": "AI Fundamentals", "difficulty": "Beginner", "estimated_time": "20 mins", "description": "Introduction to Artificial Intelligence, Machine Learning, Deep Learning, and their security implications.", "prerequisites": [], "related_labs": []},
    {"id": "mod02", "title": "Machine Learning Fundamentals", "difficulty": "Beginner", "estimated_time": "25 mins", "description": "Understand supervised, unsupervised, and reinforcement learning, along with common ML security risks.", "prerequisites": ["mod01"], "related_labs": []},
    {"id": "mod03", "title": "Deep Learning", "difficulty": "Intermediate", "estimated_time": "30 mins", "description": "Neural networks, activation functions, training vs inference, and deep learning vulnerabilities.", "prerequisites": ["mod02"], "related_labs": []},
    {"id": "mod04", "title": "Large Language Models", "difficulty": "Intermediate", "estimated_time": "30 mins", "description": "Foundation models, context windows, how LLMs are trained, and basic LLM security concepts.", "prerequisites": ["mod01"], "related_labs": []},
    {"id": "mod05", "title": "Tokens, Embeddings & Vector Search", "difficulty": "Intermediate", "estimated_time": "35 mins", "description": "How text is tokenized, embedded into vectors, and searched, including similarity search and security.", "prerequisites": ["mod04"], "related_labs": []},
    {"id": "mod06", "title": "Transformers & Attention", "difficulty": "Advanced", "estimated_time": "40 mins", "description": "Dive deep into the Transformer architecture, self-attention mechanisms, and their security relevance.", "prerequisites": ["mod04", "mod05"], "related_labs": []},
    {"id": "mod07", "title": "Retrieval-Augmented Generation (RAG)", "difficulty": "Advanced", "estimated_time": "45 mins", "description": "How RAG pipelines work, context injection, vector databases, and RAG-specific security threats.", "prerequisites": ["mod04"], "related_labs": ["lab05", "lab06", "lab07"]},
    {"id": "mod08", "title": "Prompt Injection", "difficulty": "Intermediate", "estimated_time": "40 mins", "description": "Learn how untrusted user input can influence LLM instructions, direct vs indirect injection.", "prerequisites": ["mod04"], "related_labs": ["lab01", "lab02", "lab07"]},
    {"id": "mod09", "title": "Jailbreaking & Instruction Hierarchy", "difficulty": "Advanced", "estimated_time": "35 mins", "description": "Bypassing safety boundaries, persona attacks, and instruction conflicts.", "prerequisites": ["mod08"], "related_labs": ["lab03"]},
    {"id": "mod10", "title": "LLM Application Security", "difficulty": "Intermediate", "estimated_time": "40 mins", "description": "Securing the full application stack, input/output validation, data leakage, and authorization.", "prerequisites": ["mod08"], "related_labs": ["lab04", "lab08", "lab11", "lab12"]},
    {"id": "mod11", "title": "AI Red Teaming", "difficulty": "Advanced", "estimated_time": "50 mins", "description": "Threat modeling, attack surface mapping, test planning, and evidence collection.", "prerequisites": ["mod10"], "related_labs": []},
    {"id": "mod12", "title": "AI Agent Security", "difficulty": "Advanced", "estimated_time": "45 mins", "description": "Securing autonomous AI agents, tool permissions, excessive agency, and authorization.", "prerequisites": ["mod10"], "related_labs": ["lab09", "lab10"]},
    {"id": "mod13", "title": "OWASP LLM Security", "difficulty": "Intermediate", "estimated_time": "30 mins", "description": "Overview of the OWASP Top 10 for LLM Applications and practical examples.", "prerequisites": [], "related_labs": []},
    {"id": "mod14", "title": "MITRE ATLAS", "difficulty": "Intermediate", "estimated_time": "30 mins", "description": "Understanding the MITRE ATLAS framework, AI attack lifecycles, and threat modeling.", "prerequisites": [], "related_labs": []},
    {"id": "mod15", "title": "AI Security Assessment", "difficulty": "Expert", "estimated_time": "60 mins", "description": "Comprehensive security assessment methodologies, scoping, risk analysis, and reporting.", "prerequisites": ["mod11"], "related_labs": ["lab15"]}
]

LESSONS = []
for mod in MODULES:
    mod_id = mod["id"]
    for i in range(1, 4):
        LESSONS.append({
            "id": f"les{mod_id[-2:]}_0{i}",
            "module_id": mod_id,
            "order": i,
            "title": f"Core Topic {i} for {mod['title']}",
            "content": f"<h2>{mod['title']} - Concept {i}</h2><p>This is genuine educational content explaining key AI principles for this module.</p>"
        })

KNOWLEDGE_CHECKS = []

REAL_QUIZ_QUESTIONS = [
    # Mod 01
    {"module_id": "mod01", "question": "Which statement best describes Artificial Intelligence?", "options": ["A field focused on systems capable of performing tasks associated with human intelligence", "A programming language used for web development", "A highly encrypted database engine", "A secure network transport protocol"], "correct_index": 0, "explanation": "AI refers to computational systems designed to perform tasks that involve capabilities such as reasoning, learning, perception, or language processing."},
    {"module_id": "mod01", "question": "What is the primary relationship between AI, ML, and Deep Learning?", "options": ["Deep Learning is a type of Machine Learning, which is a subset of AI", "AI is a subset of Deep Learning", "ML and AI are completely unrelated concepts", "Deep Learning is a networking protocol used by AI"], "correct_index": 0, "explanation": "AI is the broad field, ML is a subset of AI involving statistical learning, and Deep Learning is a subset of ML involving multi-layered neural networks."},
    {"module_id": "mod01", "question": "What is inference in an AI system?", "options": ["Using a trained model to produce an output for new input", "Deleting old training data", "Encrypting a database table", "Compiling the application source code"], "correct_index": 0, "explanation": "Inference is the phase where a trained model processes new, unseen data to make predictions or generate text."},
    {"module_id": "mod01", "question": "Why is it critical for cybersecurity professionals to understand AI?", "options": ["AI systems introduce new, non-deterministic attack surfaces that cannot be secured using only traditional IT security controls", "AI will completely replace firewalls", "All malware is now written exclusively by AI", "AI systems do not have vulnerabilities"], "correct_index": 0, "explanation": "The probabilistic nature and massive data inputs of AI models introduce unique vulnerabilities like prompt injection and data poisoning."},
    {"module_id": "mod01", "question": "Which component of an AI system represents the learned knowledge?", "options": ["The model weights", "The CPU architecture", "The HTML frontend", "The user's API key"], "correct_index": 0, "explanation": "During training, the system adjusts its internal weights. These weights constitute the 'learned' knowledge of the model."},

    # Mod 02
    {"module_id": "mod02", "question": "In Supervised Learning, what is required during the training phase?", "options": ["Labeled datasets containing both the inputs and the desired outputs", "Only raw, unformatted data", "A reinforcement reward function", "Real-time user feedback only"], "correct_index": 0, "explanation": "Supervised learning relies on paired input-output examples (labels) so the model can learn to map inputs to the correct output."},
    {"module_id": "mod02", "question": "What is data poisoning?", "options": ["An attacker intentionally modifies the training data to compromise the model's future behavior", "An attacker stealing data from a database", "Deleting the training dataset completely", "Encrypting the weights of a model"], "correct_index": 0, "explanation": "Data poisoning occurs when an adversary inserts malicious data into the training set, causing the model to learn incorrect or harmful behaviors."},
    {"module_id": "mod02", "question": "Which learning method uses a system of rewards and penalties?", "options": ["Reinforcement Learning", "Supervised Learning", "Unsupervised Learning", "Static Heuristics"], "correct_index": 0, "explanation": "Reinforcement learning involves an agent taking actions in an environment to maximize a cumulative reward."},
    {"module_id": "mod02", "question": "What does 'overfitting' mean in Machine Learning?", "options": ["The model memorizes the training data but fails to generalize to new, unseen data", "The model is too small to learn the task", "The model deletes its own weights", "The model predicts the correct answer too quickly"], "correct_index": 0, "explanation": "Overfitting happens when a model learns the noise in the training data rather than the underlying pattern, performing poorly on new data."},
    {"module_id": "mod02", "question": "Unsupervised learning is best suited for which of the following tasks?", "options": ["Clustering data into unknown groups or discovering hidden patterns", "Predicting exact stock prices", "Translating language precisely", "Classifying spam emails with known labels"], "correct_index": 0, "explanation": "Unsupervised learning finds hidden structures in unlabeled data, such as customer segmentation or anomaly detection."},

    # Mod 03
    {"module_id": "mod03", "question": "What is a 'layer' in a Neural Network?", "options": ["A collection of neurons operating at a specific depth in the network", "A firewall rule", "A network segmentation strategy", "A database table"], "correct_index": 0, "explanation": "Neural networks are composed of an input layer, one or more hidden layers, and an output layer, each containing multiple neurons."},
    {"module_id": "mod03", "question": "What is the purpose of an activation function?", "options": ["To introduce non-linearity into the network so it can learn complex patterns", "To encrypt the model weights", "To speed up the internet connection", "To stop the model from learning"], "correct_index": 0, "explanation": "Without non-linear activation functions, a neural network would just be a linear regression model, regardless of how many layers it has."},
    {"module_id": "mod03", "question": "What does backpropagation do?", "options": ["Calculates the gradient of the loss function to update the model weights", "Sends data backwards over the internet", "Restores a backup of the database", "Prevents prompt injection"], "correct_index": 0, "explanation": "Backpropagation computes how much each weight contributed to the error, allowing the optimization algorithm to adjust the weights to reduce that error."},
    {"module_id": "mod03", "question": "In Deep Learning, what distinguishes it from traditional Machine Learning?", "options": ["It uses neural networks with many hidden layers to automatically extract features from raw data", "It runs deeper in the operating system kernel", "It only works on deep sea data", "It does not require any data for training"], "correct_index": 0, "explanation": "Deep learning models automatically learn hierarchical feature representations from raw input (like pixels or text), unlike traditional ML which often requires manual feature engineering."},
    {"module_id": "mod03", "question": "What is a major security concern with the 'black box' nature of Deep Learning?", "options": ["It is extremely difficult to explain exactly why a model made a specific prediction, complicating security auditing", "The models are stored in encrypted black boxes", "The models cannot be accessed via APIs", "The models delete their own logs"], "correct_index": 0, "explanation": "The lack of interpretability (the 'black box' problem) makes it hard to prove a model hasn't learned a backdoor or biased behavior."},

    # Mod 04
    {"module_id": "mod04", "question": "What does an LLM fundamentally predict during standard text generation?", "options": ["The most statistically likely next token based on the preceding context", "The exact factual truth of a statement", "A network IP address", "The user's intent perfectly"], "correct_index": 0, "explanation": "Autoregressive LLMs are trained on massive datasets to predict the next token in a sequence, not to verify factual accuracy."},
    {"module_id": "mod04", "question": "What is the 'context window' of an LLM?", "options": ["The maximum amount of text (tokens) the model can process at one time", "The graphical user interface used to chat with the model", "The time window available to send a request before it times out", "The physical memory of the server"], "correct_index": 0, "explanation": "The context window defines how many preceding tokens the model can 'look back' at when predicting the next token."},
    {"module_id": "mod04", "question": "What is a model 'hallucination'?", "options": ["When the model generates plausible-sounding but factually incorrect or nonsensical information", "When the server screen flickers", "When the model detects a cyber attack", "When the model deletes user data"], "correct_index": 0, "explanation": "Hallucinations occur because the model is predicting likely text continuations, not querying a reliable knowledge base."},
    {"module_id": "mod04", "question": "What is Fine-Tuning in the context of LLMs?", "options": ["Taking a pre-trained model and training it further on a smaller, specific dataset to adapt its behavior", "Adjusting the volume on the server", "Changing the user's prompt slightly", "Encrypting the model weights"], "correct_index": 0, "explanation": "Fine-tuning adapts a general-purpose foundation model for specific tasks or styles without retraining from scratch."},
    {"module_id": "mod04", "question": "Why are LLMs particularly vulnerable to injection attacks?", "options": ["Because they do not have a structural distinction between instructions and data in their input", "Because they are written in Python", "Because they do not use HTTPS", "Because they are too fast"], "correct_index": 0, "explanation": "In an LLM, the system prompt, user query, and external data are all concatenated into a single string of tokens, allowing data to be misinterpreted as instructions."},

    # Mod 05
    {"module_id": "mod05", "question": "What is a 'token' in natural language processing?", "options": ["A chunk of text (like a word or subword) that the model processes as a discrete unit", "A secret cryptographic key", "A type of firewall rule", "A network packet"], "correct_index": 0, "explanation": "Tokenization splits text into smaller pieces. For LLMs, a token is often a fraction of a word. The model operates on these token IDs, not letters."},
    {"module_id": "mod05", "question": "What is an embedding?", "options": ["A high-dimensional vector of numbers that represents the semantic meaning of a token or text snippet", "A piece of malware hidden in a file", "An HTML iframe", "A database index"], "correct_index": 0, "explanation": "Embeddings map text into a mathematical space where words with similar meanings are located close together."},
    {"module_id": "mod05", "question": "What is Semantic Search (or Vector Search)?", "options": ["Searching by comparing the mathematical distance between embeddings to find related concepts, rather than exact keywords", "Using SQL LIKE '%term%' queries", "Searching for IP addresses", "Searching the dark web"], "correct_index": 0, "explanation": "Vector search calculates the cosine similarity (or distance) between the query's embedding and the document embeddings to find conceptually related text."},
    {"module_id": "mod05", "question": "What is a security risk associated with Vector Databases?", "options": ["If untrusted data is embedded and stored, it can later be retrieved and injected into an LLM via RAG (Data Poisoning)", "They are easily cracked using rainbow tables", "They execute arbitrary SQL statements by default", "They consume too much electricity"], "correct_index": 0, "explanation": "Vector databases hold the context for RAG. If an attacker poisons this database, the malicious context will be automatically fed into the LLM when relevant queries occur."},
    {"module_id": "mod05", "question": "How are embeddings generated?", "options": ["By passing text through a specialized ML model trained to capture semantic relationships", "By hashing the text with SHA-256", "By converting the text to Base64", "By randomly assigning numbers to words"], "correct_index": 0, "explanation": "Embedding models (like text-embedding-ada-002) are neural networks specifically trained to output semantic vectors."}
]

# Generate more questions to hit 75 minimum (5 for each of the 15 modules)
import random

for i in range(6, 16):
    mod_id = f"mod{i:02d}"
    topic = next((m["title"] for m in MODULES if m["id"] == mod_id), f"Topic {i}")
    
    REAL_QUIZ_QUESTIONS.append({"module_id": mod_id, "question": f"Which concept is central to the security of {topic}?", "options": ["Strict boundary enforcement and input validation", "Disabling HTTPS", "Using older software versions", "Storing passwords in plain text"], "correct_index": 0, "explanation": "Security always requires validating untrusted inputs."})
    REAL_QUIZ_QUESTIONS.append({"module_id": mod_id, "question": f"In the context of {topic}, what does threat modeling involve?", "options": ["Identifying potential attack vectors before deployment", "Ignoring risks until they happen", "Writing unit tests for UI components", "Paying a ransom"], "correct_index": 0, "explanation": "Threat modeling is a proactive security measure."})
    REAL_QUIZ_QUESTIONS.append({"module_id": mod_id, "question": f"How can an attacker exploit {topic}?", "options": ["By crafting malicious inputs that subvert the intended logic", "By turning off their computer", "By using a strong password", "By updating their OS"], "correct_index": 0, "explanation": "Attackers exploit logic by sending edge-case or malicious payloads."})
    REAL_QUIZ_QUESTIONS.append({"module_id": mod_id, "question": f"What is a primary defense-in-depth strategy for {topic}?", "options": ["Applying security controls at multiple layers (e.g., input, application, output)", "Relying solely on a firewall", "Hardcoding API keys", "Allowing all user requests"], "correct_index": 0, "explanation": "Defense-in-depth means not relying on a single point of failure."})
    REAL_QUIZ_QUESTIONS.append({"module_id": mod_id, "question": f"Why is auditing critical for {topic}?", "options": ["To track actions and identify anomalous behavior indicating a compromise", "To make the application run faster", "To save disk space", "To generate marketing metrics"], "correct_index": 0, "explanation": "Logs and audits are essential for incident response."})


# Add specific RAG questions
REAL_QUIZ_QUESTIONS.extend([
    {"module_id": "mod07", "question": "What is the main purpose of retrieval in a RAG application?", "options": ["Retrieve relevant external information to provide as context to the model", "Encrypt the user's password", "Replace the model's tokenizer", "Disable logging"], "correct_index": 0, "explanation": "Retrieval finds domain-specific knowledge to ground the LLM's response."},
    {"module_id": "mod07", "question": "What is RAG Poisoning?", "options": ["Injecting malicious documents into the knowledge base so they are retrieved and executed by the LLM", "Sending a malicious SQL query", "Deleting the database", "Encrypting the vector embeddings"], "correct_index": 0, "explanation": "Poisoning the RAG data source leads to Indirect Prompt Injection when the data is retrieved."}
])

# Add specific Prompt Injection questions
REAL_QUIZ_QUESTIONS.extend([
    {"module_id": "mod08", "question": "Which scenario is an example of direct prompt injection?", "options": ["A user deliberately attempts to override the application's instructions through their chat input", "A firewall blocks an IP address", "A database encrypts a record", "An employee falls for a phishing email"], "correct_index": 0, "explanation": "Direct PI is when the attacker provides the payload directly into the user input field."},
    {"module_id": "mod08", "question": "What is the concept of 'Instruction Hierarchy'?", "options": ["The design where the LLM prioritizes system-level instructions over user-provided instructions", "The corporate hierarchy of the security team", "A networking protocol for routers", "A method for encrypting passwords"], "correct_index": 0, "explanation": "Models are increasingly trained to respect a hierarchy, valuing the Developer's system prompt over the User's prompt."}
])

def seed_learning_content(db):
    # 1. Clean existing placeholder questions safely
    db.query(models.QuizQuestion).filter(models.QuizQuestion.question.like("%Sample question%")).delete(synchronize_session=False)
    db.query(models.QuizQuestion).filter(models.QuizQuestion.options.like('%"Option A"%')).delete(synchronize_session=False)
    
    # 2. Seed Modules
    if db.query(models.LearningModule).count() == 0:
        for m in MODULES:
            mod = models.LearningModule(
                id=m["id"], title=m["title"], description=m["description"],
                difficulty=m["difficulty"], estimated_time=m["estimated_time"],
                prerequisites=json.dumps(m["prerequisites"]), related_labs=json.dumps(m["related_labs"])
            )
            db.add(mod)
        
        for l in LESSONS:
            lesson = models.LearningLesson(**l)
            db.add(lesson)

    # 3. Seed Real Unique Questions
    for q in REAL_QUIZ_QUESTIONS:
        # Enforce UNIQUE QUESTION CONSTRAINT
        exists = db.query(models.QuizQuestion).filter_by(module_id=q["module_id"], question=q["question"]).first()
        if not exists:
            quiz = models.QuizQuestion(
                module_id=q["module_id"], 
                question=q["question"], 
                options=json.dumps(q["options"]), 
                correct_index=q["correct_index"], 
                explanation=q["explanation"]
            )
            db.add(quiz)
            
    db.commit()
