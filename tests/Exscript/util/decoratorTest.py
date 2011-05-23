import sys, unittest, re, os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

import Exscript.util.decorator
from Exscript.protocols.Exception import LoginFailure

class FakeConnection(object):
    def __init__(self, os = None):
        self.os   = os
        self.data = {}

    def connect(self):
        self.connected = True

    def login(self, flush = True):
        self.logged_in     = True
        self.login_flushed = flush

    def close(self, force):
        self.connected    = False
        self.close_forced = force

    def guess_os(self):
        return self.os

class decoratorTest(unittest.TestCase):
    CORRELATE = Exscript.util.decorator

    def bind_cb(self, conn, bound_arg1, bound_arg2, **kwargs):
        self.assert_(isinstance(conn, FakeConnection))
        self.assert_(bound_arg1 == 'one', bound_arg1)
        self.assert_(bound_arg2 == 'two', bound_arg2)
        self.assert_(kwargs.get('three') == 3, kwargs.get('three'))
        return 123

    def testBind(self):
        from Exscript.util.decorator import bind
        bound  = bind(self.bind_cb, 'one', 'two', three = 3)
        result = bound(FakeConnection())
        self.assert_(result == 123, result)

    def ios_cb(self, conn):
        return 'hello ios'

    def junos_cb(self, conn):
        return 'hello junos'

    def testOsFunctionMapper(self):
        from Exscript.util.decorator import os_function_mapper
        cb_map = {'ios': self.ios_cb, 'junos': self.junos_cb}
        result = os_function_mapper(FakeConnection(os = 'ios'), cb_map)
        self.assertEqual(result, 'hello ios')

        result = os_function_mapper(FakeConnection(os = 'junos'), cb_map)
        self.assertEqual(result, 'hello junos')

        self.assertRaises(Exception, os_function_mapper, FakeConnection(), cb_map)

    def connect_cb(self, conn, *args, **kwargs):
        self.assert_(conn.connected == True)
        return self.bind_cb(conn, *args, **kwargs)

    def testConnect(self):
        from Exscript.util.decorator import connect
        bound  = connect(self.connect_cb)
        result = bound(FakeConnection(), 'one', 'two', three = 3)
        self.assertEqual(result, 123)

    def autologin_cb(self, conn, *args, **kwargs):
        self.assert_(conn.logged_in == True)
        self.assert_(conn.login_flushed == False)
        return self.connect_cb(conn, *args, **kwargs)

    def testAutologin(self):
        from Exscript.util.decorator import autologin

        # Test simple login.
        bound  = autologin(self.autologin_cb, False)
        result = bound(FakeConnection(), 'one', 'two', three = 3)
        self.assertEqual(result, 123)

        # Monkey patch the fake connection such that the login fails.
        conn = FakeConnection()
        conn.data = 0
        def fail(*args, **kwargs):
            conn.data += 1
            raise LoginFailure('intended login failure')
        conn.login = fail

        # Test retry functionality.
        bound = autologin(self.autologin_cb, False, attempts = 5)
        self.assertRaises(LoginFailure, bound, conn, 'one', 'two', three = 3)
        self.assertEqual(conn.data, 5)

    def testDeprecated(self):
        pass #not really needed.

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(decoratorTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite())
