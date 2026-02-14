# CI/CD Setup for PyPI Publishing

This document describes the CI/CD setup for automatically publishing the pysqoop package to PyPI using GitHub Actions and PyPI Trusted Publishing.

## Overview

The CI/CD pipeline consists of four main workflows:

1. **Testing Workflow** (`.github/workflows/test.yml`) - Runs on every push and PR
2. **Release Workflow** (`.github/workflows/release.yml`) - Automatic version bumping and release creation
3. **Publishing Workflow** (`.github/workflows/publish.yml`) - Runs on releases and publishes to PyPI
4. **Modern Package Configuration** (`pyproject.toml`) - Replaces traditional setup.py with semantic versioning

## Testing Workflow

### Triggers
- Push to `main`, `master`, or `develop` branches
- Pull requests to these branches
- Manual workflow dispatch

### Features
- **Multi-OS Testing**: Ubuntu, Windows, macOS
- **Python Version Matrix**: 3.7 through 3.12
- **Optimized Matrix**: Excludes older Python versions on Windows/macOS for efficiency
- **Comprehensive Testing**:
  - Unit tests with pytest
  - Package import verification
  - Basic functionality tests
  - Package building and installation tests
- **Code Quality Checks**:
  - Linting with flake8
  - Code formatting with black
  - Import sorting with isort
- **Security Scanning**:
  - Static analysis with bandit
  - Vulnerability checking with safety
  - Security report artifacts

## Release Workflow (Automatic Version Bumping)

### 🤖 **Semantic Versioning with Conventional Commits**

The release workflow uses **python-semantic-release** to automatically:
- Analyze commit messages using conventional commit format
- Determine the next version based on changes (patch, minor, major)
- Update version in `__init__.py` and create git tags
- Generate changelog entries
- Create GitHub releases
- Trigger PyPI publishing

### **Conventional Commit Format**

Use these prefixes in your commit messages for automatic version bumping:

- **`feat:`** - New features (triggers **minor** version bump: 0.1.0 → 0.2.0)
- **`fix:`** - Bug fixes (triggers **patch** version bump: 0.1.0 → 0.1.1)
- **`perf:`** - Performance improvements (triggers **patch** version bump)
- **`BREAKING CHANGE:`** or **`feat!:`** - Breaking changes (triggers **major** version bump: 0.1.0 → 1.0.0)

Other prefixes (no version bump):
- **`docs:`** - Documentation changes
- **`style:`** - Code style changes
- **`refactor:`** - Code refactoring
- **`test:`** - Adding tests
- **`chore:`** - Maintenance tasks
- **`ci:`** - CI/CD changes

### **Example Commit Messages**

```bash
feat: add support for Hive partitioning
fix: resolve connection timeout issues
perf: optimize sqoop command generation
feat!: redesign API for better usability
docs: update installation instructions
```

### **Triggers**
- **Automatic**: Push to `master` or `main` branch
- **Manual**: Workflow dispatch for testing

### **Release Process**

1. **Commit Analysis**: Scans commits since last release
2. **Version Calculation**: Determines next version based on conventional commits
3. **Version Update**: Updates `pysqoop/__init__.py` with new version
4. **Git Operations**: Creates commit and tag for new version
5. **GitHub Release**: Creates release with auto-generated changelog
6. **PyPI Trigger**: Automatically triggers PyPI publishing workflow

## Publishing Workflow

### PyPI Trusted Publishing

This setup uses **PyPI Trusted Publishing**, which is the modern, secure way to publish packages without API tokens:

- **No API tokens required** - Uses OpenID Connect (OIDC) for authentication
- **Enhanced security** - Temporary tokens scoped to specific releases
- **Automatic verification** - PyPI verifies the publisher's identity

### Publishing Triggers

1. **Automatic Publishing**: When a GitHub release is published
2. **Manual Publishing**: Workflow dispatch with option to publish to Test PyPI
3. **Test PyPI**: Automatic publishing to Test PyPI on pushes to master (optional)

