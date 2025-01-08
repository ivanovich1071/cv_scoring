from bs4 import BeautifulSoup
import requests

def get_html(url: str):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    response.raise_for_status()
    return response.text

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    def get_element(selector, attribute=None):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else "Не указано"

    # Извлечение данных
    title = get_element("h1[data-qa='vacancy-title']")
    salary = get_element("span.bloko-header-section-2.bloko-header-section-2_lite")
    experience = get_element("span[data-qa='vacancy-experience']")
    employment_mode = get_element("p[data-qa='vacancy-view-employment-mode']")
    company = get_element("a[data-qa='vacancy-company-name']")
    location = get_element("p[data-qa='vacancy-view-location']")
    description = get_element("div[data-qa='vacancy-description']")

    skills_elements = soup.select("span[data-qa='bloko-tag__text']")
    skills = [skill.get_text(strip=True) for skill in skills_elements] if skills_elements else ["Навыки не указаны"]

    markdown = f"""
# {title}

**Компания:** {company}  
**Зарплата:** {salary}  
**Опыт работы:** {experience}  
**Тип занятости и режим работы:** {employment_mode}  
**Местоположение:** {location}  

## Описание вакансии
{description}

## Ключевые навыки
- {'\n- '.join(skills)}
"""

    return markdown.strip()

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    def get_element(selector, attribute=None):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else "Не указано"

    # Извлечение данных
    name = get_element("h2[data-qa='bloko-header-1']")
    gender_age = get_element("p")
    location = get_element("span[data-qa='resume-personal-address']")
    job_title = get_element("span[data-qa='resume-block-title-position']")
    job_status = get_element("span[data-qa='job-search-status']")

    experience_section = soup.select_one("div[data-qa='resume-block-experience']")
    experiences = []
    if experience_section:
        experience_items = experience_section.select("div.resume-block-item-gap")
        for item in experience_items:
            period = get_element("div.bloko-column_s-2")
            company = get_element("div.bloko-text_strong")
            position = get_element("div[data-qa='resume-block-experience-position']")
            description = get_element("div[data-qa='resume-block-experience-description']")
            experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")

    skills_elements = soup.select("span[data-qa='bloko-tag__text']")
    skills = [skill.get_text(strip=True) for skill in skills_elements] if skills_elements else ["Навыки не указаны"]

    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    for exp in experiences:
        markdown += exp + "\n"
    markdown += "## Ключевые навыки\n\n"
    markdown += ', '.join(skills) + "\n"

    return markdown.strip()
