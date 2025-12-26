# Contributing to Automated Architecture Discovery System

Thank you for your interest in contributing! This document provides guidelines for contributing to this educational/demo project.

## 🎯 Project Purpose

Before contributing, please understand that this is:
- ✅ An **educational/demonstration project**
- ✅ A **portfolio showcase** project
- ✅ A **proof-of-concept** for architecture discovery
- ❌ **NOT intended for production use** without significant modifications

## 🤝 How to Contribute

### Types of Contributions Welcome

1. **Bug Reports** 🐛
   - Issues with running the demo
   - Documentation errors
   - Broken links or missing files

2. **Documentation Improvements** 📚
   - Clearer explanations
   - Additional examples
   - Tutorial enhancements
   - Typo fixes

3. **Educational Enhancements** 🎓
   - Better code comments
   - Additional demo scenarios
   - Learning resources
   - Architecture pattern examples

4. **Feature Suggestions** 💡
   - New analysis capabilities
   - Better visualizations
   - Additional metrics
   - Enhanced reporting

### Types of Contributions NOT Accepted

- ❌ Production-hardening features (beyond scope)
- ❌ Enterprise-specific customizations
- ❌ Security audit services (out of scope)
- ❌ Performance optimization for scale (demo project)

## 📋 Contribution Process

### 1. Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/automated-architecture-discovery.git
cd automated-architecture-discovery
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code improvements

### 3. Make Your Changes

- Write clear, commented code
- Follow existing code style
- Test your changes locally
- Update documentation if needed

### 4. Test Your Changes

```bash
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test your changes
python master_orchestrator.py
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Brief description of your changes"
```

Commit message guidelines:
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issue numbers if applicable

### 6. Push to GitHub

```bash
git push origin feature/your-feature-name
```

### 7. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Fill out the PR template
4. Wait for review

## 📝 Pull Request Guidelines

### PR Title Format

- `[Feature] Add new diagram type`
- `[Fix] Correct correlation ID tracking`
- `[Docs] Update installation guide`
- `[Refactor] Improve service discovery logic`

### PR Description Should Include

- **What**: What does this PR do?
- **Why**: Why is this change needed?
- **How**: How does it work?
- **Testing**: How did you test it?
- **Screenshots**: If visual changes

Example:
```markdown
## What
Adds support for detecting circular dependencies in the architecture

## Why
Users wanted to identify potential design issues early

## How
- Implemented graph cycle detection algorithm
- Added warnings to the generated report
- Updated diagram generator to highlight cycles

## Testing
- Tested with sample circular dependency
- Verified warning appears in output
- Checked diagram rendering

## Screenshots
[Attach screenshot of circular dependency warning]
```

## 💻 Code Style Guidelines

### Python Code Style

Follow PEP 8 with these specific guidelines:

```python
# Good: Clear function names with docstrings
def analyze_service_dependencies(services: List[str]) -> Dict:
    """
    Analyzes dependencies between services.
    
    Args:
        services: List of service names
        
    Returns:
        Dictionary mapping services to their dependencies
    """
    dependencies = {}
    # ... implementation
    return dependencies

# Bad: No docstring, unclear naming
def analyze(s):
    d = {}
    # ... implementation
    return d
```

### Documentation Style

- Use clear, concise language
- Include code examples where helpful
- Add diagrams for complex concepts
- Keep beginners in mind

## 🧪 Testing Requirements

For new features:

1. **Manual Testing**
   - Run the complete system
   - Verify output files are generated
   - Check diagrams render correctly

2. **Edge Cases**
   - Test with missing data
   - Test with invalid inputs
   - Test with empty responses

3. **Documentation**
   - Update relevant README sections
   - Add examples if needed
   - Update API documentation

## 📚 Documentation Updates

When changing code, also update:

- [ ] Relevant README files
- [ ] Code comments
- [ ] Docstrings
- [ ] Examples (if applicable)
- [ ] Architecture diagrams (if structure changes)

## 🐛 Reporting Bugs

### Before Submitting a Bug Report

1. **Search existing issues** - Your bug might already be reported
2. **Try the latest version** - It might be fixed already
3. **Isolate the problem** - Create a minimal reproduction case

### Bug Report Template

```markdown
## Bug Description
[Clear description of what's wrong]

## Steps to Reproduce
1. Run command X
2. Observe error Y
3. Expected behavior Z

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.9.5]
- Installation Method: [pip, manual, etc.]

## Error Messages
```
[Paste full error message here]
```

## Additional Context
[Any other relevant information]
```

## 💡 Suggesting Enhancements

### Enhancement Request Template

```markdown
## Feature Description
[What feature would you like to see?]

## Use Case
[Why would this be useful?]

## Proposed Implementation
[Optional: How might this work?]

## Alternatives Considered
[What other approaches did you think about?]
```

## 🔍 Code Review Process

Pull requests will be reviewed for:

1. **Functionality** - Does it work as intended?
2. **Code Quality** - Is it readable and maintainable?
3. **Documentation** - Is it properly documented?
4. **Testing** - Has it been tested?
5. **Scope** - Is it appropriate for this demo project?

### Review Timeline

- Simple fixes: 3-5 days
- Documentation: 3-5 days
- New features: 5-10 days

## 🎓 Learning & Questions

### Need Help?

- **GitHub Issues** - For project-specific questions
- **Discussions** - For general questions about concepts
- **Documentation** - Start with README and docs/ folder

### Resources

- [Python Documentation](https://docs.python.org/)
- [Microservices Architecture](https://microservices.io/)
- [Mermaid Diagrams](https://mermaid.js.org/)
- [Claude AI](https://www.anthropic.com/claude)

## 📜 Code of Conduct

### Our Standards

- ✅ Be respectful and constructive
- ✅ Welcome newcomers
- ✅ Accept constructive criticism
- ✅ Focus on what's best for learning
- ✅ Show empathy towards others

### Unacceptable Behavior

- ❌ Harassment or discriminatory comments
- ❌ Personal attacks
- ❌ Trolling or insulting comments
- ❌ Public or private harassment
- ❌ Publishing others' private information

## 📄 Legal & Licensing

By contributing, you agree that:

1. Your contributions will be licensed under the MIT License
2. You have the right to contribute this code
3. You understand this is an educational/demo project
4. You've read and agree to the DISCLAIMER.md

## 🙏 Recognition

Contributors will be:
- Listed in the project README
- Credited in release notes
- Appreciated in the community!

## ❓ Questions?

If you have questions about contributing:

1. Check the [README.md](README.md)
2. Review [DISCLAIMER.md](DISCLAIMER.md)
3. Search existing GitHub Issues
4. Open a new issue with your question

---

Thank you for helping make this educational project better! 🎉

**Remember**: This is a learning project. Your contributions help others learn too!