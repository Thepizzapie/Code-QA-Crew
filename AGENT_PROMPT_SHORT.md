# 🤖 Agent Code Validation Prompt

## **MANDATORY VALIDATION BEFORE CODE COMPLETION**

**CRITICAL**: Before considering ANY code complete, you MUST run:

```bash
python qa_cli.py --path [FOLDER]                # Code analysis only
python qa_cli.py --path [FOLDER] --port [PORT]  # Code + localhost check (when needed)
```

## **VALIDATION PROTOCOL**

### **1. Generate Code** → **2. Run QA** → **3. Fix Issues** → **4. Validate Again**

### **Command Examples:**
```bash
python qa_cli.py --path ./frontend                # React code analysis only
python qa_cli.py --path ./frontend --port 3000    # React apps + demo check
python qa_cli.py --path ./backend --port 8000     # Python APIs + service check
python qa_cli.py --localhost-only --port 3000     # Quick port check only
```

## **FAILURE CONDITIONS - NEVER ACCEPT CODE IF:**
- 🚫 Shows "❌ NOT ACCESSIBLE" for localhost
- 🚫 Security scan reveals HIGH/MEDIUM risks
- 🚫 Python syntax errors detected
- 🚫 Response time > 2000ms

## **SUCCESS CONDITIONS - ONLY ACCEPT CODE IF:**
- ✅ Shows "✅ ACCESSIBLE" for localhost  
- ✅ Security scan shows "No issues detected"
- ✅ All syntax checks pass
- ✅ Response time < 1000ms

## **WORKFLOW:**
1. **Generate code**
2. **Run**: `python qa_cli.py --path [YOUR_FOLDER] --port [YOUR_PORT]`
3. **If issues found**: Fix and re-run validation
4. **If all clear**: Code is acceptable

## **INCLUDE IN RESPONSE:**
```
✅ Code Quality Validation Complete
📊 QA Results: [ACCESSIBLE/Security OK/Performance Good]
```

**NO EXCEPTIONS - This validation is mandatory for all code deliverables.** 