# python-timer
A small tool for timing the execution of any function or code block during running.

## Usage
To time a code block, wrap it with `with Timeit()` like this:
```python
with Timeit():
  for _ in range(1000):
    pass
```

To time a function, use the decorator `@timeit()` like this:
```python
@timeit()
def loop_1000_times():
  for _ in range(1000):
    pass
```
Note that the brackets after timeit are not omittable.

In both cases, you may specify a name for the timer and whether to mute the timer. For example:
```python
with Timeit(name="loop 1000 times", mute=False):
  for _ in range(1000):
    pass
```

When multiple timers are nested together, the outputs will take a form similar to the file tree:
```python
with Timeit(name="outer"):
      with Timeit(name="inner-0"):
          with Timeit(name="inner-0.0"):
              time.sleep(0.1)
          with Timeit(name="inner-0.1"):
              time.sleep(0.2)
      with Timeit(name="inner-1"):
          time.sleep(0.7)
      with Timeit(name="inner-2"):
          with Timeit(name="inner-2.0"):
              time.sleep(0.0001)
          with Timeit(name="inner-2.1"):
              with Timeit(name="inner-2.1.0"):
                  time.sleep(0.0001)
                  with Timeit(name="inner-2.1.0.0"):
                      pass
                  with Timeit(name="inner-2.1.0.1"):
                      pass
```

```
    ┌───inner-0.0: 100.13 ms
    ├───inner-0.1: 200.23 ms
┌───inner-0: 300.49 ms
├───inner-1: 700.74 ms
│   ┌───inner-2.0: 159.66 us
│   │       ┌───inner-2.1.0.0: 0.77 us (mytimeit costs additional 3.02 us)
│   │       ├───inner-2.1.0.1: 0.75 us (mytimeit costs additional 2.56 us)
│   │   ┌───inner-2.1.0: 188.32 us
│   ├───inner-2.1: 202.96 us
├───inner-2: 398.73 us
outer: 1.00 s
```
