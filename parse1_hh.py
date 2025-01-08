from bs4 import BeautifulSoup
import requests

def save_html_structure(url, filename):
    """
    Fetch the HTML structure of the given URL and save it to a file.

    :param url: URL of the webpage to fetch.
    :param filename: Name of the file to save the HTML structure.
    """
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            },
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        structure = soup.prettify()

        with open(filename, "w", encoding="utf-8") as file:
            file.write(structure)
            print(f"HTML structure saved to {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")

# Example usage
if __name__ == "__main__":
    # URL for the vacancy
    vacancy_url = "https://hh.ru/vacancy/114300788?query=%D0%BF%D1%80%D0%BE%D0%BC%D1%82+%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80&hhtmFrom=vacancy_search_list"
    save_html_structure(vacancy_url, "vacancy_structure.html")

    # URL for the resume
    resume_url = "https://rabota.by/resume/a8ad00ce0002b281ef0039ed1f476b7372374b?searchRid=173634579513729a0e0dc41b5ddf7cfb&hhtmFrom=resume_search_result"
    save_html_structure(resume_url, "resume_structure.html")
