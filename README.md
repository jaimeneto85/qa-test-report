# QA Test Report System

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)

A comprehensive Quality Assurance and Testing validation form system designed to standardize and streamline the QA process in software development projects.

## Motivation

In modern software development, maintaining high quality standards is crucial. The QA Test Report System addresses several key needs:

- **Standardization**: Ensures all QA engineers follow the same validation criteria
- **Comprehensive Coverage**: Validates multiple aspects of software delivery:
  - UX/UI Design Compliance
  - Functionality and Behavior
  - Code Quality and Testability
  - Accessibility and Performance
- **Documentation**: Generates detailed PDF reports for each validation
- **Traceability**: Links validations to specific tasks and versions
- **Multilingual Support**: Available in multiple languages (currently English and Portuguese)

## Features

- 📋 Step-by-step validation process
- 🎨 UX/UI compliance verification
- 🔍 Functionality and behavior testing
- 💻 Code quality assessment
- ♿ Accessibility validation
- 📊 Performance evaluation
- 📝 Detailed feedback system
- 📄 PDF report generation
- 🌐 Internationalization support
- 🎯 Task tracking integration

## Prerequisites

Before installing the application, make sure you have the following installed:

1. Python 3.10 or higher
2. Pipenv (install with `pip install pipenv`)
3. gettext:
   - On macOS:
     ```bash
     brew install gettext
     ```
   - On Ubuntu/Debian:
     ```bash
     sudo apt-get install gettext
     ```
   - On Windows:
     Download and install gettext from the [GNU gettext website](https://www.gnu.org/software/gettext/)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/qa-test-report.git
cd qa-test-report
```

2. Install dependencies using Pipenv:
```bash
pipenv run streamlit run app.py
```

This will create a virtual environment and install all required dependencies from the Pipfile.

## Running the Application

1. Activate the Pipenv shell:
```bash
pipenv shell
```

2. Start the Streamlit application:
```bash
streamlit run app.py
```

3. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Translation System

The application supports multiple languages through gettext. Currently supported languages:
- English (en_US)
- Portuguese (pt_BR)

### Adding New Translations

1. Create a new language directory:
```bash
mkdir -p locale/[LANG_CODE]/LC_MESSAGES
```

2. Copy the template:
```bash
cp locale/messages.pot locale/[LANG_CODE]/LC_MESSAGES/messages.po
```

3. Edit the `messages.po` file with your translations

4. Compile translations:
```bash
./compile_translations.py
```

### Updating Existing Translations

1. Update the messages template:
```bash
pybabel extract -o locale/messages.pot .
```

2. Update translation files:
```bash
pybabel update -i locale/messages.pot -d locale
```

3. Edit the updated .po files in `locale/[LANG_CODE]/LC_MESSAGES/`

4. Compile translations:
```bash
./compile_translations.py
```

## Project Structure

```
qa-test-report/
├── app.py                 # Main application file
├── lib/                   # Library modules
│   ├── __init__.py
│   ├── form_data.py      # Form data handling
│   ├── pdf_generator.py  # PDF report generation
│   ├── styles.py         # UI styles
│   └── translations.py   # i18n support
├── locale/               # Translation files
│   ├── en_US/           # English translations
│   └── pt_BR/           # Portuguese translations
├── reports/             # Generated PDF reports
├── Pipfile              # Pipenv dependencies
├── Pipfile.lock         # Pipenv lock file
└── README.md            # This file
```

## Development

To install development dependencies:
```bash
pipenv install --dev
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team.

😉 Stay in touch:

- [LinkedIn](https://www.linkedin.com/in/jaimeflneto/)
- [GitHub](https://github.com/jaimeneto85)
- [Email](mailto:jaimeflneto@gmail.com)
