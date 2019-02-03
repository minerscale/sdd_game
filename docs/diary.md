## 03/02/2019 - Getting It Rolling

After a few hours of work I have setup the enviroment I am working in. I want to keep the dependencies thin. I think I can manage to only use [Numpy](http://www.numpy.org/). I have a good idea on how my game is supposed to draw to the screen. I have created a 2D array of strings to act as the framebuffer for the game. I have *borrowed* and modified a blit function from [stack overflow](https://stackoverflow.com/).

As for this website's functionality, I have taken care to have all the tools I need for creating the documentation. I have support for:

**1.** Syntax highlighted code blocks:

```python
print('We have python syntax highlighting!') # Comment
```

**2.** Flowcharts:

{% mermaid %}
graph LR
    A[Square Rect] -- Link text --> B((Circle))
    A --> C(Round Rect)
    B --> D{Rhombus}
    C --> D
{% endmermaid %}

**3.** Gantt diagrams:

{% mermaid %}
gantt
    title A Gantt Diagram
    dateFormat  YYYY-MM-DD
    section Section
    A task           :a1, 2014-01-01, 30d
    Another task     :after a1  , 20d
    section Another
    Task in sec      :2014-01-12  , 12d
    another task      : 24d
{% endmermaid %}

**4.** Tables:

 Column 1 | Column 2 | Column 3 |
----------|----------|----------|
 `print('Code inside a table!')`{:.python}   | cell 1b  | cell 1c  |
 cell 2a  | cell 2b  | cell 2c  |
