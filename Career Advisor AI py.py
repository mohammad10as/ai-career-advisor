import math
import re
from collections import Counter
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

JOB_ROLES = [
    {
        "title": "Data Scientist",
        "skills": ["python", "machine learning", "sql", "statistics", "data analysis",
                   "tensorflow", "pandas", "numpy", "deep learning", "visualization"],
        "learning": {
            "python": "https://www.learnpython.org",
            "machine learning": "https://www.coursera.org/learn/machine-learning",
            "sql": "https://www.w3schools.com/sql/",
            "statistics": "https://www.khanacademy.org/math/statistics-probability",
            "tensorflow": "https://www.tensorflow.org/learn",
            "pandas": "https://pandas.pydata.org/docs/getting_started/index.html",
            "numpy": "https://numpy.org/learn/",
            "deep learning": "https://www.deeplearning.ai",
            "visualization": "https://www.tableau.com/learn/training",
            "data analysis": "https://www.kaggle.com/learn/pandas"
        }
    },
    {
        "title": "DevOps Engineer",
        "skills": ["aws", "docker", "kubernetes", "ci/cd", "linux", "git",
                   "automation", "cloud", "terraform", "monitoring"],
        "learning": {
            "aws": "https://aws.amazon.com/training/",
            "docker": "https://docs.docker.com/get-started/",
            "kubernetes": "https://kubernetes.io/docs/tutorials/",
            "ci/cd": "https://www.atlassian.com/continuous-delivery",
            "linux": "https://linuxjourney.com",
            "git": "https://git-scm.com/doc",
            "terraform": "https://developer.hashicorp.com/terraform/tutorials",
            "monitoring": "https://prometheus.io/docs/introduction/overview/",
            "automation": "https://www.ansible.com/resources/get-started",
            "cloud": "https://cloud.google.com/training"
        }
    },
    {
        "title": "Backend Developer",
        "skills": ["python", "java", "sql", "apis", "rest", "databases",
                   "node", "django", "flask", "microservices"],
        "learning": {
            "python": "https://www.learnpython.org",
            "java": "https://dev.java/learn/",
            "sql": "https://www.w3schools.com/sql/",
            "apis": "https://restfulapi.net",
            "rest": "https://restfulapi.net",
            "django": "https://docs.djangoproject.com/en/stable/intro/tutorial01/",
            "flask": "https://flask.palletsprojects.com/en/stable/tutorial/",
            "databases": "https://www.postgresql.org/docs/",
            "node": "https://nodejs.org/en/learn",
            "microservices": "https://microservices.io"
        }
    },
    {
        "title": "Frontend Developer",
        "skills": ["javascript", "html", "css", "react", "vue",
                   "typescript", "ui", "ux", "responsive design", "web"],
        "learning": {
            "javascript": "https://javascript.info",
            "html": "https://www.w3schools.com/html/",
            "css": "https://www.w3schools.com/css/",
            "react": "https://react.dev/learn",
            "vue": "https://vuejs.org/guide/introduction",
            "typescript": "https://www.typescriptlang.org/docs/",
            "ui": "https://www.nngroup.com/articles/",
            "ux": "https://www.interaction-design.org/literature",
            "responsive design": "https://web.dev/learn/design/",
            "web": "https://developer.mozilla.org/en-US/docs/Learn"
        }
    },
    {
        "title": "Machine Learning Engineer",
        "skills": ["python", "machine learning", "deep learning", "tensorflow",
                   "pytorch", "mlops", "docker", "cloud", "algorithms", "optimization"],
        "learning": {
            "python": "https://www.learnpython.org",
            "machine learning": "https://www.coursera.org/learn/machine-learning",
            "deep learning": "https://www.deeplearning.ai",
            "tensorflow": "https://www.tensorflow.org/learn",
            "pytorch": "https://pytorch.org/tutorials/",
            "mlops": "https://ml-ops.org",
            "docker": "https://docs.docker.com/get-started/",
            "cloud": "https://cloud.google.com/training",
            "algorithms": "https://www.khanacademy.org/computing/computer-science/algorithms",
            "optimization": "https://www.coursera.org/learn/deep-neural-network"
        }
    },
    {
        "title": "Cloud Architect",
        "skills": ["aws", "azure", "cloud", "automation", "terraform",
                   "kubernetes", "security", "networking", "docker", "devops"],
        "learning": {
            "aws": "https://aws.amazon.com/training/",
            "azure": "https://learn.microsoft.com/en-us/training/azure/",
            "cloud": "https://cloud.google.com/training",
            "terraform": "https://developer.hashicorp.com/terraform/tutorials",
            "kubernetes": "https://kubernetes.io/docs/tutorials/",
            "security": "https://www.cybrary.it",
            "networking": "https://www.cisco.com/c/en/us/training-events/training-certifications.html",
            "docker": "https://docs.docker.com/get-started/",
            "devops": "https://www.atlassian.com/devops",
            "automation": "https://www.ansible.com/resources/get-started"
        }
    },
    {
        "title": "Cybersecurity Analyst",
        "skills": ["security", "networking", "linux", "penetration testing",
                   "firewalls", "encryption", "monitoring", "incident response", "python", "risk analysis"],
        "learning": {
            "security": "https://www.cybrary.it",
            "networking": "https://www.cisco.com/c/en/us/training-events/training-certifications.html",
            "linux": "https://linuxjourney.com",
            "penetration testing": "https://www.offensive-security.com/metasploit-unleashed/",
            "firewalls": "https://www.paloaltonetworks.com/cyberpedia/what-is-a-firewall",
            "encryption": "https://www.coursera.org/learn/crypto",
            "monitoring": "https://prometheus.io/docs/introduction/overview/",
            "incident response": "https://www.sans.org/white-papers/incident-handlers-handbook/",
            "python": "https://www.learnpython.org",
            "risk analysis": "https://www.isaca.org/resources/risk-it-framework"
        }
    },
    {
        "title": "Full Stack Developer",
        "skills": ["javascript", "python", "react", "node", "sql",
                   "html", "css", "apis", "databases", "git"],
        "learning": {
            "javascript": "https://javascript.info",
            "python": "https://www.learnpython.org",
            "react": "https://react.dev/learn",
            "node": "https://nodejs.org/en/learn",
            "sql": "https://www.w3schools.com/sql/",
            "html": "https://www.w3schools.com/html/",
            "css": "https://www.w3schools.com/css/",
            "apis": "https://restfulapi.net",
            "databases": "https://www.postgresql.org/docs/",
            "git": "https://git-scm.com/doc"
        }
    },
    {
        "title": "Data Engineer",
        "skills": ["python", "sql", "spark", "hadoop", "etl",
                   "data pipelines", "cloud", "aws", "databases", "kafka"],
        "learning": {
            "python": "https://www.learnpython.org",
            "sql": "https://www.w3schools.com/sql/",
            "spark": "https://spark.apache.org/docs/latest/",
            "hadoop": "https://hadoop.apache.org/docs/stable/",
            "etl": "https://www.talend.com/resources/what-is-etl/",
            "data pipelines": "https://www.datacamp.com/courses/building-data-engineering-pipelines-in-python",
            "cloud": "https://cloud.google.com/training",
            "aws": "https://aws.amazon.com/training/",
            "databases": "https://www.postgresql.org/docs/",
            "kafka": "https://kafka.apache.org/documentation/"
        }
    },
    {
        "title": "AI Research Scientist",
        "skills": ["python", "deep learning", "machine learning", "mathematics",
                   "statistics", "pytorch", "tensorflow", "algorithms", "research", "optimization"],
        "learning": {
            "python": "https://www.learnpython.org",
            "deep learning": "https://www.deeplearning.ai",
            "machine learning": "https://www.coursera.org/learn/machine-learning",
            "mathematics": "https://www.khanacademy.org/math",
            "statistics": "https://www.khanacademy.org/math/statistics-probability",
            "pytorch": "https://pytorch.org/tutorials/",
            "tensorflow": "https://www.tensorflow.org/learn",
            "algorithms": "https://www.khanacademy.org/computing/computer-science/algorithms",
            "research": "https://arxiv.org",
            "optimization": "https://www.coursera.org/learn/deep-neural-network"
        }
    },
    {
        "title": "Mobile Developer",
        "skills": ["java", "kotlin", "swift", "react native", "flutter",
                   "mobile", "ui", "apis", "databases", "git"],
        "learning": {
            "java": "https://dev.java/learn/",
            "kotlin": "https://kotlinlang.org/docs/getting-started.html",
            "swift": "https://www.swift.org/getting-started/",
            "react native": "https://reactnative.dev/docs/getting-started",
            "flutter": "https://flutter.dev/docs/get-started/install",
            "mobile": "https://developer.android.com/guide",
            "ui": "https://www.nngroup.com/articles/",
            "apis": "https://restfulapi.net",
            "databases": "https://www.postgresql.org/docs/",
            "git": "https://git-scm.com/doc"
        }
    },
    {
        "title": "Systems Administrator",
        "skills": ["linux", "windows", "networking", "automation", "scripting",
                   "monitoring", "security", "cloud", "virtualization", "troubleshooting"],
        "learning": {
            "linux": "https://linuxjourney.com",
            "windows": "https://learn.microsoft.com/en-us/windows-server/",
            "networking": "https://www.cisco.com/c/en/us/training-events/training-certifications.html",
            "automation": "https://www.ansible.com/resources/get-started",
            "scripting": "https://www.learnpython.org",
            "monitoring": "https://prometheus.io/docs/introduction/overview/",
            "security": "https://www.cybrary.it",
            "cloud": "https://cloud.google.com/training",
            "virtualization": "https://www.vmware.com/topics/glossary/content/virtualization.html",
            "troubleshooting": "https://www.comptia.org/certifications/a"
        }
    },
]

