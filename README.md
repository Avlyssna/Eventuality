# Eventuality
Eventually, your events become eventful, and you need an easy way to manage them. That's where Eventuality comes in. We give you natural syntax like `+=` and `-=` for managing callbacks, we give you easy callback subscription through dictionaries and lists, we give you type-checking for callbacks, and we would give you the world in callbacks if we could.

## Installation
PyPI makes everything so easy these days. Installation can be done through a single, simple command:

```bash
pip install eventuality
```

## Example Usage
This example uses the dynamic addition of events, and is typically not recommended if you know the callbacks in advance. If the callbacks are known, the dictionary argument type is preferred.

```python
handler = EventHandler(['on_event'])
handler.on_event += print

handler.on_event('An event happened')
# Output: An event happened

# The `print` callback won't be called at all in this case, since it has
# been removed.
handler.on_event -= print
handler.on_event()
```
This example uses the dynamic addition of events, but simply in list form.

```python
def print_politely(string):
	print(f'{string}, and I just wanted to let you know')

handler = EventHandler(['on_event'])
handler.on_event += [print, print_politely]

handler.on_event('An event happened')
# Output: An event happened
# Output: An event happened, and I just wanted to let you know
```

This example uses the forward-knowledge of callbacks to elegantly describe the event. This is the preferred way of creating event handlers.

```python
def print_politely(string):
	print(f'{string}, and I just wanted to let you know')

handler = EventHandler({
	'on_event': [print, print_politely]
})

handler.on_event('An event happened')
# Output: An event happened
# Output: An event happened, and I just wanted to let you know
```

