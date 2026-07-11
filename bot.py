#AxiomForceSub --by OwnerAxiom
from loader import app

import handlers.start
import handlers.admin
import handlers.force_sub
import handlers.broadcast
import handlers.stats
import handlers.logs
import handlers.gitpull
import handlers.callbacks


app.run()
