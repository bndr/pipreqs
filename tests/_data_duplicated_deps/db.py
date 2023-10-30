import pymongo  # noqa:F401
from bson.objectid import ObjectId  # noqa:F401

# 'bson' package is mapped to 'pymongo'.
# But running pipreqs should not result in two duplicated
# lines 'pymongo==x.x.x'.
