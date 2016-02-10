import pymongo
from bson.objectid import ObjectId

# 'bson' package is mapped to 'pymongo'.
# But running pipreqs should not result in two duplicated
# lines 'pymongo==x.x.x'.
