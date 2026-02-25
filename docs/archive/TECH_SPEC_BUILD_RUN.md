# Technical Specification: Building and Running Components for Manual Testing

This document describes how to build and run the various components of the WALLY-CLEAN project for manual testing. It covers C/C++ binaries, Python scripts, and the React-based web UI.

---

## 1. Prerequisites

- **C Compiler:** GCC (tested on macOS)
- **Python:** 3.12+ (with `venv` and dependencies from `requirements.txt`)
- **Node.js & npm:** For React UI (Node.js 18+ recommended)

---

## 2. Building C/C++ Components

### a. Build All Binaries
```sh
make build-all
```
- Builds all C/C++ executables and shared libraries into `bin/`.

### b. Build Individual Components
- **Linked List Driver:**
  ```sh
  make
  ```
- **Simple DB Shared Library:**
  ```sh
  make libsimpledb.dylib
  ```
- **Simple DB Test Executable:**
  ```sh
  make build-db
  ```

### c. Clean Build Artifacts
```sh
make clean
```

---

## 3. Running C/C++ Binaries

- **Linked List Driver:**
  ```sh
  make run
  ```
- **Run Tests:**
  ```sh
  make run-test
  ```
- **Animated Demo:**
  ```sh
  make run-demo
  ```
- **Doubly Linked List Driver:**
  ```sh
  make run-doubly
  ```
- **Circular Linked List Driver:**
  ```sh
  make run-circular
  ```
- **Array Pointer Demo:**
  ```sh
  make run-array-demo
  ```
- **Struct Memory Demo:**
  ```sh
  make run-struct-demo
  ```
- **Simple DB Test:**
  ```sh
  make run-db-test
  ```

---

## 4. Python Components

### a. Setup Python Environment
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### b. Run Python Scripts
- **Graph Database Demo:**
  ```sh
  make run-graph-db
  # or
  python3 graph_db.py
  ```
- **Graph Examples:**
  ```sh
  make run-graph-examples
  # or
  python3 graph_examples.py
  ```
- **Web UI Backend:**
  ```sh
  make run-web-ui
  # or
  python3 graph_web_ui.py
  # Access at http://127.0.0.1:5000
  ```

---

## 5. React Web UI (graph-ui)

### a. Install Dependencies
```sh
cd graph-ui
npm install
```

### b. Run Development Server
```sh
npm run dev
# Access at http://localhost:5173
```

---

## 6. Manual Testing Checklist
- Build all C/C++ binaries and shared libraries.
- Run each C/C++ executable and verify output.
- Set up Python environment and run all Python scripts.
- Start the React UI and verify it loads in the browser.
- Test integration between backend (Python) and frontend (React UI).

---

## 7. Troubleshooting
- Ensure all dependencies are installed for each language.
- Use `make clean` to reset C/C++ builds if you encounter issues.
- Check for port conflicts (default: 5000 for backend, 5173 for frontend).
- Review logs/output for errors and consult relevant README files.

---

## 8. References
- See `README.md` and other `*_GUIDE.md` files for more details on each component.
