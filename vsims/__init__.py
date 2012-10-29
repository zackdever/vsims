"""A very simple in-memory key-value store.

db = vsims.DB() -> a new empty database.
db.set('a', 10) -> set a to 10
db.get('a') - > get the value of a

Also supports transactional blocks.

Built for: http://www.thumbtack.com/challenges
More: https://github.com/zever/vsims
"""

from vsims.db import DB
