# meTTa_Training

**Set Up:**

Method 1:

**Set Up the Virtual Environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```
   ```sh
   pip install -r requirements.txt
   ```

Method 2:

**Set up Docker**:
```sh
docker build -t metta-app .
docker run -it --rm -v ${PWD}:/app metta-app
```

3. **Links**:
   
1) https://metta-lang.dev/docs/learn/tutorials/eval_intro/main_concepts.html
2) https://metta-lang.dev/docs/learn/tutorials/ground_up/query_knowledge.html
3) https://metta-lang.dev/docs/learn/tutorials/python_use/intro.html
4) https://github.com/trueagi-io/hyperon-experimental/blob/main/python/hyperon/atoms.py#L10




