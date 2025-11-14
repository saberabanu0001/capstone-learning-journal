# well, now I'm planning to use LLAVA with LLAMA cpp.

## But here are the clarification of the things -

## 🧠 How LLaVA and llama.cpp are connected

### 👉 1. LLaVA is a MODEL

- It is NOT a program.
- It is NOT software.
- It is NOT a repository that runs by itself.

- - LLaVA = a trained vision-language model
- - (Weights + training recipe)



### 👉 2. llama.cpp is a PROGRAM (engine)

- llama.cpp is software written in C++ that can run certain models.

- It is like a car engine that can run different “model files.”

- Models = fuel
- llama.cpp = engine



👉 3. To run LLaVA inside llama.cpp, you need the LLaVA model converted to GGUF format

That means:

LLaVA model (original) → converted to → .gguf file → run with llama.cpp


So:
✔ You use llama.cpp as your runner
✔ You use LLaVA GGUF as your model
✔ Together = LLaVA running in C++