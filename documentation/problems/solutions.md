
### Problems and solutions


## Number 1:

~~~bash
_tkinter.TclError: image "pyimage3" doesn't exist
~~~

**Description:**

This error occured when I tried to add a background image to the buttons.



**Solution:**
https://stackoverflow.com/questions/20251161/tkinter-tclerror-image-pyimage3-doesnt-exist

In ChessWindow.py, I changed the line...
~~~python
wlcm_scrn = tkinter.Tk()
~~~
to this...
~~~python
wlcm_scrn = tkinter.Toplevel()
~~~