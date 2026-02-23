roadmaps = {

    "SOC Analyst": [
        "Learn Networking fundamentals (OSI, TCP/IP, ports, protocols)",
        "Master Linux basic commands and file system",
        "Understand logs and event analysis",
        "Learn SIEM tools (Splunk, ELK)",
        "Study Incident Response lifecycle",
        "Practice with TryHackMe SOC labs",
        "Understand IDS/IPS and firewall rules",
        "Prepare for Security+ certification"
    ],

    "Data Scientist": [
        "Learn Python programming",
        "Study NumPy and Pandas",
        "Data visualization using Matplotlib/Seaborn",
        "Statistics and probability basics",
        "Machine Learning using Scikit-learn",
        "Work on datasets and projects",
        "Learn SQL and data handling",
        "Build ML projects portfolio"
    ],

    "Web Developer": [
        "HTML and CSS fundamentals",
        "JavaScript basics",
        "DOM manipulation",
        "Frontend framework (React)",
        "Backend basics (Node/Flask)",
        "Database integration",
        "Build full stack projects",
        "Deploy website"
    ]
}


def generate_roadmap(role, missing_skills):
    steps = roadmaps.get(role, [])

    personalized = []

    for skill in missing_skills:
        personalized.append(f"Focus on learning: {skill}")

    return personalized + steps

