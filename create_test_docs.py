import fitz  # PyMuPDF
import os

docs = {
    "QuantumLeap_History.pdf": """QuantumLeap Innovations: Company History & Founders

QuantumLeap Innovations was founded in 2018 by Dr. Elara Vance and former aerospace engineer Marcus Sterling. The company started in a small garage in Austin, Texas, with a vision to revolutionize computing and human-machine interfaces. 

Dr. Vance, a prodigy in quantum mechanics, previously worked at the National Quantum Laboratory. Sterling brought his expertise in scalable manufacturing from his time at Orbit Dynamics. 

In 2020, the company moved to its current headquarters in Silicon Valley after securing a massive Series A funding round led by Horizon Ventures. Their mission statement is "Bridging the gap between human thought and infinite computation."
""",
    
    "QuantumLeap_Products.pdf": """QuantumLeap Innovations: Core Product Line

Our current flagship products define the cutting edge of technology:

1. The Q-Core Processor: Released in 2023, this is the world's first commercially viable room-temperature quantum chip. It operates at 256 qubits and is primarily used by research institutions for complex climate modeling and cryptographic analysis.

2. The NeuralWeave Interface (Neural Link): Launched in early 2025, this non-invasive headset allows users to control computer interfaces using sub-vocalized thoughts. It utilizes a proprietary graphene-based sensor mesh that reads motor cortex signals with 99.8% accuracy.

Both products integrate seamlessly via the proprietary 'LeapOS' operating system.
""",
    
    "QuantumLeap_Financials.pdf": """QuantumLeap Innovations: 2025 Financial Overview

The fiscal year 2025 has been a record-breaking period for QuantumLeap Innovations. 

Q3 2025 Financial Highlights:
- Gross Revenue: $450 million (a 120% increase year-over-year).
- Net Profit Margin: 28%.
- The NeuralWeave Interface accounted for $200 million of the Q3 revenue, far exceeding initial market projections.
- R&D Expenditure: $85 million, heavily focused on next-generation wearable technologies.

In November 2025, the company closed a Series C funding round, raising an additional $1.2 billion, valuing the company at $15 billion. This capital is strictly ring-fenced for expanding manufacturing facilities and funding the highly anticipated 'Project Chronos'.
""",
    
    "QuantumLeap_Roadmap.pdf": """QuantumLeap Innovations: 2026 Product Roadmap

Looking ahead, QuantumLeap is poised to disrupt the temporal-processing market.

Project Chronos (Target Release: Q4 2026):
Project Chronos is our most ambitious endeavor yet. It is a predictive analytics engine that leverages the Q-Core Processor to forecast micro-economic trends with unprecedented accuracy. The project is being personally overseen by co-founder Dr. Elara Vance.

NeuralWeave V2 (Target Release: Q2 2026):
The next iteration of our headset will be 40% lighter and will introduce 'two-way' communication, allowing the system to transmit subtle haptic feedback directly to the user's motor cortex, simulating physical touch in virtual environments.
"""
}

# Create a directory for the test files
os.makedirs("test_documents", exist_ok=True)

for filename, content in docs.items():
    doc = fitz.open()
    page = doc.new_page()
    
    # Simple text insertion with word wrapping
    rect = fitz.Rect(50, 50, 550, 800)
    page.insert_textbox(rect, content, fontsize=12, fontname="helv")
    
    filepath = os.path.join("test_documents", filename)
    doc.save(filepath)
    doc.close()

print("Successfully generated 4 PDF test documents in the 'test_documents' folder.")
