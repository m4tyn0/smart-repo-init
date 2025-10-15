# CodeRabbit CLI Workflow Guide

## 🐰 What is CodeRabbit?

CodeRabbit is an AI-powered code review tool that provides intelligent, context-aware feedback on your code changes. It integrates seamlessly with Git to review your commits locally before they reach your repository.

## 🔄 The Complete Workflow

### 1. Initial Setup (One-time)

```bash
# Install CodeRabbit CLI
curl -fsSL https://cli.coderabbit.ai/install.sh | sh

# Configure (interactive setup)
coderabbit configure

# Verify installation
coderabbit --version
```

### 2. Daily Development Cycle

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. Edit Code                                          │
│     └─ Make your changes in any editor                 │
│                                                         │
│  2. Stage Changes                                      │
│     └─ git add file.py                                 │
│     └─ git add .                                       │
│                                                         │
│  3. Commit (this triggers the review)                  │
│     └─ git commit -m "Add feature X"                   │
│                                                         │
│     ┌─────────────────────────────────────┐           │
│     │  Pre-commit Hook Runs               │           │
│     │  ├─ Detects staged files            │           │
│     │  ├─ Sends to CodeRabbit CLI         │           │
│     │  └─ Waits for review results        │           │
│     └─────────────────────────────────────┘           │
│                      │                                  │
│           ┌──────────┴──────────┐                      │
│           ▼                     ▼                       │
│     ✅ Review Passes      ❌ Issues Found               │
│     Commit proceeds       Commit blocked                │
│                           └─ Read feedback              │
│                           └─ Fix issues                 │
│                           └─ Stage & try again          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3. Review Outcome Examples

#### ✅ Successful Review

```bash
$ git commit -m "Add user validation"

🐰 Running CodeRabbit CLI review on staged changes...
Reviewing files:
  - src/user.py
  - tests/test_user.py

✓ Code quality: Excellent
✓ No security issues found
✓ Performance looks good
✓ Tests cover new functionality

✅ CodeRabbit review passed! Proceeding with commit...
[main a1b2c3d] Add user validation
 2 files changed, 45 insertions(+)
```

#### ❌ Review with Issues

```bash
$ git commit -m "Add database connection"

🐰 Running CodeRabbit CLI review on staged changes...
Reviewing files:
  - src/database.py

⚠️  Issues found:

src/database.py:15
  Potential SQL injection vulnerability
  Recommendation: Use parameterized queries instead of string formatting
  
src/database.py:23
  Database connection not properly closed
  Recommendation: Use context manager or ensure connection.close() in finally block

src/database.py:8
  Hardcoded credentials detected
  Recommendation: Use environment variables for sensitive data

❌ CodeRabbit review found issues!

Please review the suggestions above and:
  1. Fix the issues and stage your changes again, or
  2. Skip this check with: git commit --no-verify
```

## 🎯 What CodeRabbit Checks

### Code Quality
- **Style issues**: PEP 8 violations, naming conventions
- **Complexity**: Overly complex functions, deep nesting
- **Duplication**: Repeated code patterns
- **Documentation**: Missing or inadequate docstrings

### Security
- **Vulnerabilities**: SQL injection, XSS, command injection
- **Secrets**: Hardcoded passwords, API keys, tokens
- **Dependencies**: Known vulnerabilities in packages
- **Input validation**: Missing or weak validation

### Best Practices
- **Error handling**: Try-catch blocks, error messages
- **Resource management**: File handles, connections, memory
- **Type safety**: Type hints, type checking
- **Testing**: Test coverage, edge cases

### Performance
- **Inefficient algorithms**: O(n²) when O(n) is possible
- **Database queries**: N+1 queries, missing indexes
- **Memory usage**: Large allocations, memory leaks
- **Caching**: Missing caching opportunities

## ⚙️ Configuration Options

### Basic `.coderabbit.yaml`

```yaml
language: en
reviews:
  auto_review: true
  request_changes_workflow: true
```

### Advanced Configuration

```yaml
language: en
early_access: true

reviews:
  # Enable automatic reviews
  auto_review: true
  
  # Request changes workflow
  request_changes_workflow: true
  
  # Include high-level summary
  high_level_summary: true
  
  # Show review status
  review_status: true
  
  # Custom instructions for reviews
  instructions: |
    - Focus on Python best practices and PEP 8
    - Pay special attention to security in authentication code
    - Ensure all functions have type hints
    - Check for proper error handling
    - Verify test coverage for new features
  
  # Path-specific instructions
  path_instructions:
    - path: "src/api/**"
      instructions: |
        - Check for proper API versioning
        - Ensure rate limiting is implemented
        - Verify authentication on all endpoints
    
    - path: "tests/**"
      instructions: |
        - Ensure tests are independent
        - Check for proper test isolation
        - Verify edge cases are covered

# Chat configuration (for interactive use)
chat:
  auto_reply: true

# Enable additional tools
tools:
  # Shell script analysis
  shellcheck:
    enabled: true
  
  # GitHub Actions validation
  actionlint:
    enabled: true
```

