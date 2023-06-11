from types import GeneratorType
# 再帰用デコレータ
# yieldにするのを忘れないこと
# 参考: https://github.com/cheran-senthil/PyRival/blob/master/pyrival/misc/bootstrap.py
def antirec(func, stack=[]):
  def wrappedfunc(*args, **kwargs):
    if stack:
      return func(*args, **kwargs)
    to = func(*args, **kwargs)
    while True:
      if isinstance(to, GeneratorType):
        stack.append(to)
        to = next(to)
      else:
        stack.pop()
        if not stack:
          break
        to = stack[-1].send(to)
    return to
  return wrappedfunc

def antirec_cache(func, stack=[], memo={}, args_list=[]):
  def wrappedfunc(*args):
    args_list.append(args)
    if stack:
      return func(*args)
    to = func(*args)
    while True:
      if args_list[-1] in memo:
        if not isinstance(to, GeneratorType):
          stack.pop()
        res = memo[args_list.pop()]
        to = stack[-1].send(res)
        continue
      if isinstance(to, GeneratorType):
        stack.append(to)
        to = next(to)
      else:
        memo[args_list.pop()] = to
        stack.pop()
        if not stack:
          break
        to = stack[-1].send(to)
    return to
  return wrappedfunc
