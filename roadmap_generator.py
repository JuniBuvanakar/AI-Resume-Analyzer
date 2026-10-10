ROADMAP = {
    "Python": ("Python fundamentals", "Practice functions, collections, file handling and a small automation script."),
    "SQL": ("SQL querying", "Practice SELECT, JOIN, GROUP BY, subqueries and aggregations on a sample database."),
    "Excel": ("Spreadsheet analysis", "Practice formulas, lookup functions, pivot tables and data cleaning."),
    "Pandas": ("Data analysis with Pandas", "Load a CSV, clean missing values, group data and produce a short summary."),
    "Power BI": ("Power BI dashboards", "Build a small dashboard with measures, slicers and clear visualizations."),
    "Machine Learning": ("Machine-learning foundations", "Study train/test splits, evaluation metrics and a simple scikit-learn model."),
    "scikit-learn": ("scikit-learn workflow", "Train and evaluate a small baseline model using a public or synthetic dataset."),
    "FastAPI": ("FastAPI basics", "Create and test an endpoint that accepts input and returns a prediction or JSON response."),
    "Docker": ("Docker fundamentals", "Containerize a small Python application and document how to run it."),
    "Deep Learning": ("Deep-learning foundations", "Learn neural-network basics and train a small tutorial model."),
    "LLM": ("Large language model basics", "Study tokens, prompting, limitations and responsible evaluation."),
    "RAG": ("Retrieval-augmented generation", "Build a tiny document retrieval demo and inspect whether retrieved passages support answers."),
    "APIs": ("API fundamentals", "Practice HTTP methods, JSON, status codes and calling a public test API."),
    "NLP": ("Natural language processing", "Explore tokenization, text normalization and a simple text classification task."),
    "Transformers": ("Transformer fundamentals", "Learn attention and compare a pretrained text model on example inputs."),
    "Hugging Face": ("Hugging Face workflow", "Load a pretrained model or dataset and run a small inference example."),
    "OpenCV": ("Computer vision with OpenCV", "Load an image, resize it, convert color spaces and detect basic image features."),
    "CNN": ("Convolutional neural networks", "Study convolution and pooling, then run a small image-classification tutorial."),
    "YOLO": ("Object detection with YOLO", "Run a permitted pretrained object detector on sample images and inspect predictions."),
    "C++": ("C++ programming", "Practice functions, classes, STL containers and problem-solving exercises."),
    "Java": ("Java programming", "Practice classes, collections, exception handling and a small console application."),
    "JavaScript": ("JavaScript fundamentals", "Build a small interactive page and practice arrays, objects and asynchronous requests."),
    "HTML": ("HTML foundations", "Create a semantic page with headings, forms, links and accessible labels."),
    "CSS": ("CSS layout", "Build a responsive page using Flexbox or Grid."),
    "Git": ("Git version control", "Practice commits, branches, merges and a clear project history."),
    "Linux": ("Linux command line", "Practice navigation, file operations, permissions and basic shell commands."),
    "AWS": ("Cloud fundamentals", "Study core cloud concepts and deploy a small non-sensitive demo if permitted."),
    "Azure": ("Cloud fundamentals", "Study core cloud concepts and explore a small non-sensitive deployment tutorial."),
    "PostgreSQL": ("Relational database practice", "Design a small schema, add constraints and write joins and aggregations."),
    "MongoDB": ("Document database basics", "Create a small collection and practice document queries and updates."),
    "Tableau": ("Data visualization", "Build a small dashboard and explain the chart choice for each question."),
}

def generate_roadmap(missing_skills: list[str]) -> list[dict]:
    plan = []
    for i, skill in enumerate(missing_skills, start=1):
        title, activity = ROADMAP.get(skill, (f"Learn {skill}", f"Study the fundamentals of {skill} and complete a small hands-on exercise."))
        plan.append({"Priority": i, "Skill to learn": skill, "Topic": title, "Suggested activity": activity})
    return plan
