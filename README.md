# Fourward Programming Language

Fourward is a modern, Python-inspired programming language designed for simplicity and expressiveness. This repository contains the interpreter implementation and related documentation.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features
- Python-like syntax for familiarity
- Advanced control structures
- Robust error handling
- Standard library support
- Interactive REPL mode
- File-based execution

## Installation

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fourward.git
   cd fourward
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python omlang_interpreter.py --version
   ```

## Getting Started

### Running the Interpreter
1. Interactive Mode:
   ```bash
   python omlang_interpreter.py
   ```

2. Execute a File:
   ```bash
   python omlang_interpreter.py path/to/your/file.oml
   ```

### Basic Syntax Example
```python
# Variable declaration
x = 10
y = "Hello, World!"

# Control structures
if x > 5:
    print(y)
else:
    print("x is too small")

# Functions
def greet(name):
    return "Hello, " + name

print(greet("Fourward"))
```

## Documentation
- [Language Whitepaper](Programming Language White Paper- Fourward.docx)
- [Language Tutorial](Programming Language Documentation- Fourward.docx)
- [Language Reference Manual](Programming Language Specification Document - Fourward.docx)
- [Project Development Plan](project_development_plan.txt)
- [Language Evolution](language_evolution.txt)
- [Translator Architecture](translator_architecture.txt)
- [Development Environment](development_environment.txt)
- [Test Plan](test_plan.txt)
- [Conclusions](conclusions.txt)

## Examples
Check out the `examples.oml` file for more comprehensive examples of the language features.

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Team Members
- [Team Member 1 Name] - Role
- [Team Member 2 Name] - Role
- [Team Member 3 Name] - Role
- [Team Member 4 Name] - Role

## Contact
For questions or support, please contact [your-email@example.com]