ALL_KNOWN_SKILLS = sorted(set(skill for role in JOB_ROLES for skill in role["skills"]))

def extract_skills_from_text(text):
    text = text.lower()
    found = []
    for skill in ALL_KNOWN_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.append(skill)
    return found

def compute_tf(skill_list):
    total = len(skill_list)
    counts = Counter(skill_list)
    return {term: count / total for term, count in counts.items()}

def compute_idf(all_documents):
    total_docs = len(all_documents)
    term_doc_count = {}
    for doc in all_documents:
        for term in set(doc):
            term_doc_count[term] = term_doc_count.get(term, 0) + 1
    return {term: math.log(total_docs / count) for term, count in term_doc_count.items()}

def compute_tfidf_vector(skill_list, idf, vocabulary):
    tf = compute_tf(skill_list)
    return [tf.get(term, 0) * idf.get(term, 0) for term in vocabulary]

def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a**2 for a in vec_a))
    mag_b = math.sqrt(sum(b**2 for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def build_recommender():
    all_skill_lists = [role["skills"] for role in JOB_ROLES]
    vocabulary = sorted(set(s for skills in all_skill_lists for s in skills))
    idf = compute_idf(all_skill_lists)
    role_vectors = [compute_tfidf_vector(role["skills"], idf, vocabulary) for role in JOB_ROLES]
    return vocabulary, idf, role_vectors

def knn_classify(user_skills, k=3):
    distances = []
    for role in JOB_ROLES:
        role_set = set(role["skills"])
        user_set = set(user_skills)
        intersection = len(user_set & role_set)
        union = len(user_set | role_set)
        jaccard = intersection / union if union > 0 else 0
        distances.append((role["title"], jaccard))
    distances.sort(key=lambda x: x[1], reverse=True)
    return distances[:k]

def recommend(manual_skills, job_description="", top_n=3):
  
    extracted = extract_skills_from_text(job_description) if job_description else []
    all_skills = list(set([s.strip().lower() for s in manual_skills] + extracted))

    if len(all_skills) < 2:
        return {"error": "Please provide at least 2 skills or a job description."}

    vocabulary, idf, role_vectors = build_recommender()
    user_vector = compute_tfidf_vector(all_skills, idf, vocabulary)

    if all(v == 0 for v in user_vector):
        return {"error": "No matching skills found. Try: Python, AWS, Docker, SQL, React, Machine Learning..."}

    scored_roles = []
    for i, role in enumerate(JOB_ROLES):
        score = cosine_similarity(user_vector, role_vectors[i])
        missing = [s for s in role["skills"] if s not in all_skills]
        scored_roles.append({
            "title": role["title"],
            "score": round(score, 4),
            "match_percent": round(score * 100, 1),
            "matched_skills": [s for s in role["skills"] if s in all_skills],
            "missing_skills": missing,
            "learning": {s: role["learning"].get(s, "#") for s in missing[:5]}
        })

    scored_roles.sort(key=lambda x: x["score"], reverse=True)

    knn_results = knn_classify(all_skills, k=3)

    return {
        "user_skills": all_skills,
        "extracted_from_jd": extracted,
        "recommendations": scored_roles[:top_n],
        "knn_classification": [{"title": t, "similarity": round(s, 3)} for t, s in knn_results],
        "total_roles_evaluated": len(JOB_ROLES)
    }

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/recommend", methods=["POST"])
def get_recommendations():
    data = request.get_json()
    manual_skills = data.get("skills", [])
    job_description = data.get("job_description", "")
    top_n = data.get("top_n", 3)
    result = recommend(manual_skills, job_description, top_n)
    return jsonify(result)

@app.route("/skills-list", methods=["GET"])
def skills_list():
    return jsonify(ALL_KNOWN_SKILLS)

if __name__ == "__main__":
    print("\n🚀 Career Advisor is running!")
    print("📡 Open http://localhost:5000 in your browser\n")
    app.run(debug=True, port=5000)