### Publishing Process

1. **Build Stage**: Creates source and wheel distributions
2. **Verification**: Validates packages with twine
3. **Artifact Upload**: Stores distributions for publishing jobs
4. **Publishing**: Uses official PyPI publish action with trusted publishing

## Setup Instructions

### 1. Enable Trusted Publishing on PyPI

1. Go to your PyPI project settings: https://pypi.org/manage/project/pysqoop/settings/
2. Navigate to "Publishing" section
3. Add a new trusted publisher with these details:
   - **Owner**: `lucafon` (or your GitHub username)
   - **Repository name**: `pysqoop`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

### 2. Configure GitHub Repository

1. Create a new environment in your GitHub repository:
   - Go to Settings → Environments
   - Create environment named `pypi`
   - Optional: Add protection rules (require reviewers, etc.)

2. For Test PyPI (optional):
   - Create environment named `testpypi`
   - Set up trusted publishing on Test PyPI as well

### 3. Modern Package Configuration

The new `pyproject.toml` provides:

- **Modern build system** using setuptools ≥61.0
- **Comprehensive metadata** including keywords, classifiers, URLs
- **Development dependencies** for testing and code quality
- **Tool configurations** for black, isort, flake8, and bandit
- **Version bump** to 0.0.17 (from 0.0.16)

## Usage

### Automatic Release Process

The new automated workflow eliminates manual version management:

1. **Make your changes** following conventional commit format
2. **Commit with proper prefix**:
   ```bash
   git commit -m "feat: add new sqoop export functionality"
   git commit -m "fix: resolve connection pooling issue"
   ```
3. **Push to master/main branch**:
   ```bash
   git push origin master
   ```
4. **Automatic workflow** will:
   - Analyze commits and determine version bump
   - Update version in code
   - Create git tag and GitHub release
   - Publish to PyPI automatically

### Manual Release (Legacy Method)

For manual control, you can still:

1. **Update version** in `pysqoop/__init__.py`
2. **Create and push a git tag**:
   ```bash
   git tag v0.0.18
   git push origin v0.0.18
   ```
3. **Create a GitHub release** from the tag
4. **Automatic publishing** will start once the release is published

### Manual Publishing

1. Go to GitHub Actions → "Publish to PyPI"
2. Click "Run workflow"
3. Choose whether to publish to Test PyPI or production PyPI

### Testing Before Release

1. **Run tests locally**:
   ```bash
   cd unittests
   python -m pytest unitary_tests.py -v
   ```

2. **Test publishing to Test PyPI**:
   - Use workflow dispatch with "test_pypi" option enabled
   - Install from Test PyPI to verify: `pip install -i https://test.pypi.org/simple/ pysqoop`

## Security Considerations

- **No API tokens** stored in GitHub secrets
- **OIDC authentication** provides temporary, scoped access
- **Environment protection** can require manual approval for production releases
- **Security scanning** integrated into testing workflow
- **Artifact verification** ensures package integrity

## Monitoring and Troubleshooting

- **GitHub Actions logs** provide detailed build and publish information
- **PyPI project page** shows publication history and statistics
- **Security reports** are uploaded as workflow artifacts
- **Test results** are available in the Actions tab

## Benefits of This Setup

1. **Security**: No long-lived API tokens, OIDC-based authentication
2. **Automation**: Seamless publishing on releases
3. **Quality**: Comprehensive testing and code quality checks
4. **Compatibility**: Multi-OS and multi-Python version testing
5. **Monitoring**: Detailed logs and security reporting
6. **Flexibility**: Support for both production and test publishing
7. **Modern**: Uses current Python packaging best practices

## Migration Notes

- The existing `setup.py` can coexist with `pyproject.toml`
- `pyproject.toml` takes precedence for modern build tools
- All existing functionality is preserved
- Version has been incremented to 0.0.17 to mark the modernization