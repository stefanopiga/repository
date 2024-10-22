# pylint: skip-file

import json
import os
import requests
from langchain.tools import tool


class SearchTools():
    """Search Tool"""

    @tool("Search the internet")
    def search_internet(query, top_result_to_return=10):
        """Useful to search the internet
        about a given topic and return relevant results"""
        print("Searching the internet...")
        url = "https://google.serper.dev/search"
        payload = json.dumps(
            {"q": query, "num": top_result_to_return, "tbm": "nws"})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }

        try:
            response = requests.request(
                "POST", url, headers=headers, data=payload, timeout=15)
            response.raise_for_status()  # Raise an error for bad status codes
        except requests.exceptions.HTTPError as e:
            return [{"error": f"HTTP error occurred: {e}"}]
        except requests.exceptions.ConnectionError as e:
            return [{"error": f"Connection error occurred: {e}"}]
        except requests.exceptions.Timeout as e:
            return [{"error": f"Timeout error occurred: {e}"}]
        except requests.exceptions.RequestException as e:
            return [{"error": f"An error occurred: {e}"}]

        data = response.json()

        if 'organic' not in data:
            return [{"error": "Sorry, I couldn't find anything about that, there could be an error with your Serper API key."}]
        else:
            results = data['organic']
            output = []
            print("Results:", results[:top_result_to_return])
            for result in results[:top_result_to_return]:
                try:
                    date = result.get('date', 'Date not available')
                    output.append({
                        "title": result['title'],
                        "link": result['link'],
                        "date": date,
                        "snippet": result['snippet']

                    })
                except KeyError as e:
                    output.append(
                        {"error": f" Error parsing result: missing {e}"})
            return output
