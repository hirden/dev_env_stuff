import sys
import unittest
from nose_helper.config import Config
from nose_helper.util import resolve_name, try_run
import imp

class Test(unittest.TestCase):
    """The universal test case wrapper.
    """
    __test__ = False # do not collect
    def __init__(self, test, config=None):
        if not hasattr(test, '__call__'):
            raise TypeError("Test called with argument %r that "
                            "is not callable. A callable is required."
                            % test)
        self.test = test
        if config is None:
            config = Config()
        self.config = config
        unittest.TestCase.__init__(self)

    def __call__(self, *arg, **kwarg):
        return self.run(*arg, **kwarg)

    def __str__(self):
        return str(self.test)

    def _context(self):
        try:
            return self.test.context
        except AttributeError:
            pass
        try:
            return self.test.__class__
        except AttributeError:
            pass
        try:
            return resolve_name(self.test.__module__)
        except AttributeError:
            pass
        return None
    context = property(_context, None, None,
                      """Get the context object of this test.""")

    def run(self, result):
        try:
            self.runTest(result)
        except KeyboardInterrupt:
            raise
        except:
            err = sys.exc_info()
            result.addError(self, err)

    def runTest(self, result):
        test = self.test
        test(result)


class TestBase(unittest.TestCase):
    """Common functionality for FunctionTestCase and MethodTestCase.
    """
    __test__ = False # do not collect

    class Suite:
      pass

    def runTest(self):
      self.test(*self.arg)

class FunctionTestCase(TestBase):
    """TestCase wrapper for test functions.
    """
    __test__ = False # do not collect

    def __init__(self, test, setUp=None, tearDown=None, arg=tuple(),
                 descriptor=None):
        self.test = test
        self.setUpFunc = setUp
        self.tearDownFunc = tearDown
        self.arg = arg
        self.descriptor = descriptor
        TestBase.__init__(self)
        
        self.suite = TestBase.Suite()
        self.suite.__module__ = self.__get_module()
        self.suite.__name__ = ""
        has_module = True
        try:
          imp.find_module(self.suite.__module__)[1]
        except ImportError:
          has_module  = False
        if sys.version.find("IronPython") != -1 or not has_module:
          # Iron Python doesn't fully support imp
          self.suite.abs_location = ""
          self.suite.location = ""
        else:
          self.suite.abs_location = "file://" + imp.find_module(self.suite.__module__)[1]
          self.suite.location = "file://" + imp.find_module(self.suite.__module__)[1]

    def _context(self):
        return resolve_name(self.test.__module__)
    context = property(_context, None, None,
                      """Get context (module) of this test""")

    def setUp(self):
        """Run any setup function attached to the test function
        """
        if self.setUpFunc:
            self.setUpFunc()
        else:
            names = ('setup', 'setUp', 'setUpFunc')
            try_run(self.test, names)

    def tearDown(self):
        """Run any teardown function attached to the test function
        """
        if self.tearDownFunc:
            self.tearDownFunc()
        else:
            names = ('teardown', 'tearDown', 'tearDownFunc')
            try_run(self.test, names)

    def __str__(self):
        func, arg = self._descriptors()
        if hasattr(func, 'compat_func_name'):
            name = func.compat_func_name
        else:
            name = func.__name__
        if arg:
            name = "%s%s" % (name, arg)
        return name
    __repr__ = __str__

    def __get_module(self):
        func, arg = self._descriptors()
        if hasattr(func, "__module__"):
            return func.__module__
        else:
            #TODO[kate]: get module of function in jython < 2.2
            return "Unknown module."

    def _descriptors(self):
        """In most cases, this is the function itself and no arguments. For
        tests generated by generator functions, the original
        (generator) function and args passed to the generated function
        are returned.
        """
        if self.descriptor:
            return self.descriptor, self.arg
        else:
            return self.test, self.arg


class MethodTestCase(TestBase):
    """Test case wrapper for test methods.
    """
    __test__ = False # do not collect

    def __init__(self, method, test=None, arg=tuple(), descriptor=None):
        """Initialize the MethodTestCase.
        """
        self.method = method
        self.test = test
        self.arg = arg
        self.descriptor = descriptor
        self.cls = method.im_class
        self.inst = self.cls()
        if self.test is None:
            method_name = self.method.__name__
            self.test = getattr(self.inst, method_name)
        TestBase.__init__(self)
        
        self.suite = TestBase.Suite()
        self.suite.__module__, self.suite.__name__ = self.__get_module()

        has_module = True
        try:
          imp.find_module(self.suite.__module__)[1]
        except ImportError:
          has_module  = False
        if sys.version.find("IronPython") != -1 or not has_module:
          # Iron Python doesn't fully support imp
          self.suite.abs_location = ""
        else:
          self.suite.abs_location = "file://" + imp.find_module(self.suite.__module__)[1]
        self.suite.location = "python_uttestid://" + self.suite.__module__ + "." + self.suite.__name__

    def __get_module(self):
      def get_class_that_defined_method(meth):
        import inspect
        obj = meth.im_self
        for cls in inspect.getmro(meth.im_class):
          if meth.__name__ in cls.__dict__: return (cls.__module__, cls.__name__)
        return ("Unknown module", "")

      func, arg = self._descriptors()
      return get_class_that_defined_method(func)

    def __str__(self):
        func, arg = self._descriptors()
        if hasattr(func, 'compat_func_name'):
            name = func.compat_func_name
        else:
            name = func.__name__
        if arg:
            name = "%s%s" % (name, arg)
        return name
    __repr__ = __str__

    def _context(self):
        return self.cls
    context = property(_context, None, None,
                      """Get context (class) of this test""")

    def setUp(self):
        try_run(self.inst, ('setup', 'setUp'))

    def tearDown(self):
        try_run(self.inst, ('teardown', 'tearDown'))

    def _descriptors(self):
        """in most cases, this is the method itself and no arguments. For
        tests generated by generator methods, the original
        (generator) method and args passed to the generated method 
        or function are returned.
        """
        if self.descriptor:
            return self.descriptor, self.arg
        else:
            return self.method, self.arg
