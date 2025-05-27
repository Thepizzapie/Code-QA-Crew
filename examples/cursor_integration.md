# Cursor AI Integration - Code QA Validation

## Code Validation Protocol

Before completing any code task, run QA analysis and validate results.

### Required Commands

#### Code Analysis Only
```bash
python qa_cli.py --path [PROJECT_FOLDER]
```

#### Code + Localhost Check  
```bash
python qa_cli.py --path [PROJECT_FOLDER] --port [PORT]
```

#### Quick Analysis (Development)
```bash
python qa_cli.py --path [PROJECT_FOLDER] --quick
```

#### Localhost Only Check
```bash
python qa_cli.py --localhost-only --port [PORT]
```

### Success Conditions (All Must Pass)

- **Security Score ≥ 7/10** 
- **Python Quality Score ≥ 7/10**
- **Overall QA Score ≥ 7/10**
- **No High Risk security issues**
- **No syntax errors**
- **Report shows "No critical issues"**

### Failure Conditions (Must Fix Before Completion)

- **Security score < 5/10** = CRITICAL - MUST FIX
- **Python quality score < 7/10** = MUST FIX  
- **Any High Risk security issues** = IMMEDIATE FIX REQUIRED
- **Syntax errors present** = MUST FIX
- **Localhost not accessible when expected** = INVESTIGATE

### Common Issues & Fixes

#### High Risk Security Issues
- **eval() usage** → Replace with safer alternatives
- **exec() usage** → Use specific function calls
- **Shell injection** → Use subprocess with shell=False
- **SQL injection** → Use parameterized queries

#### Medium Risk Issues  
- **Pickle usage** → Use JSON or safer serialization
- **Subprocess calls** → Validate inputs, use shell=False
- **Hardcoded secrets** → Move to environment variables

#### Quality Issues
- **Long lines** → Break into multiple lines (< 120 chars)
- **Print statements** → Replace with logging
- **Missing documentation** → Add docstrings and comments
- **No error handling** → Add try/catch blocks

### Workflow Integration

#### Pre-Development
```bash
# Understand current state
python qa_cli.py --path . --quick
```

#### During Development  
```bash
# Quick checkpoint
python qa_cli.py --path ./src --type python
```

#### Pre-Commit
```bash
# Full validation
python qa_cli.py --path . --port 3000
```

#### Production Ready
```bash
# Comprehensive check
python qa_cli.py --path . --type mixed
```

### Score Interpretation

| Score | Status | Action Required |
|-------|--------|----------------|
| 10/10 | Excellent | Ready for production |
| 8-9/10 | Good | Minor improvements optional |
| 6-7/10 | Fair | Address issues before production |
| 4-5/10 | Poor | Significant fixes required |
| 1-3/10 | Critical | Major refactoring needed |

### Example Validation Flow

1. **Run Analysis**:
   ```bash
   python qa_cli.py --path ./my-project --port 3000
   ```

2. **Check Report**: Look for generated `demo_qa_report_*.md`

3. **Validate Scores**:
   - Security: 8/10
   - Python Quality: 9/10  
   - Overall QA: 7/10
   - No High Risk issues

4. **Fix Any Issues**: Address medium/low risk items

5. **Re-run Validation**: Confirm improvements

6. **Complete Task**: Only after all conditions met

### Critical Rules

1. **NEVER skip QA validation**
2. **ALWAYS fix High Risk security issues**  
3. **MUST achieve minimum scores before completion**
4. **DOCUMENT any unfixable issues with justification**
5. **RE-RUN analysis after making fixes**

### Report Integration

Include QA summary in your completion message:
```
QA VALIDATION COMPLETE
- Security Score: 8/10
- Python Quality: 9/10  
- Overall QA: 7/10
- Issues Fixed: 3 medium risk items
- Status: READY FOR PRODUCTION
```

This validation ensures professional code quality and security standards are maintained in all AI-generated code. 