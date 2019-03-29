#!/usr/bin/python
# -*- coding: utf-8 -*-


class EventHandler:
	'''
		This class handles the multitude of developer-defined events. The
		`events` argument is rather lenient: it can be either a list,
		dictionary, or tuple.

		If `events` is a list or tuple, this class uses the strings therein to
		infer the defined event names. Callbacks to each event can be added or
		removed through the respective `+=` and `-=` operators.

		If `events` is a dictionary, this class will use the dictionary's keys
		as the event names. It will also use the keys' corresponding values -
		which should be either a single callable or a list/tuple of callables -
		to set the callbacks for that event. Note that you can still add or
		remove callbacks for these events at a later time if you would need to.

		Further example usage can be found in the `main` function.
	'''
	def __init__(self, events):
		if isinstance(events, list) or isinstance(events, tuple):
			self._events = dict.fromkeys(events, Event())
		elif isinstance(events, dict):
			for name, item in events.items():
				if callable(item):
					events[name] = Event([item])
				elif isinstance(item, list) or isinstance(item, tuple):
					for callback in item:
						if not callable(callback):
							raise TypeError("Expected 'callable' type for the 'events' argument's sub-values")

					events[name] = Event(item)
				else:
					raise TypeError("Expected 'callable', 'list', or 'tuple' type for the 'events' argument's values")

			self._events = events
		else:
			raise TypeError("Expected 'list', 'dict', or 'tuple' type for the 'events' argument")

	def __getattr__(self, name):
		event = self._events.get(name)

		# We check specifically to see if it's `None`, since an empty callback
		# list would otherwise evaluate as `False`. Obviously, that is undesired
		# behaviour for our internal processing.
		if event != None:
			return event
		else:
			raise AttributeError(f"'{name}' is not defined as an event")

	def __len__(self):
		return len(self._events)


class Event:
	'''
		This class represents each event itself. Provided a list of callbacks,
		you are able to add or remove them through the `+=` and `-=` operators
		respectively.

		Upon being called, the class instance will call all available callbacks
		using the arguments provided (be it positional or keyword).
	'''
	def __init__(self, callbacks=[]):
		# This conversion removes any duplicates in the callbacks.
		self._callbacks = list(dict.fromkeys(callbacks))

	def __iadd__(self, item):
		if callable(item):
			if not item in self._callbacks:
				self._callbacks.append(item)
		elif isinstance(item, list) or isinstance(item, tuple):
			for callback in item:
				if not callable(callback):
					raise TypeError("Expected 'callable' type for the added callbacks")

			# This conversion removes any duplicates in the callbacks.
			self._callbacks = list(dict.fromkeys(item + self._callbacks))
		else:
			raise TypeError("Expected 'callable', 'list', or 'tuple' type for the added item")

		return self

	def __isub__(self, item):
		if isinstance(item, list) or isinstance(item, tuple):
			for callback in item:
				self._callbacks.remove(callback)
		else:
			self._callbacks.remove(item)
		return self

	def __len__(self):
		return len(self._callbacks)

	def __call__(self, *args, **kwargs):
		for callback in self._callbacks:
			callback(*args, **kwargs)


def main():
	# This example uses the dynamic addition of events, and is typically not
	# recommended if you know the callbacks in advance. If the callbacks are
	# known, the dictionary argument type is preferred.
	handler = EventHandler(['on_event'])
	handler.on_event += print

	handler.on_event('An event happened')
	# Output: An event happened

	# The `print` callback won't be called at all in this case, since it has
	# been removed.
	handler.on_event -= print
	handler.on_event()

	def print_politely(string):
		print(f'{string}, and I just wanted to let you know')

	# This example uses the dynamic addition of events, but simply in list form.
	handler = EventHandler(['on_event'])
	handler.on_event += [print, print_politely]

	handler.on_event('An event happened')
	# Output: An event happened
	# Output: An event happened, and I just wanted to let you know

	# This example uses the forward-knowledge of callbacks to elegantly describe
	# the event. This is the preferred way of creating event handlers.
	handler = EventHandler({
		'on_event': [print, print_politely]
	})

	handler.on_event('An event happened')
	# Output: An event happened
	# Output: An event happened, and I just wanted to let you know


if __name__ == '__main__':
	main()
