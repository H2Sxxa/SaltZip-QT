"""timeout"""

import functools
import sys


def timeout(sec, raise_sec=1):
    """
    timeout decorator
    :param sec: function raise TimeoutError after ? seconds
    :param raise_sec: retry kill thread per ? seconds
        default: 1 second
    :example:
    >>> @timeout(3)
    >>> def my_func():
    >>>     ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            err_msg = f'Function {func.__name__} timed out after {sec} seconds'

            if sys.platform != 'win32':
                '''
                非Windows系统，一般对signal都有全面的支持。
                为了实现Timeout功能，可以通过以下几步：
                1. 选用SIGALRM信号来代表Timeout事件；
                2. 将抛出超时异常的事件与SIGALRM信号的触发绑定；
                3. 设定在给定时间后触发SIGALRM信号；
                4. 运行目标函数（如超时，会自动被信号绑定的异常事件打断）。
                '''
                import signal

                def _handle_timeout(signum, frame):
                    raise TimeoutError(err_msg)

                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.alarm(sec)
                try:
                    result = func(*args, **kwargs)
                finally:
                    signal.alarm(0)
                return result

            else:
                '''
                Windows系统对signal的支持很差，因此不能通过上述方法实现。
                新的实现思路是：开启子线程来运行目标函数，主线程计时，超时后中止子线程。
                
                子线程不能向主线程返回执行结果，但是可以和主线程共享内存。
                因此，我们创建result和exception两个mutable变量，分别用来存储子线程的运行结果和异常。
                在子线程结束后，主线程可以直接通过这两个变量获取线程执行结果并顺利返回。
                
                子线程运行中所有的异常，均要保留到子线程结束后，在主线程中处理。
                如果直接在子线程中抛出异常，timeout装饰器的使用者将无法通过try/except捕获并处理该异常。
                因此，子线程运行的函数完全被try/except包住，通过mutable变量交由主线程处理。
                如果出现FuncTimeoutError，说明是超时所致，在子线程内不做捕获。
                '''
                class FuncTimeoutError(TimeoutError):
                    def __init__(self):
                        TimeoutError.__init__(self, err_msg)

                result, exception = [], []

                def run_func():
                    try:
                        res = func(*args, **kwargs)
                    except FuncTimeoutError:
                        pass
                    except Exception as e:
                        exception.append(e)
                    else:
                        result.append(res)

                # typically, a python thread cannot be terminated, use TerminableThread instead
                from .terminable_thread import TerminableThread
                thread = TerminableThread(target=run_func, daemon=True)
                thread.start()
                thread.join(timeout=sec)

                if thread.is_alive():
                    # a timeout thread keeps alive after join method, terminate and raise TimeoutError
                    exc = type('TimeoutError', FuncTimeoutError.__bases__, dict(FuncTimeoutError.__dict__))
                    thread.terminate(exception_cls=FuncTimeoutError, repeat_sec=raise_sec)
                    raise TimeoutError(err_msg)
                elif exception:
                    # if exception occurs during the thread running, raise it
                    raise exception[0]
                else:
                    # if the thread successfully finished, return its results
                    return result[0]

        return wrapped_func
    return decorator
