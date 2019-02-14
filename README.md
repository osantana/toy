# Toy Web Framework

A Simple, basic and not suitable for production usage Web Framework

## Requirements

 * Python 3.7+

## Improvement Points / TODO

- Documentation!
- Create ResourceList class and use it at ResourceListField.
- Refactor Processor / Error handling.
- Support for JSON-Patch (RFC6902).
- Fix intermitent failures related with sqlalchemy sessions during test
  running.
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

## License

MIT License

Copyright (c) 2019 Osvaldo Santana Neto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
