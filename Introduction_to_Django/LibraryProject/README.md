# Library Management System

A Django-based library management system that allows users to manage books, members, and borrowing records.

## Features

- Book management (add, edit, delete, search)
- Member management (registration, update, remove)
- Borrowing system (check-out, check-in, due dates)
- Search functionality
- User authentication and authorization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LibraryProject.git
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Usage

- Access admin panel at `http://localhost:8000/admin`
- Browse library catalog at `http://localhost:8000`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)