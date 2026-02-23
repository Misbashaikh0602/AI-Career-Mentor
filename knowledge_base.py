from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

knowledge = [
"SIEM collects and analyzes security logs from multiple systems.",
"Incident response is the process of handling a cybersecurity breach.",
"Firewalls filter incoming and outgoing network traffic.",
"IDS detects attacks while IPS prevents attacks.",
"Linux is important for cybersecurity because most servers run on Linux.",
"TCP/IP is the communication protocol used in networks.",
"SOC Analyst monitors alerts and investigates threats.",
"To become job ready you need strong practical lab experience.",
"Improve resume by adding projects and certifications.",
"Splunk is widely used SIEM tool in companies.",
"Wireshark is used for packet analysis.",
"TryHackMe and HackTheBox are best platforms for practice."
]

embeddings = model.encode(knowledge)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

def semantic_search(query):
    q_embed = model.encode([query])
    D, I = index.search(np.array(q_embed), k=2)
    answers = [knowledge[i] for i in I[0]]
    return " ".join(answers)

