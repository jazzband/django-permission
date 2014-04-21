#import permission.conf
#import permission.backends
#import permission.handlers
#import permission.logics.utils
#import permission.logics.base
#import permission.logics.author
#import permission.logics.collaborators
#import permission.utils.handlers
#import permission.utils.logics
#import permission.utils.permissions
#import permission.templatetags.permissionif
#import permission.decorators.functionbase
#import permission.decorators.methodbased
#import permission.decorators.classbase

from permission.tests.test_backends import *
from permission.tests.test_handlers import *
from permission.tests.test_utils import *
from permission.tests.test_logics import *
from permission.tests.test_decorators import *
from permission.tests.test_templatetags import *

