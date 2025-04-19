# Fourward Programming Language

Fourward is a modern programming language designed for simplicity and expressiveness. This repository contains the interpreter implementation and related documentation.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features
- Simple and expressive syntax
- Advanced control structures (if-else, while loops)
- Variable declarations with let
- Print and input functions
- Function support
- Comments support
- Robust error handling

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

2. The interpreter has no external dependencies, so no additional installation is required.

3. Verify installation:
   ```bash
   python fourward_interpreter.py --version
   ```

## Getting Started

### Running the Interpreter
1. Interactive Mode:
   ```bash
   python fourward_interpreter.py
   ```

2. Execute a File:
   ```bash
   python3 fourward_interpreter.py path/to/your/file.fwd
   ```

### Basic Syntax Example
```fourward
# Variable declaration
let x = 10;
let y = "Hello, World!";

# Control structures
if (x > 5) {
    print(y);
} else {
    print("x is too small");
}

# While loop
let count = 0;
while (count < 5) {
    print(count);
    count = count + 1;
}

# Function definition
function greet(name) {
    return "Hello, " + name;
}

print(greet("Fourward"));
```

## Documentation
- [Language Evolution](docs/language_evolution.md)
- [Project Development Plan](docs/project_development_plan.md)
- [Translator Architecture](docs/translator_architecture.md)
- [Development Environment](docs/development_environment.md)
- [Test Plan](docs/test_plan.md)
- [Conclusions](docs/conclusions.md)

## Examples
Check out the `examples.fwd` file for more comprehensive examples of the language features.

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For questions or support, please contact [your-email@example.com]