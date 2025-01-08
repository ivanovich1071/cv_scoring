import requests


def get_html(url: str):
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )


# print(response.text)
# with open("vacancy.html", "w") as f:
#     f.write(response.text)

from bs4 import BeautifulSoup


from bs4 import BeautifulSoup

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Извлечение заголовка вакансии
    title_element = soup.find("h1")
    title = title_element.get_text(strip=True) if title_element else "Заголовок не найден"

    # Извлечение зарплаты
    salary_element = soup.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite")
    salary = salary_element.get_text(strip=True) if salary_element else "Зарплата не указана"

    # Извлечение опыта работы
    experience_element = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience_element.get_text(strip=True) if experience_element else "Опыт не указан"

    # Извлечение типа занятости и режима работы
    employment_mode_element = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode_element.get_text(strip=True) if employment_mode_element else "Не указано"

    # Извлечение компании
    company_element = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company_element.get_text(strip=True) if company_element else "Компания не указана"

    # Извлечение местоположения
    location_element = soup.find("p", {"data-qa": "vacancy-view-location"})
    location = location_element.get_text(strip=True) if location_element else "Местоположение не указано"

    # Извлечение описания вакансии
    description_element = soup.find("div", {"data-qa": "vacancy-description"})
    description = description_element.get_text(strip=True) if description_element else "Описание не указано"

    # Извлечение ключевых навыков
    skills_elements = soup.find_all("span", {"data-qa": "bloko-tag__text"})
    skills = [skill.get_text(strip=True) for skill in skills_elements] if skills_elements else ["Навыки не указаны"]

    # Формирование строки в формате Markdown
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



# from bs4 import BeautifulSoup

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение основных данных кандидата
    name = soup.find('h2', {'data-qa': 'bloko-header-1'}).text.strip()
    gender_age = soup.find('p').text.strip()
    location = soup.find('span', {'data-qa': 'resume-personal-address'}).text.strip()
    job_title = soup.find('span', {'data-qa': 'resume-block-title-position'}).text.strip()
    job_status = soup.find('span', {'data-qa': 'job-search-status'}).text.strip()

    # Извлечение опыта работы
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
    experiences = []
    for item in experience_items:
        period = item.find('div', class_='bloko-column_s-2').text.strip()
        duration = item.find('div', class_='bloko-text').text.strip()
        period = period.replace(duration, f" ({duration})")

        company = item.find('div', class_='bloko-text_strong').text.strip()
        position = item.find('div', {'data-qa': 'resume-block-experience-position'}).text.strip()
        description = item.find('div', {'data-qa': 'resume-block-experience-description'}).text.strip()
        experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")

    # Извлечение ключевых навыков
    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})]

    # Формирование строки в формате Markdown
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

    return markdown

def get_candidate_info(url: str):
    response = get_html(url)
    return extract_candidate_data(response.text)

def get_job_description(url: str):
    response = get_html(url)
    return extract_vacancy_data(response.text)
