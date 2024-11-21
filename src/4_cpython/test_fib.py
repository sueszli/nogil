import fibmodule


print(fibmodule.__doc__)  # 'Efficient Fibonacci number calculator'

print(dir(fibmodule))

print(fibmodule.fib.__doc__)  # 'Calculate the nth Fibonacci'

print(fibmodule.fib(35))  # 9227465