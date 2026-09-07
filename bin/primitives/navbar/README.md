# NavbarBuilder

Двухуровневое меню сайта. Дерево собирается один раз из `meta.yaml`, затем для каждой страницы строится контекст: верхний ряд и (если нужно) нижний.

Подключение: `Builder` в `bin/processors/builder.py` вызывает `NavbarBuilder(root).build()`, а в шаблон страницы передаёт `navbar.context(context)` вместе с `root` и параметрами типа страницы.

Шаблон: `jinja/partials/navbar.j2`. Стили: `src/assets/navbar.css` (подключается как `assets/navbar.css` в `jinja/pages/*.j2`).

## Источник данных

Читается только блок `page` в `meta.yaml`. Каталог без файла или без `page:` в меню не попадает.

Подпись пункта: `page.slug`, иначе `page.title`. Если оба пустые, на первом уровне подставляется `Home`, на втором — сегмент `url`.

Состав меню задаёт `page.children` **родителя**:

| Элемент | Поведение |
| --- | --- |
| `"."` | Пропускается (это сама страница). |
| строка | Имя подкаталога. Нужны каталог и его `meta.yaml`. |
| объект | Внешняя/произвольная ссылка: `title` ← `slug`, `url` ← `url`. Дочерние пункты не разбираются. |
| остальное | Игнорируется. |

Первый уровень — `children` корня (`src/meta.yaml`), плюс сам корень как Home (`url: ""`). Второй уровень — `children` **текущего** пункта первого уровня. Глубже третьего сегмента пути навбар не смотрит.

Пример корня:

```yaml
page:
  slug: "Home"
  children:
    - .
    - ai
    - dev
    - hobby
    - type: external
      url: blog
      slug: Blog
```

У раздела свои дети — они станут нижней полосой, когда открыт этот раздел:

```yaml
# src/ai/meta.yaml
page:
  title: AI
  children: ['clients', 'prompts', 'web', 'ru']
```

## API

```python
nav = NavbarBuilder(root).build()
ctx = nav.context(page_context)  # dict с upper_items и lower_items
```

`page_context` должен иметь:

- `subdir` — относительный путь текущей страницы (`"."` или `""` для корня, иначе `ai`, `ai/clients`, …);
- `web` — `True`: ссылки вида `/ai/`; `False`: `/ai/index.html` (локальный просмотр файлов).

`context()` возвращает:

```python
{
  "upper_items": [ { "url", "title", "current" }, ... ],
  "lower_items": [ { "url", "title", "current" }, ... ],
}
```

- `url` — абсолютный путь от корня сайта (в шаблоне к нему приклеивается `root`).
- `current` — совпадение с префиксом `subdir` той же глубины (`primitives.subdir.subdir`).
- `lower_items` пустой на Home и если у выбранного верхнего пункта нет детей.

Ключ верхнего пункта — первый сегмент `subdir`. Для `ai/clients` текущий верхний — `ai`, нижний ряд — дети `ai`, текущий нижний — `clients`.

## Шаблон

```html
<div class="navbar">
  <ul class="nav-primary">… upper_items …</ul>
  {% if lower_items %}
  <ul class="nav-secondary">… lower_items …</ul>
  {% endif %}
</div>
```

Активный пункт получает класс `active`. Navbar зафиксирован сверху; у `body` в CSS задан `padding-top`, чтобы контент не прятался под меню.

## Тесты

`bin/primitives/navbar/test_navbar_builder.py` — сборка по дереву `src/`: состав рядов, `current`, различие URL при `web=True/False`, отсутствие нижней полосы на Home.
