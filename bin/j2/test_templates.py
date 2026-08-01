import pytest
import jinja2
from pathlib import Path
import tempfile
import os

from j2.templates import TemplateContainer  

# Определяем фикстуры на уровне модуля для использования во всех классах
@pytest.fixture
def temp_dir():
    """Создает временную директорию с шаблонами"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Создаем несколько тестовых шаблонов
        (tmp_path / "hello.j2").write_text("Hello, {{ name }}!")
        (tmp_path / "greeting.j2").write_text("{{ greeting }}, {{ name }}!")
        (tmp_path / "list.j2").write_text(
            "{% for item in items %}{{ item }}{% if not loop.last %}, {% endif %}{% endfor %}"
        )
        (tmp_path / "condition.j2").write_text(
            "{% if active %}Active{% else %}Inactive{% endif %}"
        )
        
        yield tmp_path


@pytest.fixture
def container(temp_dir):
    """Создает экземпляр TempateContainer"""
    return TempateContainer(str(temp_dir))


class TestTemplateContainer:
    """Тесты для класса TempateContainer"""
    
    def test_init(self, temp_dir):
        """Тест инициализации"""
        container = TempateContainer(str(temp_dir))
        assert container.path == str(temp_dir)
    
    def test_template_exists(self, container):
        """Тест получения существующего шаблона"""
        template_func = container.template("hello")
        assert callable(template_func)
    
    def test_template_not_exists(self, container):
        """Тест получения несуществующего шаблона"""
        with pytest.raises(FileNotFoundError):
            container.template("nonexistent")
    
    def test_template_render_basic(self, container):
        """Тест рендеринга простого шаблона"""
        render = container.template("hello")
        result = render({"name": "World"})
        assert result == "Hello, World!"
    
    def test_template_render_with_multiple_variables(self, container):
        """Тест рендеринга с несколькими переменными"""
        render = container.template("greeting")
        result = render({"greeting": "Good morning", "name": "Alice"})
        assert result == "Good morning, Alice!"
    
    def test_template_render_with_list(self, container):
        """Тест рендеринга с итерацией по списку"""
        render = container.template("list")
        result = render({"items": ["apple", "banana", "orange"]})
        assert result == "apple, banana, orange"
    
    def test_template_render_with_condition_true(self, container):
        """Тест рендеринга с условием (True)"""
        render = container.template("condition")
        result = render({"active": True})
        assert result == "Active"
    
    def test_template_render_with_condition_false(self, container):
        """Тест рендеринга с условием (False)"""
        render = container.template("condition")
        result = render({"active": False})
        assert result == "Inactive"
    
    def test_template_render_multiple_calls(self, container):
        """Тест множественных вызовов одного шаблона"""
        render = container.template("hello")
        
        result1 = render({"name": "Alice"})
        result2 = render({"name": "Bob"})
        
        assert result1 == "Hello, Alice!"
        assert result2 == "Hello, Bob!"
    
    def test_template_render_with_missing_variable(self, container):
        """Тест рендеринга с отсутствующей переменной"""
        render = container.template("hello")
        result = render({})  # Переменная 'name' отсутствует
        assert result == "Hello, !"  # Jinja2 подставляет пустую строку
    
    def test_different_template_extensions(self, temp_dir):
        """Тест работы с разными расширениями файлов"""
        # Создаем шаблон с другим расширением
        (temp_dir / "test.txt.j2").write_text("Content: {{ value }}")
        
        container = TempateContainer(str(temp_dir))
        render = container.template("test.txt")
        result = render({"value": "test"})
        assert result == "Content: test"
    
    def test_path_resolution(self, temp_dir):
        """Тест правильного разрешения пути"""
        # Создаем вложенную директорию
        nested_dir = temp_dir / "nested"
        nested_dir.mkdir()
        (nested_dir / "nested.j2").write_text("Nested: {{ value }}")
        
        container = TempateContainer(str(temp_dir))
        
        # Проверяем, что шаблон во вложенной директории доступен
        render = container.template("nested/nested")
        result = render({"value": "test"})
        assert result == "Nested: test"
    
    def test_template_content_with_special_characters(self, temp_dir):
        """Тест шаблона со специальными символами"""
        (temp_dir / "special.j2").write_text("{{ value|safe }}")
        
        container = TempateContainer(str(temp_dir))
        render = container.template("special")
        result = render({"value": "<script>alert('test')</script>"})
        assert result == "<script>alert('test')</script>"
    
    def test_template_reuse(self, container):
        """Тест повторного использования одного шаблона"""
        render_hello = container.template("hello")
        render_hello_again = container.template("hello")
        
        # Проверяем, что это разные объекты функций
        assert render_hello is not render_hello_again
        
        result1 = render_hello({"name": "Alice"})
        result2 = render_hello_again({"name": "Bob"})
        
        assert result1 == "Hello, Alice!"
        assert result2 == "Hello, Bob!"


# Дополнительные тесты для проверки edge cases
class TestTemplateContainerEdgeCases:
    """Тесты для пограничных случаев"""
    
    def test_empty_template(self, temp_dir):
        """Тест с пустым шаблоном"""
        (temp_dir / "empty.j2").write_text("")
        
        container = TempateContainer(str(temp_dir))
        render = container.template("empty")
        result = render({"any": "value"})
        assert result == ""
    
    def test_template_with_whitespace(self, temp_dir):
        """Тест шаблона с пробелами"""
        (temp_dir / "whitespace.j2").write_text("  {{ value }}  ")
        
        container = TempateContainer(str(temp_dir))
        render = container.template("whitespace")
        result = render({"value": "test"})
        assert result == "  test  "
    
    def test_path_with_trailing_slash(self, temp_dir):
        """Тест с путем, заканчивающимся на слеш"""
        path_with_slash = str(temp_dir) + "/"
        container = TempateContainer(path_with_slash)
        render = container.template("hello")
        result = render({"name": "World"})
        assert result == "Hello, World!"
    
    def test_template_with_complex_structure(self, temp_dir):
        """Тест со сложной структурой шаблона"""
        (temp_dir / "complex.j2").write_text(
            "{% for user in users %}"
            "{{ user.name }} ({{ user.age }} years)"
            "{% if not loop.last %}, {% endif %}"
            "{% endfor %}"
        )
        
        container = TempateContainer(str(temp_dir))
        render = container.template("complex")
        users = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
        result = render({"users": users})
        assert result == "Alice (30 years), Bob (25 years)"
    
    def test_nested_template_with_same_name(self, temp_dir):
        """Тест с вложенными шаблонами с одинаковыми именами"""
        # Создаем шаблон в корне
        (temp_dir / "test.j2").write_text("Root: {{ value }}")
        
        # Создаем шаблон во вложенной папке
        nested_dir = temp_dir / "nested"
        nested_dir.mkdir()
        (nested_dir / "test.j2").write_text("Nested: {{ value }}")
        
        container = TempateContainer(str(temp_dir))
        
        # Проверяем, что берется корневой шаблон
        render = container.template("test")
        result = render({"value": "root"})
        assert result == "Root: root"


# Альтернативный вариант - использование параметризации
class TestTemplateContainerParameterized:
    """Параметризованные тесты"""
    
    @pytest.mark.parametrize("template_name,context,expected", [
        ("hello", {"name": "World"}, "Hello, World!"),
        ("hello", {"name": "Python"}, "Hello, Python!"),
        ("greeting", {"greeting": "Hi", "name": "John"}, "Hi, John!"),
        ("condition", {"active": True}, "Active"),
        ("condition", {"active": False}, "Inactive"),
    ])
    def test_multiple_templates(self, container, template_name, context, expected):
        """Параметризованный тест для разных шаблонов"""
        render = container.template(template_name)
        result = render(context)
        assert result == expected


# Пример запуска тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
