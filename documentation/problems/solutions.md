[//]: # ()
[//]: # (# Problems and solutions)

[//]: # ()
[//]: # ()
[//]: # (## Number 1:)

[//]: # ()
[//]: # (~~~bash)

[//]: # (_tkinter.TclError: image "pyimage3" doesn't exist)

[//]: # (~~~)

[//]: # ()
[//]: # (### **Description:**)

[//]: # ()
[//]: # (This error occured when I tried to add a background image to the buttons.)

[//]: # ()
[//]: # ()
[//]: # (### **Solution:**)

[//]: # ()
[//]: # (https://stackoverflow.com/questions/20251161/tkinter-tclerror-image-pyimage3-doesnt-exist)

[//]: # ()
[//]: # (In ChessWindow.py, I changed the line...)

[//]: # (~~~python)

[//]: # (wlcm_scrn = tkinter.Tk&#40;&#41;)

[//]: # (~~~)

[//]: # (to this...)

[//]: # (~~~python)

[//]: # (wlcm_scrn = tkinter.Toplevel&#40;&#41;)

[//]: # (~~~)

[//]: # ()
[//]: # ()
[//]: # (## Number 2:)

[//]: # ()
[//]: # (### **Description:**)

[//]: # ()
[//]: # (![img.png]&#40;img.png&#41;)

[//]: # ()
[//]: # (~~~bash)

[//]: # (File "C:\Users\balaz\Desktop\pychess\chess-py\src\controller\ViewController.py", line 4, in <module>)

[//]: # (    from src.view.ChessWindow import ChessWindow)

[//]: # (ImportError: cannot import name 'ChessWindow' from partially initialized module 'src.view.ChessWindow' &#40;most likely due to a circular import&#41; &#40;C:\Users\balaz\Desktop\pychess\chess-py\src\view\ChessWindow.py&#41;)

[//]: # (~~~)

[//]: # ()
[//]: # (### **Solution:**)

[//]: # ()
[//]: # (I had to change the import statement in ViewController.py from this...)

[//]: # (~~~python)

[//]: # (from src.view.ChessWindow import ChessWindow)

[//]: # (~~~)

[//]: # (to this...)

[//]: # (```python)

[//]: # (import src.view.ChessWindow as ChessWindow)

[//]: # (```)

[//]: # (### But then it is necessary to change the type hinting:)

[//]: # ()
[//]: # (```python)

[//]: # (def __init__&#40;self, chess_window: ChessWindow.ChessWindow, white_player_name: str, black_player_name: str&#41;:)

[//]: # (    self._chess_gui: ChessWindow.ChessWindow = chess_window)

[//]: # (```)

[//]: # ()
[//]: # ()
[//]: # (## Number 3:)

[//]: # ()
[//]: # (### **Description:**)

[//]: # ()
[//]: # (Running test from command line with the following command:)

[//]: # (![img_1.png]&#40;img_1.png&#41;)

[//]: # (Have to be in the root directory of the project to run the tests.)

[//]: # (```)

[//]: # (python -m unittest .\tests\test_model\TestBishop.py)

[//]: # (```)

[//]: # ()
[//]: # ()
[//]: # (## Number 4:)

[//]: # ()
[//]: # (### Generating uml diagrams)

[//]: # ()
[//]: # (To generate UML diagrams using `pyreverse` with Graphviz, you need to install Graphviz and ensure it is available in your system's PATH. Here are the steps:)

[//]: # ()
[//]: # (### Plan)

[//]: # (1. Install Graphviz.)

[//]: # (2. Install `pylint` if not already installed.)

[//]: # (3. Use `pyreverse` to generate UML diagrams.)

[//]: # ()
[//]: # (### Steps)

[//]: # ()
[//]: # (1. **Install Graphviz**:)

[//]: # (    - On Windows, download and install Graphviz from the [official website]&#40;https://graphviz.gitlab.io/download/&#41;.)

[//]: # (    - Ensure the Graphviz `bin` directory is added to your system's PATH.)

[//]: # ()
[//]: # (2. **Install `pylint`**:)

[//]: # (    ```sh)

[//]: # (    pip install pylint)

[//]: # (    ```)

[//]: # ()
[//]: # (3. **Generate UML Diagrams**:)

[//]: # (    Navigate to the root directory of your project and run:)

[//]: # (    ```sh)

[//]: # (    pyreverse -o png -p ProjectName .)

[//]: # (    ```)

[//]: # ()
[//]: # (### Example)

[//]: # ()
[//]: # (```sh)

[//]: # (cd ./src)

[//]: # (pyreverse -o png -p ChessGame .)

[//]: # (```)

[//]: # ()
[//]: # ()
[//]: # ()