## 🚫 Bypassing the Hook (When Necessary)

Sometimes you need to commit without review (rarely recommended):

```bash
# Skip the pre-commit hook
git commit --no-verify -m "WIP: experimental feature"

# Alternative short form
git commit -n -m "Quick fix"
```

**When is it okay to skip?**
- ✅ Work-in-progress commits on a feature branch
- ✅ Reverting a problematic commit quickly
- ✅ Documentation-only changes (though review can still help)
- ❌ Production code (always review!)
- ❌ Security-sensitive code (never skip!)

## 🔧 Troubleshooting

### Hook Not Running

```bash
# Check if hook exists and is executable
ls -la .git/hooks/pre-commit

# Make it executable if needed
chmod +x .git/hooks/pre-commit

# Check if hooks are disabled
git config --get core.hooksPath
```

### CodeRabbit Not Found

```bash
# Check installation
which coderabbit

# Reinstall if needed
curl -fsSL https://cli.coderabbit.ai/install.sh | sh

# Add to PATH (if not automatic)
export PATH="$HOME/.coderabbit/bin:$PATH"
```

### Review Takes Too Long

```bash
# Review specific files only
git diff --cached --name-only | grep ".py$" | xargs coderabbit review

# Skip certain paths in .coderabbit.yaml
reviews:
  path_filters:
    exclude:
      - "vendor/**"
      - "node_modules/**"
      - "*.min.js"
```

## 💡 Pro Tips

### 1. Incremental Commits
Make smaller, focused commits. CodeRabbit reviews faster and provides more relevant feedback.

```bash
# Good: Focused commits
git add src/auth.py tests/test_auth.py
git commit -m "Add password validation"

git add src/database.py
git commit -m "Add connection pooling"

# Less ideal: Large commits
git add .
git commit -m "Add all features"
```

### 2. Learn from Reviews
CodeRabbit provides educational feedback. Read the explanations to improve your coding skills.

### 3. Customize for Your Project
Tailor `.coderabbit.yaml` to your project's specific needs and coding standards.

### 4. Use with Pull Requests
CodeRabbit can also review GitHub/GitLab pull requests automatically:

```yaml
# In .coderabbit.yaml
reviews:
  # Enable PR reviews
  pull_requests: true
  
  # Auto-approve if no issues
  auto_approve: true
```

### 5. Team Standards
Commit your `.coderabbit.yaml` to the repository so the entire team uses the same review standards.

## 📊 Review Quality Levels

CodeRabbit assigns quality levels to your code:

- 🌟 **Excellent**: No issues, follows best practices
- ✅ **Good**: Minor suggestions, generally solid
- ⚠️  **Needs Improvement**: Several issues to address
- 🚨 **Critical Issues**: Security or major bugs found

## 🔄 Integration with GitHub/GitLab

CodeRabbit can also review pull requests automatically:

1. **Connect Repository**: Link your GitHub/GitLab account
2. **Automatic PR Reviews**: CodeRabbit comments on every PR
3. **Interactive Chat**: Reply to comments to ask for clarification
4. **Incremental Reviews**: Reviews new changes in updated PRs

## 📚 Additional Resources

- **Official Docs**: https://www.coderabbit.ai/docs
- **CLI Guide**: https://www.coderabbit.ai/docs/cli
- **Configuration Reference**: https://www.coderabbit.ai/docs/configuration
- **Community**: https://discord.gg/coderabbit

## 🎓 Learning Path

1. **Week 1**: Use default settings, get familiar with feedback
2. **Week 2**: Start customizing `.coderabbit.yaml` for your needs
3. **Week 3**: Add path-specific instructions
4. **Week 4**: Fine-tune review instructions based on your team's standards

## 🤝 Best Practices Summary

✅ **DO:**
- Read all review feedback carefully
- Fix issues before committing
- Customize configuration for your project
- Use descriptive commit messages
- Make focused, incremental commits

❌ **DON'T:**
- Habitually use `--no-verify`
- Ignore security warnings
- Make huge commits
- Skip reviews for production code
- Forget to update `.coderabbit.yaml` as project evolves
