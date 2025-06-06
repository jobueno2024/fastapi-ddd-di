# fastapi-ddd-di

## ディレクトリ構造
```plaintext
.
├── src/
│   ├── main.py
│   ├── presentation/
│   │   ├── __init__.py
│   │   └── todo_router.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── todo_service.py
│   │   └── interfaces.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── repositories.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── in_memory_todo_repository.py
│   │   └── di.py
│   └── tests/
│       ├── __init__.py
│       └── test_todo_service.py
└── requirements.txt
```

## 実行方法
1. 上記ファイルをプロジェクト構造通りに配置します。
2. requirements.txt を使って依存関係をインストールします。
```bash
pip install -r requirements.txt
```
3. アプリケーションを起動します。
```bash
uvicorn src.main:app --reload
```
4. ブラウザで http://127.0.0.1:8000/docs にアクセスすると、FastAPIのSwagger UIが表示され、APIエンドポイントを試すことができます。
テストの実行
```bash
pytest src/tests/
```
