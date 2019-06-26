#! /usr/bin/env python

from functools import wraps

toppings = []

def smear(*decorator_args, **decorator_kwargs):
    import pudb; pudb.set_trace()
    called_with_parms = True
    if len(decorator_args) == 1 and callable(decorator_args[0]):
        # decorator can be of form "@smear", or "@smear('stuff')"
        # in the first case there will only one argument and it will be
        # the wrapped function
        called_with_parms = False

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            import pudb; pudb.set_trace()
            toppings.append('ketchup')
            if called_with_parms:
                for topping in decorator_args:
                    toppings.append(topping)

                for name, value in decorator_kwargs.items():
                    if value:
                        toppings.append(name)

            return method(*args, **kwargs)
        return wrapper

    #if len(decorator_args) == 1 and callable(decorator_args[0]):
    if not called_with_parms:
        return decorator(*decorator_args, **decorator_kwargs)

    return decorator



@smear('pickle', mayo=True)
#@smear
def sandwhich(inside, bread='brown', mustard=True):
    if mustard:
        toppings.append('mustard')

    result = 'It is a %s sandwhich with %s bread' % (inside, bread)
    
    if toppings:
        result += ' and '
        result += ', '.join(toppings)

    result += '.'
    print(result)



sandwhich('pastrami', bread='rye')
