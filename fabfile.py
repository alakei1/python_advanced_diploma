from fabric import task

# пока заглушка нету пока нет хоста


@task
def local_format(ctx):
    """Локально причесать код: заменяет black, isort и flake8"""
    pass


@task
def local_test(ctx):
    """Локальный запуск проверки типов и тестов pytest"""
    pass


@task
def deploy(ctx):
    """Деплой на сервер AWS (без Docker)"""
    pass
