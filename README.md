# Damn Vulnerable Class Management System

Damn Vulnerable Class Management System is a web application that is vulnerable to a number of web vulnerabilities. It is intended to be used by security professionals to test their skills and tools in a legal environment, help web developers better understand the processes of securing web applications and to aid teachers/students to teach/learn web application security in a class room environment.

## Installation

Install `pipenv`

```bash
pip install pipenv
```

Install dependencies

```bash
pipenv install
```

Enter environment

```bash
pipenv shell
```

Migrate database and setup groups

```bash
./scripts/setup.sh
```

This will guide you through the process of creating a superuser and setting up the groups.

Run the application

```bash
pipenv run python manage.py runserver
```

## Usage

Visit `http://localhost:8000/admin` and login with the superuser credentials you created in the setup script.

Create dummy data and then the application is ready to use.

## Vulnerabilities

DVGM contains the following vulnerabilities:
- SQL Injection
- Cross-Site Scripting (XSS)
- Missing server-side input validation
- Weak password hashing

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [DVGM](https://github.com/logicalhacking/dvgm)