# NiceQueue
NiceQueue is an augmented version of python's original thread-safe Queue module.

## Added Abilities
peek, peek_nowait, indexer operator(`__getitem__`), str.

## Usages
```
Q = NiceQueue()
Q.put(10)

print Q[0]  
# 10

print Q.peek()  
# 10 

print Q.peek_no_wait()
# 10

Q.put_left(20)
print Q.peek_no_wait()
# 20

print Q.__repr__()
# NiceQueue object: [20, 10] @ <__main__.NiceQueue object at 0x00000000037F8C50>

print str(Q)
# NiceQueue object: [20, 10]
```


## reference
original python [Queue module](https://docs.python.org/2/library/queue.html) 