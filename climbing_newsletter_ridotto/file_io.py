
"""Creazione file output"""
from datetime import datetime
import os


#def save_markdown(task_output):
#    """file di output"""
#    # Get today's date in the format YYYY-MM-DD
#    today_date = datetime.now().strftime('%Y-%m-%d')
#    # Set the filename with today's date
#    filename = f"{today_date}.md"
#    # Write the task output to the markdown file
#    with open(filename, 'w') as file:
#        file.write(task_output.result)
#    print(f"Newsletter saved as {filename}")


def save_markdown(task_output):
    """method for saving results"""
    try:
        today_date = datetime.now().strftime('%Y-%m-%d')
        base_path = r"C:/Users/user/Desktop/CODing/crew_AI/heirerchal_process/climbing_newsletter_ridotto"
        filename = f"{today_date}.md"
        full_path = os.path.join(base_path, filename)

        output_string = task_output.result if hasattr(task_output, 'result') else str(task_output)

        with open(full_path, 'w', encoding='utf=8') as file:
            file.write(output_string)  # Modifica qui se necessario
        print(f"Newsletter saved as {full_path}")
    except ImportError as e:
        print(f"Failed to save the newsletter: {e}")
