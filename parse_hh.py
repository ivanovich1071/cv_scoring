from bs4 import BeautifulSoup
import requests

# Функция для получения HTML страницы
def get_html(url: str, output_file: str):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    response.raise_for_status()

    # Сохранение структуры страницы в файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.text)

    return response.text

# Функция для извлечения данных из вакансии
def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    def get_element(selector, default="Не указано"):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else default

    title = get_element("h1[data-qa='vacancy-title']")
    salary = get_element("span.bloko-header-section-2")
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

# Функция для извлечения данных из резюме
def extract_candidate_data(html):
    soup = BeautifulSoup(html, "html.parser")

    def get_element(selector):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else "Не указано"

    name = get_element("h2[data-qa='resume-personal-name']")
    gender_age = get_element("p[data-qa='resume-personal-gender']")
    location = get_element("span[data-qa='resume-personal-address']")
    job_title = get_element("span[data-qa='resume-block-title-position']")
    job_status = get_element("span[data-qa='resume-block-status']")

    experience_section = soup.select_one("div[data-qa='resume-block-experience']")
    experiences = []
    if experience_section:
        experience_items = experience_section.select("div[data-qa='resume-block-experience-item']")
        for item in experience_items:
            period = item.select_one("div[data-qa='resume-block-experience-dates']").get_text(strip=True) if item.select_one("div[data-qa='resume-block-experience-dates']") else "Период не указан"
            company = item.select_one("div[data-qa='resume-block-experience-company']").get_text(strip=True) if item.select_one("div[data-qa='resume-block-experience-company']") else "Компания не указана"
            position = item.select_one("div[data-qa='resume-block-experience-position']").get_text(strip=True) if item.select_one("div[data-qa='resume-block-experience-position']") else "Должность не указана"
            description = item.select_one("div[data-qa='resume-block-experience-description']").get_text(strip=True) if item.select_one("div[data-qa='resume-block-experience-description']") else "Описание не указано"
            experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}")

    skills_elements = soup.select("span[data-qa='bloko-tag__text']")
    skills = [skill.get_text(strip=True) for skill in skills_elements] if skills_elements else ["Навыки не указаны"]

    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    for exp in experiences:
        markdown += exp + "\n\n"
    markdown += "## Ключевые навыки\n\n"
    markdown += ", ".join(skills)

    return markdown.strip()

# Основная функция обработки страницы
def process_page(url, output_structure_file, extractor):
    html = get_html(url, output_structure_file)
    return extractor(html)
