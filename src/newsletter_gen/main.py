from src.newsletter_gen.crew import NewsletterGenCrew

def load_html_template():
    with open('Newsletter_crewAI\src\newsletter_gen\config\newsletter_template.html','r') as file:
        html_template=file.read()
    return html_template
    
def run():
    inputs = {
        'topic': input('Enter the topic for yout newsletter: '),
        'personal_message': input('Enter a personal message for your newsletter: '),
        'html_template': load_html_template()
    }
    NewsletterGenCrew().crew().kickoff(inputs=inputs)
