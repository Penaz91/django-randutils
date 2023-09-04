Django-RandUtils
================

A small and assorted collection of utilities and Views for Django.

Rationale
---------

In my work, I often find myself recycling pieces of other things I developed over time. So I decided to just take them, pull them out and make them a little bit better.

Content
-------

### Middlewares

- **HtmlWrapperMiddleware:** Allows any kind of response to be wrapper into an HTML. This allows to analyze other types of response objects (like `JSONResponse`) with [Django Debug Toolbar](https://github.com/jazzband/django-debug-toolbar).

### Views

- **SearchListView:** A subclass of Django's ListView that allows for searching via GET parameters.

### Testing

- **AdminTestCase:** A testcase that automatically finds all admin urls and builds tests for changelist viewing and searching. **Requires [parameterized](https://pypi.org/project/parameterized/)
