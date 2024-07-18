import click
import requests

OLLAMA_API_URL = 'http://localhost:11434/api/chat'


def get_summary(text):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "model": "qwen2",
        "messages": [
            {
            "role": "user",
            "content": text
            }
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        summary = response.json().get('message', {}).get('content', 'No summary available.')
        return summary
    else:
        return f"Error: {response.status_code} - {response.text}"


@click.command()
@click.option('--text', '-t', help='Text to summarize')
@click.option('--file', '-f', type=click.Path(exists=True), help='Text file to summarize')
def summarize(text, file):
    if file:
        with open(file, 'r') as f:
            text = f.read()

    if not text:
        click.echo("Please provide text or a text file to summarize.")
        return

    summary = get_summary(text)
    click.echo(f"Summary:\n{summary}")


if __name__ == '__main__':
    summarize()
