import json
import csv
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_schema(schema_path):
    """Load the schema JSON file."""
    with open(schema_path, 'r') as f:
        return json.load(f)

def upload_file_to_openai(client, file_path):
    """Upload a PDF file to OpenAI."""
    print(f"Uploading file: {file_path}")
    with open(file_path, 'rb') as f:
        file = client.files.create(
            file=f,
            purpose='assistants'
        )
    print(f"✓ File uploaded with ID: {file.id}")
    return file.id

def create_assistant(client, file_id):
    """Create an assistant with file search capability."""
    print("Creating assistant with file search capability...")
    assistant = client.beta.assistants.create(
        name="Paper Data Extractor",
        instructions="""You are helping with a systematic literature review on green microservices. 
        You will extract data from the uploaded paper. 
        Answer questions based ONLY on the paper content.
        If information is not explicitly mentioned in the paper, respond with "Not Found".""",
        model="gpt-4o",  # Updated to current model
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_stores": [{
                    "file_ids": [file_id]
                }]
            }
        }
    )
    print(f"✓ Assistant created with ID: {assistant.id}")
    return assistant.id

def build_prompt(subquestion_text, parameter_prompt):
    """Build the full prompt for a parameter."""
    return f"""I am conducting a systematic literature review on green microservices. I am extracting data from this paper. I will ask you questions based on this paper and this paper alone. Do not provide an answer that is not explicitly mentioned in this paper. If you are unsure, you can simply respond with "Not Found"

{subquestion_text}

{parameter_prompt}

Short answer only, if unsure or not included in text respond with "Not Found". You do NOT need to use one of the provided examples."""

def ask_question(client, assistant_id, thread_id, question, max_retries=3):
    """Ask a question and get the response with retry logic."""
    for attempt in range(max_retries):
        try:
            # Add message to thread
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=question
            )
            
            # Run the assistant
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            
            # Wait for completion with timeout
            max_wait_time = 120  # 2 minutes max
            elapsed_time = 0
            
            while run.status in ['queued', 'in_progress', 'cancelling']:
                time.sleep(2)
                elapsed_time += 2
                
                if elapsed_time > max_wait_time:
                    print(f"  ⚠ Timeout after {max_wait_time}s, cancelling run...")
                    client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run.id)
                    break
                
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
            
            if run.status == 'completed':
                # Get messages
                messages = client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                # Get the latest assistant message
                for message in messages.data:
                    if message.role == 'assistant':
                        return message.content[0].text.value
            
            # Handle failed runs
            if run.status == 'failed':
                error_info = f"Run failed"
                if hasattr(run, 'last_error') and run.last_error:
                    error_info += f": {run.last_error.message}"
                print(f"  ⚠ {error_info}")
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"  ↻ Retrying in {wait_time}s... (attempt {attempt + 2}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    return f"ERROR: {error_info} (after {max_retries} attempts)"
            
            # Handle other non-completed statuses
            return f"ERROR: Run ended with status '{run.status}'"
            
        except Exception as e:
            print(f"  ⚠ Exception: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"  ↻ Retrying in {wait_time}s... (attempt {attempt + 2}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                return f"ERROR: {str(e)} (after {max_retries} attempts)"
    
    return "ERROR: Max retries exceeded"

def extract_data(schema_path, pdf_path, output_csv, api_key):
    """Extract data from PDF using OpenAI API and save to CSV."""
    client = OpenAI(api_key=api_key)
    schema = load_schema(schema_path)
    
    # Upload PDF
    file_id = upload_file_to_openai(client, pdf_path)
    
    # Create assistant
    assistant_id = create_assistant(client, file_id)
    
    # Create thread
    print("Creating conversation thread...")
    thread = client.beta.threads.create()
    thread_id = thread.id
    print(f"✓ Thread created with ID: {thread_id}")
    
    # Prepare CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['RQ_ID', 'Subquestion_ID', 'Subquestion', 'Parameter_ID', 'Parameter_Name', 'Response'])
        
        print("\n" + "="*60)
        print("Starting data extraction...")
        print("="*60 + "\n")
        
        for rq in schema['research_questions']:
            rq_id = rq['id']
            
            for subquestion in rq['subquestions']:
                subq_id = subquestion['id']
                subq_text = subquestion['question']
                
                for parameter in subquestion['parameters']:
                    param_id = parameter['id']
                    param_name = parameter['name']
                    param_prompt = parameter['prompt']
                    
                    # Build full prompt
                    full_prompt = build_prompt(subq_text, param_prompt)
                    
                    print(f"\nProcessing: {param_id} - {param_name}")
                    print(f"Prompt:\n{full_prompt}\n")
                    print("-" * 60)
                    
                    try:
                        response = ask_question(client, assistant_id, thread_id, full_prompt)
                        
                        # Write to CSV
                        csv_writer.writerow([rq_id, subq_id, subq_text, param_id, param_name, response])
                        csv_file.flush()
                        
                        print(f"Response: {response[:100]}...")
                        
                    except Exception as e:
                        print(f"Error processing {param_id}: {str(e)}")
                        csv_writer.writerow([rq_id, subq_id, subq_text, param_id, param_name, f"ERROR: {str(e)}"])
                        csv_file.flush()
                    
                    # Longer delay to avoid rate limits
                    time.sleep(1.5)
    
    # Cleanup
    print("\n" + "="*60)
    print("Cleaning up...")
    print("="*60)
    try:
        client.beta.assistants.delete(assistant_id)
        print("✓ Assistant deleted")
    except Exception as e:
        print(f"Note: Could not delete assistant: {e}")
    
    print("\n" + "="*60)
    print("✓ Extraction complete!")
    print("="*60)

if __name__ == "__main__":
    # Configuration
    SCHEMA_PATH = "schema.json"
    PDF_PATH = "dataset/['N. Toosi - GreenFog A Framework for Sustainable Fog Computing.pdf"  # Path to your PDF file
    OUTPUT_CSV = "extracted_data.csv"
    
    # Get API key from environment variable
    API_KEY = os.getenv('OPENAI_API_KEY')
    
    if not API_KEY:
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("\nPlease set it using:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("\nOr get your API key from: https://platform.openai.com/api-keys")
        exit(1)
    
    if not os.path.exists(PDF_PATH):
        print(f"ERROR: PDF file not found: {PDF_PATH}")
        print("\nPlease update the PDF_PATH variable with the correct path to your PDF file")
        exit(1)
    
    extract_data(SCHEMA_PATH, PDF_PATH, OUTPUT_CSV, API_KEY)
    print(f"\nData extraction complete. Results saved to {OUTPUT_CSV}")