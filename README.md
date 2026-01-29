REST API для системы управления запасами с поддержкой иерархических категорий, заказов и клиентов

inventory-management-system/
├── .env.example
├── .dockerignore
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
├── alembic.ini
├── nginx.conf
│
├── alembic/
│   ├── __init__.py
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── __init__.py
│
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── app.py
│   │   ├── database.py
│   │   ├── logger.py
│   │   └── dependencies.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities.py
│   │   └── interfaces.py
│   ├── application/
│   │   ├── __init__.py
│   │   └── use_cases/
│   │       ├── __init__.py
│   │       └── add_item_to_order.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repositories.py
│   │   │   └── session.py
│   │   └── exceptions.py
│   └── presentation/
│       ├── __init__.py
│       └── api/
│           ├── __init__.py
│           ├── router.py
│           └── endpoints/
│               ├── __init__.py
│               ├── orders.py
│               ├── items.py
│               └── categories.py
│
├── scripts/
│   └── check_code.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_domain/
│   │   └── test_entities.py
│   ├── test_application/
│   │   └── test_add_item_to_order.py
│   └── test_integration/
│       └── test_api.py
│
└── docs/
    ├── database_schema.md
    ├── sql_queries.md
    └── api_documentation.md