# Toy Web Framework

A framework designed For Fun.

## Requirements

 * Python 3.10+

## TODO

- Documentation!
- Create ResourceList class and use it at ResourceListField.
- Refactor Processor / Error handling.
- Support for JSON-Patch (RFC6902).
- Fix errors related with SQLAlchemy on tests
- More fields:
  - datetime field
  - date field
  - time field
  - timedelta field
- Contrib/plugins package with:
  - Database + ResourceModel specialization
- More serializers:
  - xml
  - html/form
- Handle query strings with fields in Handler
- Refactor request/app to use a Context object that wraps both objects
  and things like 'user'
