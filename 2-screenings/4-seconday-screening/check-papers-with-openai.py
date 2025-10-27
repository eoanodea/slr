import os
import pandas as pd
from openai import OpenAI
from PyPDF2 import PdfReader
import re

# Set your OpenAI API key here or as an environment variable
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)


# Inclusion/Exclusion criteria (edit as needed)
IC = [
    "IC5 - Title/abstract indicates energy efficiency/consumption is considered in software engineering or architecture.",
    "IC6 - Title/abstract refers to solutions for energy-efficient microservices.",
]
EC = [
    "EC4 - Only discusses energy at hardware/infrastructure level, not software/architecture.",
    "EC5 - No mention of measurement, analysis, or evaluation of energy in microservices.",
    "EC6 - The paper is a secondary study (SLR, mapping studies...)",
]

# def ask_openai(title, abstract):
#     prompt = f"""
#     I am screening papers for a systematic literature review.
#     The topic of the systematic review is energy efficiency and energy consumption in microservice architectures.
#     The study should focus exclusively on this topic.

#     I give 2 examples with title and abstract that should be included.
#     Example 1:
#     - Title: Estimating the energy consumption of model-view-controller applications
#     - Abstract: For information and communication technology to reach its goal of zero emissions in 2050, power consumption must be reduced, including the energy consumed by software. To develop sustainability-aware software, green metrics have been implemented to estimate the energy consumed by the execution of an application. However, they have a rebound energy consumption effect because they require an application to be executed to estimate the energy consumed after each change. To address this problem, it is necessary to construct energy estimation models that do not require the execution of applications. This work addresses this problem by constructing a green model based on size, complexity and duplicated lines to estimate the energy consumed by model-view-controller applications without their execution. This article defines a model constructed based on 52 applications. The results were accurate in twelve applications, which showed that the joule estimation was very close to reality, avoiding the energy consumed by the execution of applications. © 2023, The Author(s).

#     Example 2:
#     - Title: Online Power Consumption Estimation for Functions in Cloud Applications
#     - Abstract: The growth of cloud services leads to more and more data centers that are increasingly larger and consume considerable amounts of power. To increase energy efficiency, informed decisions on workload placement and provisioning are essential. Micro-services and the upcoming serverless platforms with more granular deployment options exacerbate this problem. For this reason, knowing the power consumption of the deployed application becomes crucial, providing the necessary information for autonomous decision making. However, the actual power draw of a server running a specific application under load is not available without specialized measurement equipment or power consumption models. Yet, granularity is often only down to machine level and not application level. In this paper, we propose a monitoring and modeling approach to estimate power consumption on an application function level. The model uses performance counters that are allocated to specific functions to assess their impact on the total power consumption. Hence our model applies to a large variety of servers and for micro-service and serverless workloads. Our model uses an additional correction to minimize falsely allocated performance counters and increase accuracy. We validate the proposed approach on real hardware with a dedicated benchmarking application. The evaluation shows that our approach can be used to monitor application power consumption down to the function level with high accuracy for reliable workload provisioning and placement decisions.

#     Exclude the article if any of the following criteria are true:
#     {chr(10).join(f"- {c}" for c in EC)}

#     Include the article if any of the following criteria are true:
#     {chr(10).join(f"- {c}" for c in IC)}

#     Decide if the article should be included or excluded from the systematic review.
#     I give the title and abstract of the article as input.
#     Only answer INCLUDE or EXCLUDE, and the IC or EC ID (e.g. 'Include - IC5').
#     Be lenient. I prefer including papers by mistake rather than excluding them by mistake.

#     Paper Title: {title}
#     Abstract: {abstract}
#     """
    
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",  # or "gpt-4" if you have access
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=100,
#             temperature=0
#         )
#         answer = response.choices[0].message.content
#         return answer
#     except Exception as e:
#         print(f"Error: {e}")
#         return "API Error"

def extract_section(text, start_pattern, end_pattern):
    match = re.search(
        rf"{start_pattern}(.*?){end_pattern}",
        text,
        re.IGNORECASE | re.DOTALL
    )
    return match.group(1).strip() if match else "Not found"

def extract_intro_and_conclusion(pdf_path):
    # Extract all text from the PDF
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += "\n" + page_text

    # Normalize whitespace and line breaks
    full_text = re.sub(r'\r\n?', '\n', full_text)
    full_text = re.sub(r'\n+', '\n', full_text)

    # Introduction: from "Introduction" to a line starting with "II." or "2."
    intro = extract_section(
        full_text,
        r"(?i)NTRODUCTION\b",  # Start: "Introduction" possibly with number
        r"(?:\nII\.|\n2\.)"  # End: line starting with "II." or "2."
    )

    # Conclusion: from "Conclusion" or "Conclusions" to "References" or end of text
    conclusion = extract_section(
        full_text,
        r"(?:^|\n)(?:[IVXLCDM\d]+\.?\s*)?Conclusion[s]?\b",  # Start: "Conclusion" possibly with number
        r"(?:\nReferences|\Z|Acknowledgment)"  # End: "References" or end of text
    )

    return intro, conclusion

def main():
    pdf_dir = "asreview/seconday-screening/data"
    for fname in os.listdir(pdf_dir):
        if fname.endswith(".pdf"):
            path = os.path.join(pdf_dir, fname)
            intro, concl = extract_intro_and_conclusion(path)
            print(f"File: {fname}")
            print("Introduction:\n", intro[:1000], "\n")
            print("Conclusion:\n", concl[:1000], "\n")
            print("="*80)


if __name__ == "__main__":
    main()